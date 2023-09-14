# File Transfer: SERVER
# The server performs the following functions:
# Create a TCP socket.
# Bind the IP address and PORT to the server socket.
# Listening for the clients.
# Accept the connection from the client.
# Receive the filename from the client and create a text file.
# Send a response back to the client.
# Receive the text data from the client.
# Write (save) the data into the text file.
# Send a response message back to the client.
# Close the text file.
# Close the connection.

# FIle Transfer: CLIENT
# The client performs the following functions:
# Create a TCP socket for the client.
# Connect to the server.
# Read the data from the text file.
# Send the filename to the server.
# Receive the response from the server.
# Send the text file data to the server.
# Receive the response from the server.
# Close the file.
# Close the connection.

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
