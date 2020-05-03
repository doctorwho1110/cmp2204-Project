import socket
import json
import time
import os
from os.path import isfile,join


def announcing(ip,dict_to_json):

    try:
        UDPAnnouncerSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        UDPAnnouncerSocket.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
        UDPAnnouncerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except socket.error as e:
        print ("Caught exception socket.error : %s" % e)
    message = json.dumps(dict_to_json).encode()
    while True:
        UDPAnnouncerSocket.sendto(message,('<broadcast>',5000))
        print("Send.")
        time.sleep(60)



def main():
    AnnouncerSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    MyIp = socket.gethostbyname(socket.gethostname()).split(".")
    MyIp = "{}.{}.{}.255'".format(MyIp[0],MyIp[1],MyIp[2])
    AnnouncerSocket.close()
    username = input("Please enter a Username: ")
    directoryOfFiles = "./p2pfiles/"
    usersInformation_Json = {"username":username,"files":[f for f in os.listdir(directoryOfFiles) if isfile(join(directoryOfFiles,f))]}
    announcing(MyIp,usersInformation_Json)

if __name__ == "__main__":
    main()
