import socket
import sys
import threading
import socket
import numpy as np
import cv2 as cv
import time
from winreg import *
VALUES_COUNT = 2

IP = "127.0.0.1"  # IP ADDRESS
PORT = 2134  # PORT ADDRESS
TEN_LISTENERS = 10  # AMOUNT OF LISTENERS
FOUR_CHARACTERS = 4  # for zfill
FOUR_BYTES = 4  # for self.my_socket.recv
PARTS = 1024
HEADER_LENGTH = 4
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


class Client(object):
    """
    class client
    """
    def __init__(self, ip, port):
        """
        constructor -- gets ip and port -- initiate server socket
        """
        # self.my_socket = self.initiate_client_socket(ip, port)
        #ip, port = self.registry_values()
        self.my_socket = None
        self.initiate_socket(ip, port)

    def registry_values(self):
        """
        gets server ip and port from registry
        """
        ip = ""
        port = 0
        raw_key = OpenKey(HKEY_LOCAL_MACHINE,
                          r"Computer\HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\client_backup")
        for i in range(VALUES_COUNT):
            try:
                name, value, type = EnumValue(raw_key, i)
                if name == "IPsame":
                    ip = value
                if name == "port":
                    port = value
                print(i, name, value, type)
            except EnvironmentError:
                print("You have ", i, " values")
                break
        CloseKey(raw_key)
        return ip, port

    def initiate_socket(self, ip, port):
        """
        connect client socket
        """
        try:
            # initiate socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # connect to server
            print("ip =", ip)
            print("port =", port)
            sock.connect((ip,  port))
            self.my_socket = sock
            receive_thread = threading.Thread(target=self.receive_socket_message)
            receive_thread.start()

        except Exception as e:
            print("Error initate_client_socket", e)
            exit()

    def receive_socket_message(self):
        """
        sends listening and gets messages from server
        """
        print("enter message: listening + name / call + name")
        mes = input()
        self.send_message_to_server(mes)

        if mes.startswith("listening"):
            self.handle_server_response_list()

        # if wants to send to different client
        elif mes.startswith("call"):
            self.handle_server_response_call()

        # if invalid - not send to or listening
        else:
            self.send_message_to_server("invalid request")

        # while True:
            # header = self.my_socket.recv(FOUR_BYTES)
            # data = self.my_socket.recv(int(header))
            # print(data.decode())  # print data

    def handle_server_response_list(self):
        """
        handle the server response
        """
        try:
            header = self.my_socket.recv(FOUR_BYTES)
            data = self.my_socket.recv(int(header))
            print(data.decode())  # print data
            self.receive_video()
        except Exception as e:
            print("Error: handle_server_response", e)
            self.send_message_to_server('close')  #

    def handle_server_response_call(self):
        """
        handle the server response
        """
        try:
            # print("here - handle_server_response_call")
            header = self.my_socket.recv(FOUR_BYTES)
            data = self.my_socket.recv(int(header))
            print(data.decode())  # print data
            self.send_video()
        except Exception as e:
            print("Error: handle_server_response", e)
            self.send_message_to_server('close')

    def send_message_to_server(self, mes):
        """
        send the request to the server
        """
        try:
            size = (str(len(mes.encode())).zfill(FOUR_CHARACTERS)).encode()
            self.my_socket.send(size + mes.encode())
        except Exception as e:
            print ("Error send_request_to_server:", e)

    def send_video(self):
        """
        sends video to server
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
                    self.send_chunk(code)
                    data = frame.tobytes()
                    for i in range(RANGE_START, len(data), BUF):
                        #self.my_socket.send((str(len(data[i:i + BUF])).zfill(FOUR_CHARACTERS)).encode())
                        #self.my_socket.send(str(i).encode())
                        self.send_chunk(data[i:i + BUF])
                    time.sleep(TIME_SLEEP)
                else:
                    break
        except ConnectionAbortedError as e:
            self.my_socket.close()

    def send_chunk(self, chunk):
        """
        gets chunk and sends to server
        """
        length = len(chunk)
        data = str(length).zfill(MAX_CHUNK_SIZE).encode() + chunk
        self.my_socket.send(data)

    def receive_chunk(self):
        """
        gets chunk from server
        """
        raw_chunk_size = self.my_socket.recv(MAX_CHUNK_SIZE)
        chunk_size = int(raw_chunk_size.decode())
        left = chunk_size
        chunk = b''
        while left > END:
            chunk += self.my_socket.recv(left)
            left = left - len(chunk)
        return chunk

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
            print ("Error send_request_to_server:", e)


def main():
    """
    check my methods
    """
    client = Client(IP, PORT)


if __name__ == '__main__':
    main()
