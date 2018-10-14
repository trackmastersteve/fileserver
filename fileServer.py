#!/user/bin/env python3
#
# fileServer.py
#
import socket
import threading
import os

def retrieveFile(name, sock):
    filename = sock.recv(1024).decode("UTF-8")
    if os.path.isfile(filename):
        sock.send(bytes("EXISTS " + str(os.path.getsize(filename)) +"\n", "UTF-8"))
        userResponse = sock.recv(1024).decode("UTF-8")
        if userResponse[:2] == 'OK':
            with open(filename, 'rb') as f:
                bytesToSend = f.read(1024)
                sock.send(bytesToSend)
                while bytesToSend != "":
                    bytesToSend = f.read(1024)
                    sock.send(bytesToSend)

    else:
        sock.send(bytes("ERR" +"\n", "UTF-8"))

    sock.close()

def main():
    host = '127.0.0.1'
    port = 4444

    s = socket.socket()
    s.bind((host, port))

    s.listen(5)

    print("Server Started.")
    while True:
        c, addr = s.accept()
        print("Client connected ip: " + str(addr))
        t = threading.Thread(target=retrieveFile, args=("retreiveThread", c))
        t.start()

    s.close()

main()