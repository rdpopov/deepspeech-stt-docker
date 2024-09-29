import socket
import threading
import sys
import numpy as np
import time
from scipy.io import wavfile
from scipy.signal import resample
import socket
import sounddevice as sd
import numpy as np

# https://chatgpt.com/share/66f9d9d8-13a0-800f-9450-6438b6b75a72
# https://chatgpt.com/share/66f9d9d8-13a0-800f-9450-6438b6b75a72

# --- main ---

## move those in a spearate z
time.sleep(1)
host = '0.0.0.0'
port = 9999
fl = './ImperialMarch60.wav'

sample_rate = 44100  # Sample rate must match the sender
channels = 1  # Mono audio
blocksize = 1024 

def curry_socket(s):
    def audio_callback(indata, frames, time, status):
        data = indata.flatten().tobytes()
        s.send(data)
    return audio_callback

def client_microphone(host, port):
    print("HENLO")
    sn = 0
    secs  = 10
    with socket.socket() as s:

        try:
            s.connect((host, port))
        except ConnectionRefusedError:
            time.sleep(1)

        s.setblocking(False)
        callback = curry_socket(s)

        with sd.InputStream(samplerate=sample_rate, channels=channels, blocksize=blocksize, callback=callback):
            # while True:
            while secs> 0:
                # secs-=1
                sd.sleep(1000)  # Keep the stream alive
        print("File Sent thread 1", str(sys.argv[1]), sn)
        s.shutdown(socket.SHUT_RDWR)

try:
    t = threading.Thread(target=client_microphone, args=(host, port))
    t.start()
    t.join()
    print("exit")
except:
    exit(1)
