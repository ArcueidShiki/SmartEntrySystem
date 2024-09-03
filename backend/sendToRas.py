import socket

def send_message(message, server_ip, server_port=1234):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((server_ip, server_port))
        print(f"Connected to server at {server_ip}:{server_port}")

        # Send the message
        client_socket.send(message.encode('utf-8'))

        # Receive a response (optional)
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Server response: {response}")

    except Exception as e:
        print(f"Failed to connect or send message: {e}")
    
    finally:
        # Close the connection
        client_socket.close()

if __name__ == "__main__":
    server_ip = "172.20.10.2"  # Replace with your Raspberry Pi's IP address
    message = "Hello from Mac"
    send_message(message, server_ip)