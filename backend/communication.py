import socket

def start_server(host='0.0.0.0', port=12345):
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the address and port
    server_socket.bind((host, port))

    # Start listening for incoming connections
    server_socket.listen(1)
    print(f"Server started on {host}:{port}, waiting for connections...")

    while True:
        # Accept a connection
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        # Receive the message
        message = client_socket.recv(1024).decode('utf-8')
        print(f"Received message: {message}")

        # Send a response back to the client (optional)
        client_socket.send("Message received".encode('utf-8'))

        # Close the connection
        client_socket.close()

if __name__ == "__main__":
    start_server()