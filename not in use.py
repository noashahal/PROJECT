# client:

def handle_server_response(self):
    """
    handle the server response
    """
    try:
        header = self.my_socket.recv(FOUR_BYTES)
        data = self.my_socket.recv(int(header))
        print(data.decode())  # print data
        return data.decode()
    except Exception as e:
        print("Error: handle_server_response", e)
        self.send_message_to_server('close')  #
        return "ERROR handle_server_response "

def handle_user_input(self):
    """
    Gets the request (input) and checks if it is a lligal command
    if it is:
    send the request to the server, and calls handle_server_response
    and if not - prints "illigal request"
    """
    mes = ''
    while mes.upper() != 'QUIT' and mes.upper() != 'EXIT':
        # while request is not quit/exit
        mes = input()
        self.send_message_to_server(mes)
        self.handle_server_response()


    def send(self):
        capture = cv2.VideoCapture(0)
        #self.client_socket.connect(('127.0.0.1', 50505))

        while True:
            ret, frame = capture.read()
            data = cv2.imencode('.jpg', frame)[1].tostring()
            try:
                self.my_socket.sendto((str(len(data)).zfill(16)).encode(), (IP, PORT))
                self.my_socket.sendto(data, (IP, PORT))
                time.sleep(1/40)
            except socket.error as msg:
                print('Connection failure: %s\n terminating program' % msg)
                sys.exit(1)

    def rec(self):
        n = 0
        while True:
            s = b""
            try:
                length, addr = self.my_socket.recvfrom(16).decode()
                #print (length)
            except socket.error as msg:
                print('Connection failure: %s\n terminating program' % msg)
                sys.exit(1)
            if str(length).isdigit():
                length = int(length)
            else:
                print("error: " + length)
                sys.exit(1)
            try:
                for i in range(int(length/512)):
                    data, addr = self.my_socket.recvfrom(512)
                    s += data
                data, addr = self.my_socket.recvfrom(512)
                s += data
                #n+=1
                #print(n)
                nparr = np.fromstring(s, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                cv2.imshow('frame', frame)
                key = cv2.waitKey(1)
                time.sleep(1/40)
            except socket.error as msg:
                print('Connection failure: %s\n terminating program' % msg)
                sys.exit(1)

# server:
    @staticmethod
    def receive_and_send_video(receive_video_socket, send_video_socket):
        """
        gets video from one client, and sends video to another
        NOTHING HERE WORKSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
        """
        try:
            while True:
                s = b""
                length, addr = receive_video_socket.recvfrom(16)
                # print (length)
                if str(length).isdigit():
                    length = int(length)
                else:
                    print("error: " + length)
                    break
                for i in range(int(length / BUF)):
                    data, addr = receive_video_socket.recvfrom(BUF)
                    s += data
                data, addr = receive_video_socket.recvfrom(BUF)
                s += data
                time.sleep(TIME_SLEEP_2)
                send_video_socket.sendto((str(len(s)).zfill(16)).encode(), (IP, PORT))
                send_video_socket.sendto(s, (IP, PORT))
        except socket.error as msg:
            print("socket failure: ", msg)
        except Exception as msg:
            print("send and receive exception: ", msg)


    def handle_single_client(self, client_socket):
        """ thread function which handles a single client  in a loop """
        mes = None
        while mes != '' and mes != 'close':
            try:
                # receiving data
                mes = self.receive_mes(client_socket)
                # adds a listening socket
                if mes.startswith("listening"):
                    self.client_dict[mes.split(' ')[GET_CLIENT_NAME]] \
                        = client_socket
                    print("client dict is: {}".format(self.client_dict))
                    self.send_mes("listening socket added", client_socket)
                    print("Sent message: "+mes)
                    mes = self.receive_mes(client_socket)
                    print("Rcvd message: " + mes)

                # if wants to send to different client
                if mes.startswith("call"):
                    client_name = mes.split(" ")[GET_CLIENT_NAME]
                    mes = "error here " + mes
                    print("you're calling: "+client_name)
                    while client_name not in self.client_dict:
                        time.sleep(TIME_SLEEP)
                        print("waiting for other client to be added to dict")
                    send_video_socket = self.client_dict[client_name]
                    self.send_mes("calling", client_socket)
                    self.receive_and_send_video(client_socket, send_video_socket)

                else:
                    print("received illegal message: ", mes)
                    mes = "error"
                    self.send_mes(mes, client_socket)
                    break

            except socket.error as msg:
                print("socket failure: ", msg)
                break
            except Exception as msg:
                print("exception!: ", msg)
                break
