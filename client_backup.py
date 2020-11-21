import socket
import sys
import threading
import socket
import numpy as np
import cv2 as cv
import time
from winreg import *
from constants import *


class Client(object):
    """
    class client Todo: write more
    """
    def __init__(self, ip, port):
        """
        constructor -- gets ip and port -- initiate both sockets
        """
        # ip, port = self.registry_values()
        self.receive_video_socket = None
        self.connect_to_server(ip, port, "listening")
        self.send_video_socket = None
        self.connect_to_server(ip, port, "call")
        self.my_name = "noa"
        self.call_name = "amir"

    def registry_values(self):
        """
        gets server ip and port from registry
        """
        ip = ""
        port = 0
        raw_key = OpenKey(HKEY_LOCAL_MACHINE,
                          r"Computer\HKEY_LOCAL_MACHINE"
                          r"\SOFTWARE\WOW6432Node\client_backup")
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

    def connect_to_server(self, ip, port, kind):
        """
        connect client socket
        """
        sock = ''
        try:
            # initiate socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # connect to server
            print("ip =", ip)
            print("port =", port)
            sock.connect((ip, port))
        except Exception as e:
            print("Error initate_client_socket", e)
            exit()

        if kind == "call":
            self.initiate_send_thread(sock)

        else:
            self.initiate_receive_thread(sock)

    def initiate_send_thread(self, sock):
        """
        sends call to server
        starts thread that sends video
        """
        self.send_video_socket = sock
        mes = "call " + str(self.call_name)
        self.send_chunk(mes.encode(), self.send_video_socket)
        mes = self.receive_mes(self.send_video_socket)
        print(mes)
        send_thread = threading.Thread(target=self.send_video)
        send_thread.start()

    def initiate_receive_thread(self, sock):
        """
        sends listening to server
        starts thread that receives video
        """
        self.receive_video_socket = sock
        mes = "listening " + str(self.my_name)
        self.send_chunk(mes.encode(), self.receive_video_socket)
        mes = self.receive_mes(self.receive_video_socket)
        print(mes)
        receive_thread = threading.Thread(target=self.receive_video)
        receive_thread.start()

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
                    self.send_chunk(code, self.send_video_socket)
                    data = frame.tobytes()
                    for i in range(RANGE_START, len(data), BUF):
                        self.send_chunk(data[i:i + BUF],
                                        self.send_video_socket)
                    time.sleep(TIME_SLEEP)
                else:
                    break
        except ConnectionAbortedError as e:
            self.send_video_socket.close()

    @staticmethod
    def send_chunk(chunk, sock):
        """
        gets chunk and sends to server
        """
        length = len(chunk)
        data = str(length).zfill(MAX_CHUNK_SIZE).encode() + chunk
        sock.send(data)

    def receive_chunk(self):
        """
        gets chunk from server
        """
        raw_chunk_size = b''
        raw_chunk_size_to_get = MAX_CHUNK_SIZE
        while len(raw_chunk_size) < raw_chunk_size_to_get:
            raw_chunk_size += self.receive_video_socket.recv(
                raw_chunk_size_to_get - len(raw_chunk_size))
        try:
            chunk_size = int(raw_chunk_size.decode())
        except:
            print('raw chunk size is {} its length is {}'
                  .format(raw_chunk_size, len(raw_chunk_size)))
        left = chunk_size
        chunk = b''
        while left > END:
            chunk += self.receive_video_socket.recv(left)
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

            self.receive_video_socket.close()
            cv.destroyAllWindows()

        except Exception as e:
            self.receive_video_socket.close()
            cv.destroyAllWindows()
            print ("Error send_request_to_server:", e)

    @staticmethod
    def receive_mes(sock):
        """
        receives and returns message from client
        """
        try:
            raw_data = sock.recv(MAX_CHUNK_SIZE)
            data = raw_data.decode()
            mes = "invalid message"
            if data.isdigit():
                mes = sock.recv(int(data)).decode()
                mes = str(mes)
            return mes
        except Exception as e:
            sock.close()
            print("Error receive_mes: ", e)


def main():
    """
    check my methods
    """
    client = Client(IP, PORT)


if __name__ == '__main__':
    main()
