import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()

userdata = [["admin", "21232f297a57a5a743894a0e4a801fc3"], ["oliver", "098f6bcd4621d373cade4e832627b4f6"]]

def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print("accepted connection from", addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
            print("closing connection to", data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            usrpwd = data.outb.decode("utf-8").split(" ")
            echo = b""
            if len(usrpwd) == 2:
                for u in range(len(userdata)):
                    if usrpwd[0]==userdata[u][0]:
                        if usrpwd[1]==userdata[u][1]:
                            print("Logged in as " + usrpwd[0])
                            echo = b"Valid credentials"
                            break
                        else:
                            print("Access denied")
                            echo = b"Username and/or password are not in registered in the database"
                            break
                sent = sock.send(echo)  # Should be ready to write


if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print("listening on", (host, port))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()
