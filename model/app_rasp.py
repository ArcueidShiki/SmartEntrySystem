import socket
import struct
import numpy as np

def receive_and_process_video(frame_processor, host='0.0.0.0', port=12345):
    # Set up the socket server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        
        try:
            while True:
                # Receive the size of the frame (4 bytes, big-endian)
                frame_size_data = client_socket.recv(4)
                if not frame_size_data:
                    break

                frame_size = struct.unpack(">L", frame_size_data)[0]

                # Receive the frame data
                frame_data = b''
                while len(frame_data) < frame_size:
                    packet = client_socket.recv(4096)
                    if not packet:
                        break
                    frame_data += packet
                
                # Reshape the raw RGB frame into the correct format (640x480 resolution, RGB format)
                frame = np.frombuffer(frame_data, dtype=np.uint8).reshape((480, 640, 3))

                # Call the AI model for mask detection
                locs, preds = frame_processor(frame)

                # (Optional) You can send the prediction results back to the client if needed

        except Exception as e:
            print(f"Error in receiving video frame: {e}")
        finally:
            client_socket.close()

def frame_processor(frame):
    # Load your pre-trained AI models (faceNet and mask detection model)
    faceNet = ...  # Load faceNet model
    model = ...    # Load mask detection model

    # Call the detect_and_predict_mask function on the frame
    locs, preds = detect_and_predict_mask(frame, faceNet, model)
    
    # Return locations and predictions
    return locs, preds

if __name__ == "__main__":
    receive_and_process_video(frame_processor)
