import socket

def send_servo_command(angle, server_ip, server_port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_ip, server_port))
        client_socket.sendall(str(angle).encode())
        response = client_socket.recv(1024).decode()
        print(f"Response from server: {response}")
    except Exception as e:
        print(f"Failed to send command: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    server_ip = "172.20.10.2"  # Replace with your Raspberry Pi's IP address
    angle = 90  # Set the desired angle
    send_servo_command(angle, server_ip)