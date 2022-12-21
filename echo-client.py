#!/usr/bin/env python3

import socket
import base64

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    with open("link-store.png", "rb") as image:
        b64string = base64.b64encode(image.read())
        s.sendall(b64string)
    data = s.recv(1024)

print('Received', repr(data))