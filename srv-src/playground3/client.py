import socket
import threading
import sys
import numpy as np
import time
from scipy.io import wavfile
from scipy.signal import resample

# --- main ---

## move those in a spearate z
time.sleep(1)
host = '0.0.0.0'
port = 9999
fl = './ImperialMarch60.wav'

desired_sample_rate = 44100

def resample_file(data, sample_rate, new_sample_rate ): 
    number_of_samples = round(len(data) * float(new_sample_rate) / sample_rate)
    return resample(data, number_of_samples)

def client_waw(host, port):
    print("HENLO")
    sn = 0
    with socket.socket() as s:
        try:
            s.connect((host, port))
        except ConnectionRefusedError:
            time.sleep(1)

        s.setblocking(False)
        samplerate, data = wavfile.read(fl, mmap=True)
        print(samplerate,desired_sample_rate,desired_sample_rate/samplerate)
        data = resample_file(data,samplerate, desired_sample_rate)
        mx = len(data)
        n = 0
        # TODO: make this into a generator
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
