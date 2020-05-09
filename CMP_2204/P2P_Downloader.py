import json
import subprocess
import socket
import datetime
import platform


def main():
    while True:
        some = {}
        with open("store.txt", "r") as f:
            val = json.loads(f.readline())
            some.clear()
            for x in val:
                some[x[:-2]] = val[x]
            print("P2P server")
            print("\n")
            for x in some:
                print("File Name = " + x)
                print("IP Address = " + some[x])
            inp = input("Enter File Name To Download=")
            for i in range(1, 6):
                flag = False
                if client(some[inp], inp + "_" + str(i), i) is False:
                    for x in some:
                        if x == inp:
                            if client(some[x], inp + "_" + str(i), i) is True:
                                flag = True
                                break
                else:
                    flag = True
                if flag is False:
                    print("Couldn't download the file")
                    break
            with open(inp, 'wb') as outfile:
                for i in range(1, 6):
                    with open(inp + "_" + str(i), "rb") as infile:
                        outfile.write(infile.read())


def client(ipAddress, message, count):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ipAddress, 5001))
    try:
        sock.send(json.dumps({"filename": message}).encode())
        chunk = open(message, "wb")
        while True:
            data = sock.recv(4096)
            chunk.write(data)
            # subprocess.run("clear" if platform.system() != "Windows" else "cls")
            # Windowsta problem cikardigii icin de aktive edilmistir
            # Unix-Like sistemlerde aktif hale getirebilir (stabil degil)
            print("[" + str(count) + "/5]" + message[:-2] + " is downloading.")
            print("Download is complate!")
            if len(data) == 0:
                with open("client.txt", "a") as log:
                    curr_time = datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")
                    log.write(curr_time + "," + ipAddress + "," + message + "\n")
                chunk.close()
                break
        return True
    except:
        print("Error on download from " + ipAddress)
        return False
    finally:
        sock.close()


if __name__ == "__main__":
    main()
