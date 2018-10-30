import sys
import socket
import hashlib


HOST = "127.0.0.1"
PORT = 4662

h = hashlib.md5()

if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<name> <password>")
    sys.exit(1)

name, password = sys.argv[1:3]
h.update(password.encode())
msg = name + " " + h.hexdigest()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(msg.encode())
    data = s.recv(1024)
print(repr(data.decode()))
