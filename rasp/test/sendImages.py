import socket
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
import time
from time import sleep



def send_images(image_path, server_ip, server_port=8000):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    picam2 = Picamera2()
    picam2.configure(picam2.create_still_configuration(main={"size": (400, 400)}))
    picam2.start()
    client_socket.connect((server_ip, server_port))
    while True:
        try:
            
            print(f"Connected to server at {server_ip}:{server_port}")
            while True:
                picam2.capture_file(image_path)
                print("Image saved as 'image.jpg'")
                # Open the image file
                with open(image_path, 'rb') as image_file:
                    # Read the image data
                    image_data = image_file.read()
                
                # Send the image size first
                client_socket.sendall(len(image_data).to_bytes(4, 'big'))

                # Send the image data
                client_socket.sendall(image_data)
                print("Image sent successfully")
                # maybe this is waiting for a command to continue.
                sleep(1)

        except Exception as e:
            print(f"Failed to send image: {e}")
            print("Try to reconnect")
            client_socket.close()
            client_socket.connect((server_ip, server_port))

if __name__ == "__main__":
    server_ip = "172.20.10.11"  # Replace with your Mac's IP address
    image_path = "image.jpg"  # Replace
    send_images(image_path, server_ip)