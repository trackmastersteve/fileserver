#!/usr/bin/env python3
#
# fileServerClient.py
#
import socket

def main():
    host = '127.0.0.1'
    port = 4444

    s = socket.socket()
    s.connect((host, port))

    filename = input("Filename: ")
    if filename != 'q':
        s.send(bytes(filename, "UTF-8"))
        data = s.recv(1024).decode("UTF-8")
        if data[:6] == 'EXISTS':
            filesize = int(data[6:])
            message = input("File Exists. " + str(filesize) + "Bytes, Download? (Y/N)")
            if message == 'Y':
                s.send(bytes('OK', "UTF-8"))
                f = open('arm0red_'+filename, 'wb')
                data = s.recv(1024)
                totalRecv = len(data)
                f.write(data)
                while totalRecv < filesize:
                    data = s.recv(1024)
                    totalRecv += len(data)
                    f.write(data)
                    print("{0:.2f}".format((totalRecv/float(filesize))*100) + "% Done.")
                print("Download complete!")

        else:
            print("File does not exist!")

    s.close()

main()