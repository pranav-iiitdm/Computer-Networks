import socket

s = socket.socket()
port = 12360

s.connect(('172.16.7.180', port))

print(s.recv(1024).decode())

s.close()