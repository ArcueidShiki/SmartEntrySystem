import socket
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
import time

def send_images(image_path, server_ip, server_port=8000):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    picam2 = Picamera2()
    try:
        # Connect to the server
        client_socket.connect((server_ip, server_port))
        print(f"Connected to server at {server_ip}:{server_port}")
        picam2.configure(picam2.create_still_configuration(main={"size": (640, 480)}))
        picam2.start()
        while True:
            print("capturing image... ")
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

    except Exception as e:
        print(f"Failed to send image: {e}")

    finally:
        # Close the connection
        picam2.stop()
        client_socket.close()

if __name__ == "__main__":
    server_ip = "172.20.10.11"  # Replace with your Mac's IP address
    image_path = "image.jpg"  # Replace
    send_images(image_path, server_ip)