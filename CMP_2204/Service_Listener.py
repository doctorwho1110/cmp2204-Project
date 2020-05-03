import socket
import json
import sys

files = {}
bufferSize = 2048


def listenerIp():
    ListenerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    MyIp = socket.gethostbyname(socket.gethostname()).split(".")
    MyIp = "{}.{}.{}.255'".format(MyIp[0], MyIp[1], MyIp[2])
    ListenerSocket.close()
    return MyIp


def listening(adres):
    print("Service Listening...")
    try:
        UDPListenerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        UDPListenerSocket.bind(adres)
    except socket.error as e:
        print("Caught exception socket.error : %s" % e)
    while True:
        info, address = UDPListenerSocket.recvfrom(bufferSize)
        ip = address[0], portL = address[1]
        # msg = b"Listener listening..."
        # UDPListenerSocket.sendto(msg,(ip,port))

        if ip != listenerIp():
            data = json.loads(str(info.decode()))
            if data["username"] is None:
                continue
            for file in data["files"]:
                files[file] = ip
            for key in files:
                print("Username" + data["username"])
                print("File: " + key)
                print("IP : " + files[key])
            with open("store.txt", "w") as f:
                f.write(json.dumps(files))


def main():
    ip = listenerIp()
    listening((ip, 5000))


if __name__ == "__main__":
    main()