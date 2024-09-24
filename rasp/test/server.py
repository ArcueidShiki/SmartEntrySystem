import threading
import time
import json
import socket
import struct
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
from threading import Condition
import io
import smbus

bus = smbus.SMBus(1)
mlx99614_address = 0x5A
BACKEND_IP = "172.20.10.11"
BACKEND_PORT = 8000
# Set up the socket connection
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((BACKEND_IP, BACKEND_PORT))

picam2 = Picamera2()
config = picam2.create_preview_configuration(main = {"size":(640, 480), "format":"RGB888"})
picam2.configure(config)
picam2.start()
# class StreamingOutput(io.BufferedIOBase):
#     def __init__(self):
#         self.frame = None
#         self.condition = Condition()

#     def write(self, buf):
#         with self.condition:
#             self.frame = buf
#             slef.condition.notify_all()

# class StreamingServer(socketserver.ThreadingMixin, server.HTTPServer):
#     allow_reuse_address = True
#     daemon_threas = True

def send_video_frame():
    try:
        while True:
            picam2.capture_file("image.jpg")
            # Open the image file
            with open("image.jpg", 'rb') as image_file:
                # Read the image data
                image_data = image_file.read()
                # Send the image size first
                client_socket.sendall(len(image_data).to_bytes(4, 'big'))
                # Send the image data
                client_socket.sendall(image_data)
                print("Image sent successfully")
    except Exception as e:
        print(f"Failed to send image: {e}")

    finally:
        # Close the connection
        picam2.stop()
        client_socket.close()
    # # Initialize the PiCamera
    # with Picamera2() as camera:
    #     camera.resolution = (640, 480)  # Set the resolution
    #     camera.framerate = 30  # Set the framerate
        
    #     # Use a stream to capture frames
    #     stream = io.BytesIO()

    #     # Start capturing frames
    #     for frame in camera.capture_continuous(stream, format='rgb', use_video_port=True):
    #         # Get the frame data (raw RGB bytes)
    #         frame_data = stream.getvalue()
            
    #         # Send the size of the frame first (as 4 bytes)
    #         frame_size = len(frame_data)
            # client_socket.sendall(struct.pack(">L", frame_size))
            
    #         # Send the frame data
    #         client_socket.sendall(frame_data)
            
    #         # Clear the stream for the next frame
    #         stream.seek(0)
    #         stream.truncate()

    #         # Introduce delay for desired framerate (e.g., 1 frame per second)
    #         time.sleep(1)


# def send_data_to_backend(data):
#     try:
#         client_socket.sendall(json.dumps(data).encode('utf-8'))
#     except Exception as e:
#         print(e)
#     finally:
#         print()
    

# def start_control_command_server():
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
#         server_socket.bind((BACKEND_IP, BACKEND_PORT))
#         server_socket.listen(1)
#         while True:
#             client_socket, _ = server_socket.accept()
#             command = client_socket.recv(1024).decode('utf-8')
#             process_control_command(command)

def video_stream_thread():
    # This function handles video stream transmission
    while True:
        # Capture and send video frames (MJPEG or RTSP)
        send_video_frame()
        time.sleep(1)  # Send every second

# def read_temperature():
#     temp = bus.read_word_data(mlx99614_address, 0x07)
#     return temp * 0.02 - 273.15

# def temp_data_thread():
#     # This function sends sensor data, status code, and message
#     while True:
#         temp_data = read_temperature()
#         # status_code = get_status_code()
#         # message_string = get_message_string()
#         data = {
#             "temp_data": temp_data,
#             "status_code": 200,
#             # "message": message_string
#         }
#         send_data_to_backend(data)
#         time.sleep(1)  # Send every second

# def control_command_listener_thread():
#     # This function listens for control commands (like servo angles)
#     start_control_command_server()

# Main function
if __name__ == "__main__":
    # Create threads for different tasks
    video_thread = threading.Thread(target=video_stream_thread)
    # sensor_thread = threading.Thread(target=temp_data_thread)
    # control_thread = threading.Thread(target=control_command_listener_thread)

    # Start all threads
    video_thread.start()
    # sensor_thread.start()
    # control_thread.start()

    # Join threads to keep the main process alive
    video_thread.join()
    # sensor_thread.join()
    # control_thread.join()
    picam2.stop()
    client_socket.close()
