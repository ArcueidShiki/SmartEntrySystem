from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
# from imutils.video import VideoStream
from flask import Flask, render_template, Response, request
import numpy as np
import imutils
import time
import os
import cv2
import socket
import struct
import requests
# netsh advfirewall set allprofiles state off
app = Flask(__name__)
model = load_model("mask_detector.keras")
prototxtPath = "face_detector/deploy.prototxt"
weightsPath = "face_detector/res10_300x300_ssd_iter_140000.caffemodel"
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 8000))
RSP_IP = "172.20.10.4"

def detect_and_predict_mask(frame, faceNet, maskNet):
    # Grab the dimensions of the frame and then construct a blob
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))
    # pass blob through the network and obtain the face detections
    faceNet.setInput(blob)
    detections = faceNet.forward()

    # initialize our list of faces, their corresponding lcoations,
    # and the list of predicitons from our face mask network
    faces = []
    locs = []
    preds = []

    for i in range(0, detections.shape[2]):
        # extract the confidence (i.e. probability) associated with the detection
        confidence = detections[0, 0, i, 2]
        # filter out weak detections by ensuring the confidence is greater thatn the minimum confidence
        if confidence > 0.5:
            # compute the (x,y)-coordinates of the bounding box for the object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            # ensure the bounding boxed fall within the dimensionss of the frame
            (endX, endY) = (min(w, endX), min(h, endY))
            # extract the face ROI, convert it from BGR to RGB channel
            # ordering, resize it to 224x224, and preprocess it
            face = frame[startY:endY, startX:endX]
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            face = cv2.resize(face, (224, 224))
            face = img_to_array(face)
            face = preprocess_input(face)
            # add the face and bounding boxed to their respective lists
            faces.append(face)
            locs.append((startX, startY, endX, endY))
        
    # only make a predictionss if at least one face was detected
    if len(faces) > 0:
        faces = np.array(faces, dtype="float32")
        preds = maskNet.predict(faces, batch_size=32)
    # return a 2-tuple of the face locations and their corresponding locations
    return (locs, preds)
    
def generate_frames():
    server_socket.listen(1)
    print("Waiting for connection from Raspberry Pi...")
    client_socket, addr = server_socket.accept()
    while True:
        try:
            image_size = int.from_bytes(client_socket.recv(4), 'big')
            # Receive the image data
            image_data = b''
            while len(image_data) < image_size:
                packet = client_socket.recv(4096)
                if not packet:
                    break
                image_data += packet

            # Save the received image to the specified path
            with open("image.jpg", 'wb') as image_file:
                image_file.write(image_data)
            
            frame = cv2.imread("image.jpg")
            if frame is None or frame.size == 0:
                print("Error: Frame not captured correctly")
                continue
            frame = imutils.resize(frame, width=400)
            (locs, preds) = detect_and_predict_mask(frame, faceNet, model)
            # Loop over the detected face locations and their corresponding locations
            for (box, pred) in zip(locs, preds):
                (startX, startY, endX, endY) = box
                (mask, withoutMask) = pred
                # Determin the class label and color we'll sue to draw the bounding box and text
                label = "Mask" if mask > withoutMask else "No Mask"
                color = (0, 255, 0) if label == "Mask" else (0, 0, 255)
                # Include the probability in the label
                label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)
                # Display the label and bounding box rectangle on the output frame
                cv2.putText(frame, label, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
                cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            print(f"Error in receiving video frame: {e}")
            client_socket.close()
            client_socket, addr = server_socket.accept()

def generate_single_frame():
    try:
        server_socket.listen(1)
        print("Waiting for connection from Raspberry Pi...")
        client_socket, addr = server_socket.accept()
        print(f"Connected to {addr}")
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
        with open("image.jpg", 'wb') as image_file:
            image_file.write(image_data)
        
        frame = cv2.imread("image.jpg")
        # Detect faces and predict mask/no mask
        locs, preds = detect_and_predict_mask(frame, faceNet, model)

        # Loop over the detected face locations and their corresponding locations
        for (box, pred) in zip(locs, preds):
            (startX, startY, endX, endY) = box
            (mask, withoutMask) = pred
            # Determine the class label and color we'll use to draw the bounding box and text
            label = "Mask" if mask > withoutMask else "No Mask"
            color = (0, 255, 0) if label == "Mask" else (0, 0, 255)
            # Include the probability in the label
            label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)
            # Display the label and bounding box rectangle on the output frame
            cv2.putText(frame, label, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

        # Encode the frame in JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        return frame

    except Exception as e:
        print(f"Error in processing single frame: {e}")
        return None
    finally:
        client_socket.close()
        # server_socket.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/image_feed')
def image_feed():
    frame = generate_single_frame()
    if frame is None:
        return Response(status=500)
    return Response(frame, mimetype='image/jpeg')

if __name__ == "__main__":
    app.run(host='172.20.10.11', port=5000)