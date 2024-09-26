import socket
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
import time

#initiate the camera

picam2 = Picamera2()

#configure the camera for preview and capture
camera_config = picam2.create_still_configuration()
picam2.configure(camera_config)

#start the camera

picam2.start()

#Capture the image

print("capturing image... ")

picam2.capture_file("image.jpg")

print("Image saved as 'image.jpg'")

# Stop the camera
picam2.stop()

def send_image(image_path, server_ip, server_port=8000):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((server_ip, server_port))
        print(f"Connected to server at {server_ip}:{server_port}")

        # Open the image file
        with open(image_path, 'rb') as image_file:
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
        client_socket.close()

if __name__ == "__main__":
    server_ip = "172.20.10.11"  # Replace with your Mac's IP address
    image_path = "image.jpg"  # Replace
    send_image(image_path, server_ip)