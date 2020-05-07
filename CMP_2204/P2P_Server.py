import socket
import threading
import os
import json
import datetime
import math
import socket

class Server:

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.accept_connections()

    def accept_connections(self):
        ip = socket.gethostbyname(socket.gethostname())
        port = 5001

        self.s.bind((ip, port))
        self.s.listen(10)

        print('Running on IP: ' + ip)
        print('Running on port: ' + str(port))

        while 1:
            c, addr = self.s.accept()
            print("Got connection from", addr)
            print(c)

            threading.Thread(target=self.handle_client, args=(c, addr,)).start()

    def  divide_into_chunks(self, file, fileName, directory):
        '''if not os.path.exists(directory):
            os.makedirs(directory)'''
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

    def handle_client(self, c, addr,fileName,directory):

        while True:
            filename = c.recv(4096)
            if not os.path.exists(filename): #Filename dosyası osde yoksa
                c.send("File does not exist".encode())  # Mesajı gönder
                os.makedirs(directory)
            else:
                filename = "p2pfiles/" + json.loads(filename.decode())["files"] # İsim ataması
                print("Files received ...")
                c.send("EXISTS" + str(os.path.getsize(filename))) #Dosyanı  bulunduğuna dair kullanıcıya mesaj yolla
                userResponse = c.recv(1024) # Kullanıcının mesajını al
                if userResponse[:2] == 'OK':
                    with open(filename, "rb") as fn: #filename adında bir dosya aç
                        bytesToSend = fn.read(os.path.getsize(filename))
                        CHUNK_SIZE=math.ceil(math.ceil(bytesToSend) / 5)
                        #c.send(bytesToSend)
                        cnt = 1
                        divided_file = fn.read(int(CHUNK_SIZE))
                        while divided_file:
                            name = directory + "/" + fileName.split('.')[0] + "" + str(cnt)  # Hatalı olabilir
                            with open(name, 'wb+') as div:
                                div.write(divided_file)
                            cnt += 1
                            divided_file = fn.read(int(CHUNK_SIZE))
            break
        c.shutdown(socket.SHUT_RDWR)
        c.close()




server = Server()
