import sys
import threading
import socket
import numpy as np
import cv2 as cv
import time
from winreg import *
import pyaudio

VALUES_COUNT = 2
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
TIME_SLEEP_USERS = 0.5
WID = 3
HIGH = 4
WAIT_KEY = 1
END = 0
MAX_CHUNK_SIZE = 10
