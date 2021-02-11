import datetime
import json
import os
import math
import socket
import threading

'''
def start_socket(ip):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        ip = socket.gethostbyname(socket.gethostname())
        port = 5001
        s.bind((ip, port))
        s.listen(10)
        print('Running on IP: ' + ip)
'''

def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("1.1.1.1", 1))  # erişilmesine gerek yok ip tespiti için.
    ip = s.getsockname()[0]  # for hamachi update this line ip = "25.147.229.97" with your hamachi ipv4
    s.close()
    print("\n" + "P2P Server Started!")
    print("Listening from " + ip)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((ip, 5001))
    sock.listen(10)
    while True:
        connection, clientInfo = sock.accept()
        thread = threading.Thread(target=handleSend, args=(connection, clientInfo))
        thread.start()


def create_file(fileName, connection, clientInfo):
    with open(fileName, "rb") as f:
        connection.send(f.read(os.path.getsize(fileName)))
        log_file = open("server.txt", "a")
        current_time = datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")
        log_file.write(
            current_time
            + "," + clientInfo[0] + "," + fileName + "\n"
        )
        log_file.close()


def handleSend(connection, clientInfo):
    try:
        while True:
            d = connection.recv(4096)
            if d:
                fileName = "files/" + json.loads(d.decode())["filename"]
                create_file(fileName, connection, clientInfo)
                break
            else:
                break
    except:
        print("Error Occurred")
    finally:
        connection.close()


if __name__ == '__main__':
    if not os.path.exists('files'):
        os.makedirs('files')
    print("P2P Server Starting.." + "\n")
    print("The file to be shared and the project must be in the same folder")
    fileName = input("Enter file name : ")
    c = os.path.getsize(fileName)
    CHUNK_SIZE = math.ceil(math.ceil(c) / 5)
    index = 1
    with open(fileName, 'rb') as infile:
        chunk = infile.read(int(CHUNK_SIZE))
        while chunk:
            chunkname = "files/" + fileName + '_' + str(index)
            with open(chunkname, 'wb+') as chunk_file:
                chunk_file.write(chunk)
            index += 1
            chunk = infile.read(int(CHUNK_SIZE))
    chunk_file.close()
    print("Files are ready to share")
    server()