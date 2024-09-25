import socket
import struct
import time
import numpy as np
from picamera2 import Picamera2

# Initialize the camera
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
picam2.start()

# Set up the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(1)
print("Server listening on port 8000")

conn, addr = server_socket.accept()
print(f"Connection from {addr}")

while True:
    frame = picam2.capture_array()
    
    # Serialize the frame using numpy
    data = frame.tobytes()
    # Pack the frame size
    message_size = struct.pack("L", len(data))
    # Send the frame size and frame data
    conn.sendall(message_size + data)
    
    time.sleep(0.1)  # Add a small delay to control the frame rate

picam2.stop()
conn.close()
server_socket.close()