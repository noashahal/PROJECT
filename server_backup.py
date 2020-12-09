import threading
import sys
import socket
import numpy as np
import cv2 as cv
import time
import pyaudio
FOUR_BYTES = 4
EXIT = -1
LISTEN = 10
IP = '0.0.0.0'
SEND_VIDEO_PORT = 1113
RECEIVE_VIDEO_PORT = 1114
SEND_AUDIO_PORT = 1112
RECEIVE_AUDIO_PORT = 1111
GET_CLIENT_NAME = 1
SOCKET_IN_MESSAGE = 1
BUF = 512  # size of video chunk
WIDTH = 640
HEIGHT = 480
RANGE_START = 0
CAPTURE = 0
TIME_SLEEP = 5
WID = 3
HIGH = 4
WAIT_KEY = 1
END = 0
MAX_CHUNK_SIZE = 10  # for zfill - len of messages
CHUNK = 1024
MAX_CONNECT = 2


class Server(object):
    def __init__(self):
        """ constructor"""
        self.server_socket = None
        try:
            self.receive_video_socket = self.start_socket(IP, RECEIVE_VIDEO_PORT)
            print('started socket at ip {} port {}'.format(IP, RECEIVE_VIDEO_PORT))
            self.send_video_socket = self.start_socket(IP, SEND_VIDEO_PORT)
            print('started socket at ip {} port {}'.format(IP, SEND_VIDEO_PORT))
            self.receive_audio_socket = self.start_socket(IP, RECEIVE_AUDIO_PORT)
            print('started socket at ip {} port {}'.format(IP, RECEIVE_AUDIO_PORT))
            self.send_audio_socket = self.start_socket(IP, SEND_AUDIO_PORT)
            print('started socket at ip {} port {}'.format(IP, SEND_AUDIO_PORT))
            self.client_video_dict = {}
            self.client_audio_dict = {}

        except socket.error as e:
            print("socket creation fail: ", e)
            sys.exit(EXIT)
        except Exception as e:
            print("server construct fail: ", e)
            sys.exit(EXIT)

    @staticmethod
    def start_socket(ip, port):
        """
        starts a socket with ip and port
        """
        sock = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        # the server binds itself to a certain socket
        sock.bind((ip, port))
        # listening to the socket
        sock.listen(LISTEN)
        return sock

    @staticmethod
    def send_mes(message, send_video_socket):
        """
        receives and sends message
        """
        message = message.encode()
        size = (str(len(message)).zfill(MAX_CHUNK_SIZE)).encode()
        send_video_socket.send(size + message)

    def handle_clients(self):
        """
        handle a single client
        accepts a connection request and call handle _client
        for receiving its requests
        """
        num = 0
        done = False
        while not done and num < MAX_CONNECT:
            try:
                # starts threads

                receive_video_thread = threading.Thread(target=self.add_video_client)
                receive_audio_thread = threading.Thread(target=self.add_audio_client)
                send_video_thread = threading.Thread(target=self.start_video_relay)
                send_audio_thread = threading.Thread(target=self.start_audio_relay)
                receive_video_thread.start()
                print("started receive video thread")
                receive_audio_thread.start()
                print("started receive audio thread")
                send_video_thread.start()
                print("started send video thread")
                send_audio_thread.start()
                print("started send audio thread")
                num += 1

            except socket.error as msg:
                print("socket failure: ", msg)
                done = True
            except Exception as msg:
                print("exception: ", msg)
                done = True

    def start_video_relay(self):
        """
        connects receive video socket,
        gets name
        calls receive_and_send_video with names socket
        """
        try:
            receive_video_client_socket, address = self.receive_video_socket.accept()
            print("connected relay video: {}".format(receive_video_client_socket))
            name = self.receive_mes(receive_video_client_socket)
            print("calling: {}".format(name))
            self.send_chunk("calling".encode(), receive_video_client_socket)
            while name not in self.client_video_dict:
                time.sleep(TIME_SLEEP)
                print("waiting for the other client to connect")
                self.send_chunk("wait".encode(), receive_video_client_socket)
            self.send_chunk("start".encode(), receive_video_client_socket)
            send_sock = self.client_video_dict[name]
            self.receive_and_send_video(receive_video_client_socket, send_sock)
        except socket.error as e:
            print("socket video relay fail: ", e)
            sys.exit(EXIT)
        except Exception as e:
            print("video relay exception: ", e)
            sys.exit(EXIT)

    def start_audio_relay(self):
        """
        connects receive audio socket,
        gets name
        calls receive_and_send_audio with names socket
        """
        try:
            receive_audio_client_socket, address = self.receive_audio_socket.accept()
            print("connected relay audio")
            name = self.receive_mes(receive_audio_client_socket)
            self.send_chunk("calling".encode(), receive_audio_client_socket)
            while name not in self.client_audio_dict:
                time.sleep(TIME_SLEEP)
                print("waiting for the other client to connect")
                self.send_chunk("wait".encode(), receive_audio_client_socket)
            self.send_chunk("start".encode(), receive_audio_client_socket)
            send_sock = self.client_audio_dict[name]
            self.receive_and_send_audio(receive_audio_client_socket, send_sock)
        except socket.error as e:
            print("socket audio relay fail: ", e)
            sys.exit(EXIT)
        except Exception as e:
            print("audio relay exception: ", e)
            sys.exit(EXIT)

    def add_video_client(self):
        """
        connects send video socket,
        gets name
        adds name to dictionary
        """
        try:
            #print("starting receive video")
            send_video_client_socket, address = self.send_video_socket.accept()
            print("connected receive video: {}".format(send_video_client_socket))
            my_name = self.receive_mes(send_video_client_socket)
            self.client_video_dict[my_name] = send_video_client_socket
            self.send_chunk("listening vid".encode(), send_video_client_socket)
            print(self.client_video_dict)
        except socket.error as e:
            print("socket add video client fail: ", e)
            sys.exit(EXIT)
        except Exception as e:
            print("add video client exception: ", e)
            sys.exit(EXIT)

    def add_audio_client(self):
        """
        connects send video socket,
        gets name
        adds name to dictionary
        """
        try:
            send_audio_client_socket, address = self.send_audio_socket.accept()
            print("connected receive audio")
            my_name = self.receive_mes(send_audio_client_socket)
            self.client_audio_dict[my_name] = send_audio_client_socket
            self.send_chunk("listening audio".encode(), send_audio_client_socket)
        except socket.error as e:
            print("socket add audio client fail: ", e)
            sys.exit(EXIT)
        except Exception as e:
            print("add audio client exception: ", e)
            sys.exit(EXIT)

    def receive_and_send_video(self, receive_video_socket, send_video_socket):
        """
        gets video from client and sends to other client
        doesn't SHOW video
        """
        print("got to receive and send video")
        try:
            num_of_chunks = WIDTH * HEIGHT * WID / BUF
            while True:
                chunks = []
                while len(chunks) < num_of_chunks:
                    chunk = self.receive_chunk(receive_video_socket)
                    self.send_chunk(chunk, send_video_socket)

        except ConnectionAbortedError as e:
            receive_video_socket.close()

    @staticmethod
    def receive_and_send_audio(receive_audio_socket, send_audio_socket):
        """
        gets audio chunk from one client, sends to other client
        without playing audio!
        different stream for sending and receiving!
        """
        i = 0
        try:
            while True:
                i += 1
                data = receive_audio_socket.recv(CHUNK)
                print("got audio chunk number {} of length {}".format(i, len(data)))
                if len(data) == 0:
                    break
                send_audio_socket.send(data)
        except KeyboardInterrupt:
            pass
        print('Shutting down')
        receive_audio_socket.close()
        send_audio_socket.close()

    @staticmethod
    def send_chunk(chunk, send_socket):
        """
        gets chunk and sends to server
        """
        length = len(chunk)
        data = str(length).zfill(MAX_CHUNK_SIZE).encode() + chunk
        send_socket.send(data)

    @staticmethod
    def receive_chunk(receive_video_socket):
        """
        gets chunk from server
        """
        raw_chunk_size = b''
        raw_chunk_size_to_get = MAX_CHUNK_SIZE
        while len(raw_chunk_size) < raw_chunk_size_to_get:
            raw_chunk_size += receive_video_socket.recv(raw_chunk_size_to_get - len(raw_chunk_size))
        try:
            chunk_size = int(raw_chunk_size.decode())
        except:
            print('raw chunk size is {} its length is {}'.format(raw_chunk_size, len(raw_chunk_size)))
        left = chunk_size
        chunk = b''
        while left > END:
            chunk += receive_video_socket.recv(left)
            left = left - len(chunk)
        return chunk

    @staticmethod
    def receive_mes(client_socket):
        """
        receives and returns message from client
        """
        try:
            raw_data = client_socket.recv(MAX_CHUNK_SIZE)
            data = raw_data.decode()
            mes = "invalid message"
            if data.isdigit():
                mes = client_socket.recv(int(data)).decode()
                mes = str(mes)
            return mes
        except Exception as e:
            client_socket.close()
            print("Error in receive_mes: ", e)

    def close_all(self):
        """
        closes all sockets and connections
        """
        self.receive_video_socket.close()
        self.send_video_socket.close()
        self.receive_audio_socket.close()
        self.send_audio_socket.close()


def main():
    """
    server main - receives a message returns it to client
    """
    try:
        srvr = Server()
        srvr.handle_clients()
    except socket.error as msg:
        print("socket failure: ", msg)
    except Exception as msg:
        print("exception: ", msg)


if __name__ == '__main__':
    main()
