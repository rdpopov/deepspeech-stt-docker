import pyaudio

config = {
    "web": {
        "ports_range": list(range(5000, 5004)),
        "chunk_size": 2048,
        "refused_connections": 1,
        "default_port": 4999,
    },
    "audio": {
        "format": pyaudio.paInt16,
        "rate": 44100,
        "channels": 1,
    }
}  # move this int omodule for time being
