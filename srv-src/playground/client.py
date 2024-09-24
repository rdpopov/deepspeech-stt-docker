import socket
import threading
import sys
import numpy as np
import time
from scipy.io import wavfile

# --- main ---

time.sleep(1)
host = '0.0.0.0'
port = 9999


print("Connected to the server")

# def client(host, port):
#     with socket.socket() as s:
#         try:
#             s.connect((host, port))
#         except ConnectionRefusedError:
#             time.sleep(1)


#         s.setblocking(False)
#         for i in range(10):

#             if (i%2 == 0):
#                 message = "Hello from " + str(sys.argv[1]) + " " + str(i)
#                 message = message.encode()
#                 s.send(message)

#             try:
#                 message = s.recv(1024)
#                 message = message.decode()
#                 print('client recv:', message)

#             except BlockingIOError:
#                 pass
#             time.sleep(0.01)

def client_waw(host, port):
    print("HENLO")
    sn = 0
    with socket.socket() as s:
        try:
            s.connect((host, port))
        except ConnectionRefusedError:
            time.sleep(1)

        s.setblocking(False)
        samplerate, data = wavfile.read('./ImperialMarch60.wav', mmap=True) 
        mx = len(data)
        n = 0
        while n + 4096 < mx:
            try:
                s.send(data[n:(n+4096)])
                sn += 1
                n += 4096
            except BlockingIOError:
                pass
            time.sleep(0.01)
        try:
            s.send(data[n:mx])
        except BlockingIOError:
            pass
        time.sleep(0.01)

        print("File Sent thread 1", str(sys.argv[1]), sn)
        s.shutdown(socket.SHUT_RDWR)


try:
    t = threading.Thread(target=client_waw, args=(host, port))
    t.start()
    t.join()
    print("exit")
except:
    exit(1)
