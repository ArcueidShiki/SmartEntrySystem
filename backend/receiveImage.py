import socket

def receive_image(save_path, host='0.0.0.0', port=12345):
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the address and port
    server_socket.bind((host, port))

    # Start listening for incoming connections
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}, waiting for image...")

    # Accept a connection
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    try:
        # Receive the image size first
        image_size = int.from_bytes(client_socket.recv(4), 'big')

        # Receive the image data
        image_data = b''
        while len(image_data) < image_size:
            packet = client_socket.recv(4096)
            if not packet:
                break
            image_data += packet

        # Save the received image to the specified path
        with open(save_path, 'wb') as image_file:
            image_file.write(image_data)
        
        print("Image received and saved successfully")

    except Exception as e:
        print(f"Failed to receive image: {e}")

    finally:
        # Close the connection
        client_socket.close()

if __name__ == "__main__":
    save_path = "./static/images/image.jpg"  # Replace with the path where you want to save the image
    receive_image(save_path)