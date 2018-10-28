import socket


def prepareReply():
    HOST = "127.0.0.1"
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()

        with conn:
            print("Connected by: ", addr)
            while True:
                data = conn.recv(5000)
                if not data:
                    break
                #response = prepareReply(data)
                countWords = len(str(data).split(" "))
                print("Amount of words received: ", countWords)
                conn.sendall(data)

def run():
    prepareReply()


if __name__ == "__main__":
    run()
