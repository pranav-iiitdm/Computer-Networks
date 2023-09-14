import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
# '172.16.19.94'
PORT = 5570
ADDR = (IP, PORT)
FORMAT = "utf-8"
DISCONNECT_MSG = "DISCONNECT!"

def handle_client(conn, addr):
    print(f'[NEW CONNECTION] {addr}:{conn} connected...')

    file_name = conn.recv(1024).decode(FORMAT)
    fp = open(file_name, 'w')
    conn.send('[SERVER] File Name Received ... '.encode(FORMAT))
    data = conn.recv(1024).decode(FORMAT)
    fp.write(data)
    conn.send('[SERVER] Data Received ...'.encode(FORMAT))
    fp.close()

    conn.close()

def main():
    print('[SERVER] Starting...')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind(ADDR)
    server.listen()

    print(f'[SERVER] Listening on port : {PORT}')

    while True:
        conn, addr = server.accept()

        thread = threading.Thread(target = handle_client, args = (conn, addr))
        thread.start()

        file_name = input('> Enter the File Name : ')
        conn.send(file_name.encode(FORMAT))
        msg = conn.recv(1024).decode(FORMAT)
        print(msg)
        fp = open(file_name, 'r')
        data = fp.read()
        conn.send(data.encode(FORMAT))
        msg1 = conn.recv(1024).decode(FORMAT)
        print(msg1)

if __name__ == '__main__':
    main()