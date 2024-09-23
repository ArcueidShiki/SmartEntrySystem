import socket

def start_server(host='0.0.0.0', port=1234):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server_socket.bind((host, port))
    
    server_socket.listen(1)
    print(f"Server started on {host}:{port}, waiting for connections..")
    
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        
        message = client_socket.recv(1024).decode('utf-8')
        print(f"Received message: {message}")
        
        client_socket.send("Message received by Raspberry Pi".encode('utf-8'))
        
        client_socket.close()

if __name__ == "__main__":
    start_server()