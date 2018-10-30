import socket
import sys


def receive():
    HOST = "127.0.0.1"
    PORT = 65432

    #inputStr = sys.argv[1]
    inputStr = ""
    for i in range(1, 1000):
        inputStr += "Word "
    inputStr += "Word"
    bytesize = len(inputStr.encode('utf-8'))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(inputStr.encode())
        data = s.recv(bytesize)
    print("Received", repr(data.decode()))


if __name__ == "__main__":
    receive()
