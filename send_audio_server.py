import pyaudio
import socket
import threading
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
chunk = CHUNK = 1024
MAX_CHUNK_SIZE = 10


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
        print("Error in receive_mes: ", e)


def receive_and_save_audio():
    """
    receives audio chunks and plays as WAV file
    """
    try:
        rec_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        rec_socket.bind(('10.100.102.97', 1111))
        rec_socket.listen(10)
        print(rec_socket)
        print("listening!")
        sock, address = rec_socket.accept()
        print("sending client accepted")
    except Exception as e:
        print("sending client error: ", e)

    p_rec = pyaudio.PyAudio()
    stream_rec = p_rec.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK,
                            input=False)
    i = 0
    try:
        while True:
            i += 1
            data = sock.recv(CHUNK)
            print("got chunk number {} of length {}".format(i, len(data)))
            #if len(data) == 0:
                #break
            stream_rec.write(data)
            #print("wrote chunk #{}".format(i))
    except KeyboardInterrupt:
        pass
    print('Shutting down')
    sock.close()
    stream_rec.close()
    p_rec.terminate()


def record_and_send_audio():
    """
    records and sends audio in real time
    """
    try:
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        send_socket.bind(("10.100.102.97", 1112))
        send_socket.listen(10)
        print(send_socket)
        print("listening!")
        sock, address = send_socket.accept()
        print("receiving client accepted")
    except Exception as e:
        print("receiving client error: ", e)

    p_send = pyaudio.PyAudio()  # Create an interface to PortAudio
    print('Recording...')
    stream_send = p_send.open(format=FORMAT, channels=CHANNELS, rate=RATE, frames_per_buffer=chunk, input=True,
                              output=False)
    try:
        # Store data in chunks for 3 seconds
        done = False
        while not done:
            data = stream_send.read(chunk)
            sock.send(data)
        print('Finished recording')
    except Exception as e:
        print("sending audio error: {}".format(e))


def main():
    """
    main
    """
    send_audio_thread = threading.Thread(
        target=record_and_send_audio)
    send_audio_thread.start()
    rec_audio_thread = threading.Thread(
        target=receive_and_save_audio)
    rec_audio_thread.start()


if __name__ == '__main__':
    main()
