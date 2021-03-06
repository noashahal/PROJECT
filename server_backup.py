import threading
import sys
import socket
# import numpy as np
# import cv2 as cv
import time
# import pyaudio
# from constants import *
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
ADD = 1
MAX_CHUNK_SIZE = 10  # for zfill - len of messages
CHUNK = 1024


class OGServer(object):
    def __init__(self):
        """ constructs server - starts sockets"""
        self.server_socket = None
        try:
            self.receive_video_socket = \
                self.start_socket(IP, RECEIVE_VIDEO_PORT)
            print('started socket at ip {} port {}'
                  .format(IP, RECEIVE_VIDEO_PORT))
            self.send_video_socket = \
                self.start_socket(IP, SEND_VIDEO_PORT)
            print('started socket at ip {} port {}'
                  .format(IP, SEND_VIDEO_PORT))
            self.receive_audio_socket = \
                self.start_socket(IP, RECEIVE_AUDIO_PORT)
            print('started socket at ip {} port {}'
                  .format(IP, RECEIVE_AUDIO_PORT))
            self.send_audio_socket = \
                self.start_socket(IP, SEND_AUDIO_PORT)
            print('started socket at ip {} port {}'
                  .format(IP, SEND_AUDIO_PORT))
            self.client_video_dict = {}
            self.client_audio_dict = {}

        except socket.error as e:
            print("socket creation fail: ", e)
            self.close_all()
        except Exception as e:
            print("server construct fail: ", e)
            self.close_all()

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
        done = False
        while not done:
            try:
                # starts threads
                receive_video_client_socket, address = \
                    self.receive_video_socket.accept()
                print("connected relay video: {}"
                      .format(receive_video_client_socket))
                video_thread = \
                    threading.Thread(target=self.start_video_relay,
                                     args=(receive_video_client_socket, ))
                audio_thread = threading.Thread(target=self.start_audio_relay)
                video_thread.start()
                audio_thread.start()

            except socket.error as msg:
                print("socket failure handle clients: ", msg)
                done = True
            except Exception as msg:
                print("exception handle clients: ", msg)
                done = True

    def start_video_relay(self, receive_video_client_socket):
        """
        connects receive video socket,
        gets name
        calls receive_and_send_video with names socket
        """
        try:
            self.add_video_client()
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
            self.close_all()
        except Exception as e:
            print("video relay exception: ", e)
            self.close_all()

    def start_audio_relay(self):
        """
        connects receive audio socket,
        gets name
        calls receive_and_send_audio with names socket
        """
        try:
            self.add_audio_client()
            receive_audio_client_socket, address = \
                self.receive_audio_socket.accept()
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
            self.close_all()
        except Exception as e:
            print("audio relay exception: ", e)
            self.close_all()

    def add_video_client(self):
        """
        connects send video socket,
        gets name
        adds name to dictionary
        """
        try:
            # print("starting receive video")
            send_video_client_socket, address = self.send_video_socket.accept()
            print("connected receive video: {}"
                  .format(send_video_client_socket))
            my_name = self.receive_mes(send_video_client_socket)
            self.client_video_dict[my_name] = send_video_client_socket
            self.send_chunk("listening vid".encode(), send_video_client_socket)
            print(self.client_video_dict)
        except socket.error as e:
            print("socket add video client fail: ", e)
            self.close_all()
        except Exception as e:
            print("add video client exception: ", e)
            self.close_all()

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
            self.send_chunk("listening audio".encode(),
                            send_audio_client_socket)
        except socket.error as e:
            print("socket add audio client fail: ", e)
            self.close_all()
        except Exception as e:
            print("add audio client exception: ", e)
            self.close_all()

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
            self.close_all()

    @staticmethod
    def receive_and_send_audio(receive_audio_socket, send_audio_socket):
        """
        gets audio chunk from one client, sends to other client
        without playing audio!
        different stream for sending and receiving!
        """
        try:
            while True:
                data = receive_audio_socket.recv(CHUNK)
                if len(data) == END:
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
        gets chunk and socket and sends
        """
        length = len(chunk)
        data = str(length).zfill(MAX_CHUNK_SIZE).encode() + chunk
        send_socket.send(data)

    @staticmethod
    def receive_chunk(receive_socket):
        """
        gets chunk from server
        """
        raw_chunk_size = b''
        raw_chunk_size_to_get = MAX_CHUNK_SIZE
        while len(raw_chunk_size) < raw_chunk_size_to_get:
            rec = raw_chunk_size_to_get - len(raw_chunk_size)
            raw_chunk_size += receive_socket.recv(rec)
        try:
            chunk_size = int(raw_chunk_size.decode())
        except:
            print('raw chunk size is {} its length is {}'
                  .format(raw_chunk_size, len(raw_chunk_size)))
        left = chunk_size
        chunk = b''
        while left > END:
            chunk += receive_socket.recv(left)
            left = left - len(chunk)
        return chunk

    def receive_mes(self, client_socket):
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
            self.close_all()

    def close_all(self):
        """
        closes all sockets and connections
        """
        self.receive_video_socket.close()
        self.send_video_socket.close()
        self.receive_audio_socket.close()
        self.send_audio_socket.close()
        sys.exit(EXIT)


def main():
    """
    todo: write more
    """
    try:
        srvr = OGServer()
        srvr.handle_clients()
    except socket.error as msg:
        print("socket failure main: ", msg)
    except Exception as msg:
        print("exception main: ", msg)


if __name__ == '__main__':
    main()
