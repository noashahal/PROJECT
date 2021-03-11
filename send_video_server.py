import threading
import sys
import socket
import numpy as np
import cv2 as cv
import time
EXIT = -1
LISTEN = 10
IP = '0.0.0.0'
PORT = 1111
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


class Server(object):
    def __init__(self):
        """ constructor"""
        self.server_socket = None
        try:
            self.server_socket = self.start_socket(IP, PORT)
            print('started socket at ip {} port {}'.format(IP, PORT))
            self.client_socket, address = self.server_socket.accept()
            print("connected client socket: {}".format(self.client_socket))
            self.send_video()
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
        print("started socket {}".format(sock))
        return sock

    @staticmethod
    def send_chunk(chunk, send_socket):
        """
        gets chunk and sends to server
        """
        length = len(chunk)
        data = str(length).zfill(MAX_CHUNK_SIZE).encode() + chunk
        send_socket.send(data)

    def send_video(self):
        """
        sends video to client
        """
        # print("here send")
        cap = cv.VideoCapture(CAPTURE)
        cap.set(WID, WIDTH)
        cap.set(HIGH, HEIGHT)
        code = 'start'
        code = ('start' + (BUF - len(code)) * 'a').encode('utf-8')
        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    self.send_chunk(code, self.client_socket)
                    data = frame.tobytes()
                    for i in range(RANGE_START, len(data), BUF):
                        self.send_chunk(data[i:i + BUF],
                                        self.client_socket)
                    time.sleep(TIME_SLEEP)
                else:
                    break
        except ConnectionAbortedError as e:
            print("exception send video")
            self.server_socket.close()


def main():
    """
    todo: write more
    """
    try:
        server_ = Server()
    except socket.error as msg:
        print("socket failure: ", msg)
    except Exception as msg:
        print("exception: ", msg)


if __name__ == '__main__':
    main()
