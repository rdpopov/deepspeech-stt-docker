import shared_config
import socket
import pyaudio
import wave
config = shared_config.config


port_range = config["web"]["ports_range"]

empty_sink = True

p = pyaudio.PyAudio()

class AudioJack():
    def __init__(self, port, stt_context, taken=True):
        self.port = port
        self.taken = taken
        self.rx_frames = []
        self.tx_text = []
        self.chunk = config["web"]["chunk_size"]

    def accept(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()
        self.socket.bind(('0.0.0.0', 5000))
        self.socket.listen(10)
        self.conn, self.address = self.socket.accept()

    def run(self):
        print("Connection from " + self.address[0] + ":" + str(self.address[1]))
        try:
            self.conn.poll(0.03)
            data = self.conn.recv(self.chunk)
            if not empty_sink:
                self.rx_frames.append(data)
        except socket.error as error_message:
            self.finish()
            print("Recieved: ", str(error_message))

    def fininsh(self):
        print("Calling destructor .. ish")
        self.socket.close()
        self.taken = False

    def is_taken(self):
        return self.taken



WAVE_OUTPUT_FILENAME = "output.wav"


rcv = AudioJack(5000, None)
rcv.accept()
while rcv.is_taken():
    rcv.run()

with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
    wf.setnchannels(config['audio']['channels'])
    wf.setsampwidth(p.get_sample_size(config['audio']['format']))
    wf.setframerate(config['audio']['rate'])
    # wf.writeframes(b''.join(frames))
