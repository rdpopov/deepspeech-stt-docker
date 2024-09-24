
import socket
import sys
import time

# --- main ---

host = '0.0.0.0'
port = 9999

s = socket.socket()
s.connect((host, port))

print("Connected to the server")

message = "Hello from" + sys.argv[1]
for i in range(100):
    try:
        print('send:', message)
        message = message.encode()
        s.send(message)

        # message = s.recv(1024)
        # message = message.decode()
        # print('recv:', message)
        # time.sleep(1)
    except:
        print("Error")

