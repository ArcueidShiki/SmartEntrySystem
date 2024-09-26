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

app = Flask(__name__)
model = load_model("mask_detector.keras")
prototxtPath = "face_detector/deploy.prototxt"
weightsPath = "face_detector/res10_300x300_ssd_iter_140000.caffemodel"
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

@app.route('/detect_mask', methods=['POST'])
def detect_mask():
    # Receive the frame size
    message_size = struct.calcsize("L")
    data = request.data
    frame_size = struct.unpack("L", data[:message_size])[0]
    
    # Receive the frame data
    frame_data = data[message_size:message_size + frame_size]
    frame = np.frombuffer(frame_data, dtype=np.uint8).reshape((480, 640, 3))

    # Process the frame using the mask detection model
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))
    faceNet.setInput(blob)
    detections = faceNet.forward()

    faces = []
    locs = []
    preds = []

    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            (endX, endY) = (min(w, endX), min(h, endY))
            face = frame[startY:endY, startX:endX]
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            face = cv2.resize(face, (224, 224))
            face = img_to_array(face)
            face = preprocess_input(face)
            faces.append(face)
            locs.append((startX, startY, endX, endY))

    if len(faces) > 0:
        faces = np.array(faces, dtype="float32")
        preds = model.predict(faces, batch_size=32)

    results = [{"loc": loc, "pred": pred} for loc, pred in zip(locs, preds)]
    return jsonify(results)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)