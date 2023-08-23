import socket
import threading
import sys

IP = socket.gethostbyname(socket.gethostname())
PORT = 5569
ADDR = (IP, PORT)
FORMAT = "utf-8"
DISCONNECT_MSG = "DISCONNECT!"

conn_clients = []

def handle_client(conn, addr):
    print(f'\r[NEW CONNECTION] {addr} Connected!')

    for client in conn_clients:
        if client['addr'] != addr:
            conn.send(f"[EXISTING CONNECTION]... {client['addr'][0]} {client['addr'][1]} connected to the server".encode(FORMAT))

    for client in conn_clients:
        if client['addr'] != addr:
            client['conn'].send(f"\n[NEW CONNECTION]...{addr[0]} {addr[1]}".encode(FORMAT))

    connected = True

    while connected:
        msg = conn.recv(1024).decode(FORMAT)
        
        if msg == DISCONNECT_MSG:
            connected = False
            for client in conn_clients:
                if client['addr'] != addr:
                    client['conn'].send(f"\n[DISCONNECTED]...{addr[0]} {addr[1]} from the server".encode(FORMAT))
            for client in conn_clients:
                if client["addr"] == addr:
                    conn_clients.remove(client)
                    break
            else:
                print(f'[ERROR] Cannot Disconnect {addr}')
        else:
            to_addr = (msg.split(':')[0], int(msg.split(':')[1]))
            msg = (msg.split(':')[2])
            msg = f"{to_addr} : {msg}"

            for client in conn_clients:
                if client['addr'] == to_addr:
                    try:
                        client["conn"].send(msg.encode(FORMAT))
                        conn.send("Message sent".encode(FORMAT))
                    except BrokenPipeError:
                        print(f"[ERROR] Cannot send message to {to_addr}")
                    break

    conn.close()
                

def main():
    print(f'[SERVER] Starting... ')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind(ADDR)

    server.listen()
    print(f'[SERVER] Listening on port : {PORT} ...')

    while True:
        conn, addr = server.accept()
        conn_clients.append({"conn" : conn, "addr" : addr})

        thread = threading.Thread(target = handle_client,args = (conn, addr))
        thread.start()

        print(f'\r[ACTIVE CONNECTIONS] {threading.active_count() - 1}')

if __name__ == '__main__':
    main()