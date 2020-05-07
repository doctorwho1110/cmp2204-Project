import socket
import threading
import os
import json
import datetime
import math
import socket


def divide_into_chunks(file, fileName, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    c = os.path.getsize(file)
    CHUNK_SIZE = math.ceil(math.ceil(c) / 5)
    cnt = 1
    with open(file, 'rb') as infile:
        divided_file = infile.read(int(CHUNK_SIZE))
        while divided_file:
            name = directory + "/" + fileName.split('.')[0] + "" + str(cnt)
            with open(name, 'wb+') as div:
                div.write(divided_file)
            cnt += 1
            divided_file = infile.read(int(CHUNK_SIZE))

    user_file = input("Which file do you want to host ? ")

    divide_into_chunks(user_file, )


class Server:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.accept_connections()

    def accept_connections(self):
        ip = socket.gethostbyname(socket.gethostname())
        port = int(input('Enter desired port --> '))

        self.s.bind((ip, port))
        self.s.listen(10)

        print('Running on IP: ' + ip)
        print('Running on port: ' + str(port))

        while 1:
            c, addr = self.s.accept()
            print("Got connection from", addr)
            print(c)

            threading.Thread(target=self.handle_client, args=(c, addr,)).start()

    def handle_client(self, c, addr):
        while True:

            filename = c.recv(4096)

            if not os.path.exists(filename):
                c.send("File does not exist".encode())
            else:
                filename = "p2pfiles/" + json.loads(filename.decode())["files"]
                print("Files received ...")
                if os.path.isfile(filename):
                    c.send("EXISTS" + str(os.path.getsize(filename)))
                    userResponse = c.recv(1024)
                    if userResponse[:2] == 'OK':
                        with open(filename, "rb") as fn:
                            btyesToSend = fn.read(os.path.getsize(filename))
                            c.send(btyesToSend)
                            logins = open("P2P.txt", "a")
                            timenow = datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")
                            logins.write(timenow + "," + addr[0] + "," + filename + "\n")
                            logins.close()
                            break
        c.shutdown(socket.SHUT_RDWR)
        c.close()

    def divide_into_chunks(self, file, fileName, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
        c = os.path.getsize(file)
        CHUNK_SIZE = math.ceil(math.ceil(c) / 5)
        cnt = 1
        with open(file, 'rb') as infile:
            divided_file = infile.read(int(CHUNK_SIZE))
            while divided_file:
                name = directory + "/" + fileName.split('.')[0] + "" + str(cnt)
                with open(name, 'wb+') as div:
                    div.write(divided_file)
                cnt += 1
                divided_file = infile.read(int(CHUNK_SIZE))


server = Server()
