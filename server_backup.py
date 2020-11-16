import socket
import threading
import sys
import socket
import numpy as np
import cv2 as cv
import time
FOUR_BYTES = 4
EXIT = -1
LISTEN = 10
MSG_LEN = 4
IP = '0.0.0.0'
PORT = 2134
GET_CLIENT_NAME = 1
SOCKET_IN_MESSAGE = 1
BUF = 512
WIDTH = 640
HEIGHT = 480
RANGE_START = 0
CAPTURE = 0
TIME_SLEEP = 0.1
WID = 3
HIGH = 4
WAIT_KEY = 1
END = 0
MAX_CHUNK_SIZE = 10


class Server(object):
    def __init__(self):
        """ constructor"""
        self.server_socket = None
        try:
            # initiating server socket
            self.server_socket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
            # the server binds itself to a certain socket
            self.server_socket.bind((IP, PORT))
            # listening to the socket
            self.server_socket.listen(LISTEN)
            self.client_dict = {}
        except socket.error as e:
            print("booz!!", e)
            sys.exit(EXIT)
        except Exception as e:
            print("booz!!!", e)
            sys.exit(EXIT)

    def handle_single_client(self, client_socket):
        """ thread function which handles a single client  in a loop """
        data = None
        while data != '' and data != 'close':
            try:
                # receiving data
                raw_data = client_socket.recv(MSG_LEN)
                data = raw_data.decode()
                if data.isdigit():
                    mes = client_socket.recv(int(data)).decode()

                    # adds a listening socket
                    if mes.startswith("listening"):
                        self.client_dict[mes.split(' ')[GET_CLIENT_NAME]] \
                            = client_socket
                        # print(self.client_dict)
                        self.send_mes("listening socket added", client_socket)

                    # if wants to send to different client
                    elif mes.startswith("call"):
                        client_name = mes.split(" ")[GET_CLIENT_NAME]
                        # print("you're calling: "+client_name)
                        send_socket = self.client_dict[client_name]
                        self.send_mes("calling", client_socket)
                        #raw_data = client_socket.recv(MSG_LEN)
                        #data = int(raw_data.decode())
                        #mes = str(client_socket.recv(data).decode())
                        #self.client_dict[mes.split(' ')[GET_CLIENT_NAME]] \
                            #= client_socket
                        #print(self.client_dict)
                        #self.send_mes("listening socket added", client_socket)
                        self.receive_and_send_video(client_socket, send_socket)

                    # if invalid - not send to or listening
                    else:
                        self.send_mes("unvalid request", client_socket)

                else:
                    print("received illegal size: ", raw_data)
                    mes = "error"
                    self.send_mes(mes, client_socket)
                    break

            except socket.error as msg:
                print("socket failure: ", msg)
                break
            except Exception as msg:
                print("exception!: ", msg)
                break

    @staticmethod
    def send_mes(message, send_socket):
        """
        receives and sends message
        """
        message = message.encode()
        size = (str(len(message)).zfill(MSG_LEN)).encode()
        send_socket.send(size + message)

    def handle_clients(self):
            """
            handle a single client
            accepts a connection request and call handle _client
            for receiving its requests
            """
            done = False
            while not done:
                try:
                    # accepting a connect request
                    client_socket, address = self.server_socket.accept()
                    print("client accepted")
                    clnt_thread = threading.Thread(
                        target=self.handle_single_client, args=(client_socket,))
                    clnt_thread.start()

                except socket.error as msg:
                    print("socket failure: ", msg)
                    done = True
                except Exception as msg:
                    print("exception: ", msg)
                    done = True

    def receive_and_send_video(self, receive_socket, send_socket):
        """
        gets video from client and sends to other client
        doesn't SHOW video
        """
        print("got to receive and send video")
        try:
            #code = b'start'
            num_of_chunks = WIDTH * HEIGHT * WID / BUF
            num = 0
            while True:
                chunks = []
                #start = False
                while len(chunks) < num_of_chunks:
                    num += 1
                    chunk = self.receive_chunk(receive_socket, num)
                    self.send_chunk(chunk, send_socket)
                    #if start:
                        #chunks.append(chunk)
                    #elif chunk.startswith(code):
                        #start = True

                #byte_frame = b''.join(chunks)
                #print("got {} chunks. Total len is {}".format(num, len(byte_frame)))
                #frame = np.frombuffer(
                    #byte_frame, dtype=np.uint8).reshape(HEIGHT, WIDTH, WID)

                #data = frame
                # data = byte_frame
                #code = ('start' + (BUF - len(code)) * 'a').encode('utf-8')
                #self.send_chunk(code, send_socket)
                #for i in range(RANGE_START, len(data), BUF):
                    #send_socket.send((str(len(data[i:i + BUF])).zfill(FOUR_CHARACTERS)).encode())
                    #self.send_chunk(data[i:i + BUF], send_socket)
                #time.sleep(TIME_SLEEP)
        except ConnectionAbortedError as e:
            receive_socket.close()

    @staticmethod
    def send_chunk(chunk, send_socket):
        """
        gets chunk and sends to server
        """
        length = len(chunk)
        data = str(length).zfill(MAX_CHUNK_SIZE).encode() + chunk
        send_socket.send(data)

    @staticmethod
    def receive_chunk(receive_socket, num):
        """
        gets chunk from server
        """
        raw_chunk_size = b''
        raw_chunk_size_to_get = MAX_CHUNK_SIZE
        while len(raw_chunk_size) < raw_chunk_size_to_get:
            raw_chunk_size += receive_socket.recv(raw_chunk_size_to_get - len(raw_chunk_size))
        try:
            chunk_size = int(raw_chunk_size.decode())
        except:
            print('raw chunk size is {} its length is {}'.format(raw_chunk_size, len(raw_chunk_size)))
        #print("chunk num {} size: {}".format(num, raw_chunk_size))
        left = chunk_size
        chunk = b''
        while left > END:
            chunk += receive_socket.recv(left)
            left = left - len(chunk)
        return chunk


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
