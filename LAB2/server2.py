import socket
import threading
import sys

IP = socket.gethostbyname(socket.gethostname())
PORT = 5567
ADDR = (IP, PORT)
FORMAT = "utf-8"
DISCONNECT_MSG = "DISCONNECT!"

conn_clients = []

def send_msg():
    while(True):
        addr_input = input('> Enter IP PORT : ')
        addr_input = (addr_input.split()[0], int(addr_input.split()[1]))
        msg = input('> Enter the message : ')

        for client in conn_clients:
            if client["addr"] == addr_input:
                client["conn"].send(msg.encode(FORMAT))
                break
        else:
            print(f'[ERROR] {addr_input} not connected!')

def handle_client(conn, addr):
    print(f'\r[NEW CONNECTION] {addr} Connected!')

    connected = True

    while connected:
        msg = conn.recv(1024).decode(FORMAT)
        if msg == DISCONNECT_MSG:
            connected = False
            for client in conn_clients:
                if client["addr"] == addr:
                    conn_clients.remove(client)
                    break
            else:
                print(f'[ERROR] Cannot Disconnect {addr}')
        print(f'\r {addr} : {msg}')
        print('> Enter IP PORT : ', end="")
        sys.stdout.flush()

        try:
            conn.send("Msg received".encode(FORMAT))
        except BrokenPipeError:
            print(f"[ERROR] Cannot send message to {addr}")
            break

    conn.close()
                

def main():
    print(f'[SERVER] Starting... ')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind(ADDR)

    server.listen()
    print(f'[SERVER] Listening on port : {PORT} ...')

    print(f'[ACTIVE CONNECTIONS] {threading.active_count() - 1}')

    send_thread = threading.Thread(target = send_msg)
    send_thread.start()

    while True:
        conn, addr = server.accept()
        conn_clients.append({"conn" : conn, "addr" : addr})

        thread = threading.Thread(target = handle_client,args = (conn, addr))
        thread.start()

        print(f'\r[ACTIVE CONNECTIONS] {threading.active_count() - 2}')
        print('> Enter IP PORT : ',end="")
        sys.stdout.flush()

if __name__ == '__main__':
    main()