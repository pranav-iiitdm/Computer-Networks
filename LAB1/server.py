import socket

s = socket.socket()
print("Socket Created")

port = 12357

s.bind(('', port))
print("socket is bind to %s", port)

s.listen(5) 

while True:
    c, addr = s.accept()
    print("Connected to ", addr)

    c.send("hello from pranav".encode())

    c.close()

    break