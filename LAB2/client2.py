import socket
import threading
import sys
import os

IP = socket.gethostbyname(socket.gethostname())
PORT = 5567
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "DISCONNECT!"

def recv_msg(client):
    connected = True

    while connected:
        try:
            msg = client.recv(1024).decode(FORMAT)
        except OSError:
            return

        if msg == DISCONNECT_MESSAGE:
            connected = False

        if msg:
            print(f"\r[SERVER] {msg}")
            print("> ", end="")
            sys.stdout.flush()
    client.close()
    os.exit(0)


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    print(f'[CONNECTED] Connected to server on {IP} : {PORT}')

    thread = threading.Thread(target = recv_msg, args = (client,))
    thread.start()

    connected = True

    while connected:
        msg = input('> ')
        client.send(msg.encode(FORMAT))

        if msg == DISCONNECT_MESSAGE:
            connected = False

        msg = client.recv(1024).decode(FORMAT)
        print(f"[SERVER]... {msg}")

    print(f'[DISCONNECTED].. Disconnected from {IP} : {PORT}')
    client.close()

if __name__ == '__main__':
    main()