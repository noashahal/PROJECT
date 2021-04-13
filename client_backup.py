import sys
import threading
import socket
import numpy as np
import cv2 as cv
import time
from winreg import *
from final_peula import *
import pyaudio
VALUES_COUNT = 2
IP = '127.0.0.1'  # IP ADDRESS
SEND_VIDEO_PORT = 1114
RECEIVE_VIDEO_PORT = 1113
SEND_AUDIO_PORT = 1111
RECEIVE_AUDIO_PORT = 1112
TEN_LISTENERS = 10  # AMOUNT OF LISTENERS
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
MAX_CHUNK_SIZE = 10  # for zfill - len of messages
FORMAT = pyaudio.paInt16  # audio format
CHANNELS = 1  # num of channels for audio
RATE = 44100  # audio send rate
chunk = CHUNK = 1024  # audio chunk size
EXIT = -1
ADD = 1  # for counter


class OGClient(object):
    """
    class client Todo: write more
    """
    def __init__(self, call_name, my_name, client_manage):
        """
        todo: comment
        """
        self.receive_video_socket = None
        self.send_video_socket = None
        self.receive_audio_socket = None
        self.send_audio_socket = None
        self.my_name = my_name  # "noa"
        self.call_name = call_name  # "amir"
        self.lock = threading.Lock()
        self.done = False
        self.client_manage = client_manage
        self.call_ended = False

        self.voice_device = pyaudio.PyAudio()

        self.voice_stream = self.voice_device.open(
            format=FORMAT, channels=CHANNELS,
            rate=RATE, frames_per_buffer=chunk,
            input=True, output=True)
        self.initiate_threads()

    def initiate_threads(self):
        """
        sends call to server
        starts thread that sends video
        """
        receive_audio_thread = threading.Thread(target=self.receive_audio)
        receive_audio_thread.start()
        send_audio_thread = threading.Thread(target=self.send_audio)
        send_audio_thread.start()
        # receive_video_thread = threading.Thread(target=self.receive_video)
        # receive_video_thread.start()
        send_video_thread = threading.Thread(target=self.send_video)
        send_video_thread.start()
        self.receive_video()

    def send_video(self):
        """
        sends video to server
        """
        print("got to send video")
        self.send_video_socket = self.start_socket(IP, SEND_VIDEO_PORT)
        self.send_chunk(self.call_name.encode(), self.send_video_socket)
        mes = self.receive_mes(self.send_video_socket)
        print(mes)
        mes = self.receive_mes(self.send_video_socket)
        print(mes)
        while mes == "wait":
            time.sleep(TIME_SLEEP)
            mes = self.receive_mes(self.send_video_socket)
            print(mes)
        # print("here send")
        cap = cv.VideoCapture(CAPTURE, cv2.CAP_DSHOW)
        cap.set(WID, WIDTH)
        cap.set(HIGH, HEIGHT)
        code = 'start'
        code = ('start' + (BUF - len(code)) * 'a').encode('utf-8')
        # try:
        while cap.isOpened() and not self.done:
            # print("here!!!!!")
            try:
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
            except socket.error as msg:
                print("socket failure send video: {}".format(msg))
                self.done = True
                self.call_ended = True
        # except ConnectionAbortedError as e:
        # print("exception send video")
        self.send_video_socket.close()

    @staticmethod
    def send_chunk(chnk, sock):
        """
        gets chunk and sends to server
        """
        length = len(chnk)
        data = str(length).zfill(MAX_CHUNK_SIZE).encode() + chnk
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
        chunk_size = int(raw_chunk_size.decode())
        left = chunk_size

        chunk = b''
        try:
            while left > END:
                chunk += self.receive_video_socket.recv(left)
                left = left - len(chunk)
            return chunk
        except Exception as e:
            print("exception receive chunk 1: {}".format(e))
            self.receive_video_socket.close()
            # sys.exit(EXIT)

    def receive_video(self):
        """
        receives and shows video from server
        """
        try:
            print("receive video!!!!!!!!!!!!!!!")
            self.receive_video_socket = self.start_socket(IP, RECEIVE_VIDEO_PORT)
            self.send_chunk(self.my_name.encode(), self.receive_video_socket)
            print(self.receive_mes(self.receive_video_socket))
            # try:
            frame = self.get_frame()
            show_video(self, frame, self.my_name,
                       self.call_name, self.client_manage)

        except Exception as e:
            self.receive_video_socket.close()
            cv.destroyAllWindows()
            print("Error receive_video:", e)
            # sys.exit(EXIT)

    def get_frame(self):
        """
        gets single frame
        """
        code = b'start'
        num_of_chunks = WIDTH * HEIGHT * WID / BUF
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
        # print("got frame")
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

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
            # sys.exit(EXIT)

    @staticmethod
    def start_socket(ip, port):
        """
        starts and returns socket
        """
        try:
            # initiate socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # connect to server
            print("started socket at ip {} and port {}".format(ip, port))
            sock.connect((ip, port))
            return sock
        except Exception as e:
            print("Error start_socket", e)
            # exit()

    def receive_audio(self):
        """
        receives and plays audio
        """
        print("got to receive audio")
        self.receive_audio_socket = self.start_socket(IP, RECEIVE_AUDIO_PORT)
        self.send_chunk(self.my_name.encode(), self.receive_audio_socket)
        print(self.receive_mes(self.receive_audio_socket))

        print("receive stream made")
        i = 0
        while not self.done:
            try:
                i += 1
                data = self.receive_audio_socket.recv(CHUNK)  # get audio chunk
                self.lock.acquire()
                self.voice_stream.write(data)  # plays
                self.lock.release()
                # if len(data) == 0:
                #    done = True
                # print("wrote chunk #{}".format(i))
            except socket.error as msg:
                print("socket failure receive audio: {}".format(msg))
                self.done = True
                self.call_ended = True
            except KeyboardInterrupt:
                print("exception receive audio")
                self.done = True
                self.call_ended = True
        self.call_ended = True
        self.receive_audio_socket.close()
        # stream_receive.close()
        # p_receive.terminate()

    def send_audio(self):
        """
        records and sends audio to server
        """
        print("got to send audio")
        self.send_audio_socket = self.start_socket(IP, SEND_AUDIO_PORT)
        self.send_chunk(self.call_name.encode(), self.send_audio_socket)
        mes = self.receive_mes(self.send_audio_socket)
        print(mes)
        mes = self.receive_mes(self.send_audio_socket)
        print(mes)
        while mes == "wait":
            time.sleep(TIME_SLEEP)
            mes = self.receive_mes(self.send_audio_socket)
            print(mes)

        print('Recording...')
        print("send stream opened")

        # Store data in chunks for 3 secondsdone = False
        num = 1
        while not self.done:
            try:
                self.lock.acquire()
                data = self.voice_stream.read(chunk)  # records chunk
                self.lock.release()
                # print("chunk {} recorded".format(num))
                self.send_audio_socket.send(data)  # sends chunk
                # print("chunk {} sent".format(num))
                num += 1
            except socket.error as msg:
                print("socket failure send audio: {}".format(msg))
                self.done = True
                self.call_ended = True
                print("call ended is true in thread")
                # self.close_all()
            except Exception as e:
                print("sending audio error: {}".format(e))
                self.done = True
                self.call_ended = True
        print("i am here noa and ayelet")
        self.send_audio_socket.close()
        self.voice_stream.close()
        self.voice_device.terminate()

    def close_all(self):
        """
        closes all sockets and connections
        """
        cv.destroyAllWindows()
        self.done = True
        # sys.exit(EXIT)


def main(call_name, my_name, client_manage):
    """
    check my methods
    """
    client = OGClient(call_name, my_name, client_manage)
    while True:
        time.sleep(TIME_SLEEP)
