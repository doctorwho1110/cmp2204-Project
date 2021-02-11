import socket
import json
import sys
import os


files = {}
bufferSize = 4096


def listenerIp():
    ListenerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ListenerSocket.connect(("1.1.1.1", 1))
    ip = ListenerSocket.getsockname()[0].split(".")
    MyIp = ip[0] + "." + ip[1] + "." + ip[2] + ".255"

    ListenerSocket.close()
    return MyIp


def create_userfile(info, ip):
    if ip != listenerIp():
        data = json.loads(info.decode("utf-8"))
        if data["username"] is None:
            pass
        for file in data["files"]:
            files[file] = ip
        for key in files:
            print("Username" + data["username"])
            print("File: " + key)
            print("IP : " + files[key])
        with open("store.txt", "w") as f:
            f.write(json.dumps(files))


def listening(adres):
    print("Service Listening...")

    try:
        UDPListenerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        UDPListenerSocket.bind(adres)
    except socket.error as e:
        print("Caught exception socket.error : %s" % e)
    while True:
        info, address = UDPListenerSocket.recvfrom(bufferSize)

        ip = address[0]
        create_userfile(info, ip)


def main():
    ip = listenerIp()

    print(ip)
    if os.name == 'nt':
        print("Running On Windows")
        listening((listenerIp(), 5000))
    else:
        print("Running On Unix-Like Systems")
        listening((ip, 5000))


if __name__ == "__main__":
    main()