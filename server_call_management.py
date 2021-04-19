import threading
import sys
import socket
import server_backup
import time
TIME_SLEEP = 0.5
MAX_CHUNK_SIZE = 10  # for zfill - len of messages
EXIT = -1
LISTEN = 10
IP = '0.0.0.0'
LISTEN_PORT = 1000
CALL_PORT = 1001
USERS_PORT = 1002
WAIT_KEY = 1


class Server(object):
    def __init__(self):
        """ constructor"""
        try:
            self.call_socket = self.start_socket(IP, CALL_PORT)
            self.listen_socket = self.start_socket(IP, LISTEN_PORT)
            self.users_socket = self.start_socket(IP, USERS_PORT)
            self.client_dict = {}
            # self.start_call()

        except socket.error as e:
            print("socket creation fail: ", e)
            self.call_socket.close()
            self.listen_socket.close()
        except Exception as e:
            print("server construct fail: ", e)

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
    def receive_mes(client_socket):
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

    @staticmethod
    def send_mes(mes, sock):
        """
        gets chunk and sends to server
        """
        # print("mes "+mes.decode())
        # try:
        length = len(mes)
        data = str(length).zfill(MAX_CHUNK_SIZE).encode() + mes
        sock.send(data)
        # except socket.error as msg:
        #     print(msg)
        #     sock.close()

    def handle_clients(self):
        """
        when new client connects, adds to call options
        starts make call thread, which either happens or not
        """
        done = False
        while not done:
            try:
                listening_socket, address = self.listen_socket.accept()
                print("listen socket connect: {}".format(listening_socket))
                name = self.receive_mes(listening_socket)
                # add to options:
                self.client_dict[name] = listening_socket
                # gets string of connected contacts
                options = ','.join(self.client_dict.keys())
                print(options)
                # sends options to client:
                self.send_mes(options.encode(), listening_socket)
                users_thread = threading.Thread(target=self.users)
                users_thread.start()
                client_thread = threading.Thread(target=self.handle_call)
                client_thread.start()

            except socket.error as msg:
                print("socket failure: ", msg)
                done = True
            except Exception as msg:
                print("exception: ", msg)
                done = True

    def users(self):
        """
        refreshes users constantly
        """
        done = False
        users_socket, address = self.users_socket.accept()
        while not done:
            try:
                # gets string of connected contacts
                options = ','.join(self.client_dict.keys())
                # sends options to client:
                self.send_mes(options.encode(), users_socket)
                time.sleep(TIME_SLEEP)
            except socket.error as msg:
                print("socket failure users: ", msg)
                done = True

    def handle_call(self):
        """
        sends options to calling client
        client chooses,
        asks chosen client if wants to allow convo
        if allows,
        calls start call(which currently just prints yay)
        """
        call_socket, address = self.call_socket.accept()
        print("connected call socket: {}".format(call_socket))
        # gets name of user making the call:
        caller_name = self.receive_mes(call_socket)
        # gets from calling client user they want to call:
        receiver_name = self.receive_mes(call_socket)
        # gets receivers socket from dictionary
        if receiver_name not in self.client_dict:
            print("boi bye")
            sys.exit(EXIT)
        receiver_sock = self.client_dict[receiver_name]
        mes = "{} is calling you".format(caller_name)
        self.send_mes(mes.encode(), receiver_sock)
        answer = self.receive_mes(receiver_sock)
        print("answer from {}: {}".format(receiver_name, answer))
        if answer == "Y":
            self.send_mes("call".encode(), call_socket)
            self.start_call()
        else:
            self.send_mes("no call".encode(), call_socket)

    @staticmethod
    def start_call():
        # server_backup.main()
        # print("heyo")
        # server_backup.start_call_og_sever()
        srvr = server_backup.OGServer()
        srvr.handle_clients()


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
