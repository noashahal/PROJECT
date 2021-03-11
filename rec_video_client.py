import threading
import sys
import socket
import numpy as np
import cv2 as cv
import time
EXIT = -1
LISTEN = 10
IP = '172.29.225.78'
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


class Client(object):
    """
    class client
    """
    def __init__(self):
        self.my_socket = self.start_socket(IP, PORT)
        self.receive_video()

    @staticmethod
    def start_socket(ip, port):
        """
        starts and returns socket
        """
        try:
            # initiate socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # connect to server
            sock.connect((ip, port))
            print("started and connected socket: {}".format(sock))
            return sock
        except Exception as e:
            print("Error start_socket", e)

    def receive_video(self):
        """
        receives and shows video from server
        """
        try:
            code = b'start'
            num_of_chunks = WIDTH * HEIGHT * WID / BUF
            while True:
                chunks = []
                start = False
                while len(chunks) < num_of_chunks:
                    chunk = self.receive_chunk()
                    if start:
                        chunks.append(chunk)
                    elif chunk.startswith(code):
                        start = True

                byte_frame = b''.join(chunks)
                frame = np.frombuffer(
                    byte_frame, dtype=np.uint8).reshape(HEIGHT, WIDTH, WID)

                cv.imshow('recv', frame)
                if cv.waitKey(WAIT_KEY) & 0xFF == ord('q'):
                    break

            self.my_socket.close()
            cv.destroyAllWindows()

        except Exception as e:
            self.my_socket.close()
            cv.destroyAllWindows()
            print("Error receive_video:", e)
            sys.exit(EXIT)

    def receive_chunk(self):
        """
        gets chunk from server
        """
        raw_chunk_size = b''
        raw_chunk_size_to_get = MAX_CHUNK_SIZE
        while len(raw_chunk_size) < raw_chunk_size_to_get:
            raw_chunk_size += self.my_socket.recv(
                raw_chunk_size_to_get - len(raw_chunk_size))
        try:
            chunk_size = int(raw_chunk_size.decode())
        except Exception as e:
            print('raw chunk size is {} its length is {}'
                  .format(raw_chunk_size, len(raw_chunk_size)))
            print("exception receive chunk 1: {}".format(e))
        left = chunk_size
        chunk = b''
        try:
            while left > END:
                chunk += self.my_socket.recv(left)
                left = left - len(chunk)
            return chunk
        except Exception as e:
            print("exception receive chunk 1: {}".format(e))
            self.my_socket.close()


def main():
    """
    check my methods
    """
    client = Client()
    while True:
        time.sleep(TIME_SLEEP)


if __name__ == '__main__':
    main()
