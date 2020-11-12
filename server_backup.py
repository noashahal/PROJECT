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
            #try:
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
                    self.receive_and_send_video(client_socket, send_socket)

                # if invalid - not send to or listening
                else:
                    self.send_mes("unvalid request", client_socket)

            else:
                print("received illegal size: ", raw_data)
                mes = "error"
                self.send_mes(mes, client_socket)
                break
    """
            # data = data.upper()
        except socket.error as msg:
            print("socket failure: ", msg)
            break
        except Exception as msg:
            print("exception!: ", msg)
            break
        """
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
            handle a sigle client
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
        try:
            code = b'start'
            num_of_chunks = WIDTH * HEIGHT * WID / BUF
            while True:
                chunks = []
                start = False
                chnkC = 0
                while len(chunks) < num_of_chunks:
                    #size = int(receive_socket.recv(FOUR_BYTES).decode())
                    #chunk = receive_socket.recv(size)
                    num = receive_socket.recv(1)
                    print(num.decode() + "chunk number")
                    chunk = receive_socket.recv(BUF)
                    chnkC += 1
                    if start:
                        chunks.append(chunk)
                    elif chunk.startswith(code):
                        start = True




                byte_frame = b''.join(chunks)
                print("got {} chunks. Total len is {}".format(chnkC, len(byte_frame)))
                frame = np.frombuffer(
                    byte_frame, dtype=np.uint8).reshape(HEIGHT, WIDTH, WID)

                data = frame
                code = ('start' + (BUF - len(code)) * 'a').encode('utf-8')
                send_socket.send(code)
                for i in range(RANGE_START, len(data), BUF):
                    #send_socket.send((str(len(data[i:i + BUF])).zfill(FOUR_CHARACTERS)).encode())
                    send_socket.send(data[i:i + BUF])
                time.sleep(TIME_SLEEP)
        except ConnectionAbortedError as e:
            receive_socket.close()


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
