import json
import subprocess
import socket
import datetime
import platform


def start_socket(ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, 5001))


def create_file(chunk, data, message, ip):
    if len(data) == 0:
        with open("client.txt", "a") as log:
            current_time = datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")
            log.write(current_time + "," + ip + "," + message + "\n")
        chunk.close()


def writing_data(s, count, msg, ipaddress):
    s.send(json.dumps({"filename": msg}).encode())
    chunk = open(msg, "wb")
    while True:
        data = s.recv(4096)
        chunk.write(data)
        # subprocess.run("clear" if platform.system() != "Windows" else "cls")
        # Windowsta problem cikardigi icin de aktive edilmistir
        # Unix-Like sistemlerde aktif hale getirebilir (stabil degil)
        print("[" + str(count) + "/5]" + msg[:-2] + " is downloading.")
        print("Download is complete!")
        create_file(chunk, data, msg, ipaddress)
        break
        return True


def client(ipAddress, message, count):
    start_socket(ipAddress)
    try:
        writing_data(socket.s, count, message, ipAddress)
    except:
        print("Error on download from " + ipAddress)
        return False
    finally:
        socket.socket.close()


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


if __name__ == "__main__":
    main()
