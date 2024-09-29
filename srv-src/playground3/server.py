import socket
import threading
import time

a = 0
def handle_client_waw_client(conn, addr,id):
    misses = 0
    # recv message
    recieved = 0 
    with open("output"+ str(a) + ".waw","wb") as out:
        while True:
            try:
                message = conn.recv(4096)
                if not message:
                    break
                out.write(message)
                recieved += 1
            except BrokenPipeError: # for when also ending the connection
                break
            except ConnectionResetError: # for when abruyptly closing
                break

            # time.sleep(1)

    print("rcv - ",recieved)
    conn.close()


host = '0.0.0.0'
port = 9999

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # solution for "[Error 89] Address already in use". Use before bind()
# s.setblocking(False)
s.bind((host, port))
s.listen(6)

all_threads = []
try:
    while True:

        res = False
        if len(all_threads) > 0:
            for  t in all_threads:
                if t.is_alive():
                    res = True
        else:
            res = True
        if res:
            print("Waiting for client")
            try:
                conn, addr = s.accept()
                print("Client:", addr)
                # t = threading.Thread(target=handle_client, args=(conn, addr))
                t = threading.Thread(target=handle_client_waw_client, args=(conn, addr, a))
                a+=1
                t.start()
                all_threads.append(t)
            except ConnectionRefusedError: # when using it with non blocking sockets
                time.sleep(1)
        else: 
            break

except KeyboardInterrupt:
    print("Stopped by Ctrl+C")
finally:
    if s:
        s.close()
    for t in all_threads:
        t.join()
