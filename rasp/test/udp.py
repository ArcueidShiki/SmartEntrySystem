from picamera2.outputs import FileOutput, Picamera2
from picamera2.encoders import Encoder
import time
import socket

picam2 = Picamera2()
config = picam2.create_video_configuration(raw={}, encode="raw")
picam2.configure(config)
encoder = Encoder()
picam2.start_recording(encoder, "test.raw")

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.connect(("172.20.10.11", 8000))
    stream = sock.makefile("wb")
    output = FileOutput(stream)

while True:
    try:
        picam2.capture(output)
    except KeyboardInterrupt:
        picam2.stop_recording()
        break