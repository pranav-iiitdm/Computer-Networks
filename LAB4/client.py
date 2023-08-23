import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 5568
ADDR = (IP, PORT)
FORMAT = "utf-8"
DISCONNECT_MSG = "DISCONNECT!"

def handle_server(client):
    file_name = client.recv(1024).decode(FORMAT)
    fp = open(file_name, 'w')
    client.send('[CLIENT] File Name Received ... '.encode(FORMAT))
    data = client.recv(1024).decode(FORMAT)
    fp.write(data)
    client.send('[CLIENT] Data Received ...'.encode(FORMAT))
    fp.close()

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    print(f'[CONNECTED] Connected to {IP} : {PORT} ...')

    thread = threading.Thread(target = handle_server, args = (client, ))
    thread.start()

    file_name = input('> Enter the File Name : ')
    client.send(file_name.encode(FORMAT))
    msg = client.recv(1024).decode(FORMAT)
    print(msg)
    fp = open(file_name, 'r')
    data = fp.read()
    client.send(data.encode(FORMAT))
    msg1 = client.recv(1024).decode(FORMAT)
    print(msg1)

    fp.close()

    client.close()

if __name__ == '__main__':
    main()