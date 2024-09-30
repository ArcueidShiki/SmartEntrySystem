import json
import threading
from flask_cors import CORS
from store_data_to_database import store_data

from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
# from imutils.video import VideoStream
from flask import Flask, render_template, Response, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
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

CORS(app)

# Create the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///entries.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/images'

db = SQLAlchemy(app)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    temperature = db.Column(db.Float, nullable=False)
    mask_status = db.Column(db.Boolean, nullable=False)
    image_path = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()



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

            if face is None:
                continue
                # gray_img = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                # cv2.imshow('Stream', gray_img)
            try:
                face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            # if cv2.waitKey(1) == 27:
                # continue
            
                

            # face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            # face = cv2.resize(face, (224, 224))
                face = img_to_array(face)
                face = preprocess_input(face)
                # add the face and bounding boxed to their respective lis
            except Exception as e:
                continue
            finally:
                faces.append(face)
                locs.append((startX, startY, endX, endY))
        
    # only make a predictionss if at least one face was detected
    if len(faces) > 0:
        faces = np.array(faces, dtype="float32")
        preds = maskNet.predict(faces, batch_size=32)
    # return a 2-tuple of the face locations and their corresponding locations
    return (locs, preds)
    

latest_prediction = {
    "label": "",
    "probability": 0.0
}


def generate_frames():
    global latest_prediction
    # camera = cv2.VideoCapture(0)
    while True:
        # success, frame = camera.read()
        # if not success:
        #     print("Error: Frame not captured correctly")
        #     continue
        url = 'http://172.20.10.4:8000/stream.mjpg'
        response = requests.get(url, stream=True)
        bytes = b''
        if response.status_code == 200:
            print("Connection successful! Processing MJPEG stream...")
            for chunk in response.iter_content(chunk_size=1024):
                bytes += chunk
                a = bytes.find(b'\xff\xd8')  # Start of JPEG frame
                b = bytes.find(b'\xff\xd9')  # End of JPEG frame
                if a != -1 and b != -1:
                    jpg = bytes[a:b+2]  # Extract the JPEG image
                    bytes = bytes[b+2:]  # Reset the byte array
                    frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    if frame is None:
                        print("frame is none")
                        continue
                    frame = imutils.resize(frame, width=400)
                    (locs, preds) = detect_and_predict_mask(frame, faceNet, model)
                    for (box, pred) in zip(locs, preds):
                        (startX, startY, endX, endY) = box
                        (mask, withoutMask) = pred
                        label = "Mask" if mask > withoutMask else "No Mask"
                        probability = max(mask, withoutMask) * 100
                        latest_prediction["label"] = label
                        latest_prediction["probability"] = probability
                        label_text = "{}: {:.2f}%".format(label, probability)
                        color = (0, 255, 0) if label == "Mask" else (0, 0, 255)
                        cv2.putText(frame, label_text, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
                        cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
                    ret, buffer = cv2.imencode('.jpg', frame)
                    frame = buffer.tobytes()
                    yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
        else:
            print(f"Failed to connect to the stream. Status code: {response.status_code}")

        # Clean up
        # cv2.destroyAllWindows()

####



        # frame = imutils.resize(frame, width=400)
        # (locs, preds) = detect_and_predict_mask(frame, faceNet, model)

        # for (box, pred) in zip(locs, preds):
        #     (startX, startY, endX, endY) = box
        #     (mask, withoutMask) = pred
        #     label = "Mask" if mask > withoutMask else "No Mask"
        #     probability = max(mask, withoutMask) * 100

        #     # Update the latest prediction
        #     latest_prediction["label"] = label
        #     latest_prediction["probability"] = probability

        #     label_text = "{}: {:.2f}%".format(label, probability)
        #     color = (0, 255, 0) if label == "Mask" else (0, 0, 255)
        #     cv2.putText(frame, label_text, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
        #     cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

        # ret, buffer = cv2.imencode('.jpg', frame)
        # frame = buffer.tobytes()
        # yield (b'--frame\r\n'
        #        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')




# This is the code made by Jingtong

# def generate_frames():
#     server_socket.listen(1)
#     print("Waiting for connection from Raspberry Pi...")
#     client_socket, addr = server_socket.accept()
#     while True:
#         try:
#             image_size = int.from_bytes(client_socket.recv(4), 'big')
#             # Receive the image data
#             image_data = b''
#             while len(image_data) < image_size:
#                 packet = client_socket.recv(4096)
#                 if not packet:
#                     break
#                 image_data += packet

#             # Save the received image to the specified path
#             with open("image.jpg", 'wb') as image_file:
#                 image_file.write(image_data)
            
#             frame = cv2.imread("image.jpg")
#             if frame is None or frame.size == 0:
#                 print("Error: Frame not captured correctly")
#                 continue
#             frame = imutils.resize(frame, width=400)
#             (locs, preds) = detect_and_predict_mask(frame, faceNet, model)
#             # Loop over the detected face locations and their corresponding locations
#             for (box, pred) in zip(locs, preds):
#                 (startX, startY, endX, endY) = box
#                 (mask, withoutMask) = pred
#                 # Determin the class label and color we'll sue to draw the bounding box and text
#                 label = "Mask" if mask > withoutMask else "No Mask"
#                 color = (0, 255, 0) if label == "Mask" else (0, 0, 255)
#                 # Include the probability in the label
#                 label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)
#                 # Display the label and bounding box rectangle on the output frame
#                 cv2.putText(frame, label, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
#                 cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                     b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
#         except Exception as e:
#             print(f"Error in receiving video frame: {e}")
#             client_socket.close()
#             client_socket, addr = server_socket.accept()



def generate_single_frame():
    try:
        # Initialize the camera (0 is the default camera)
        camera = cv2.VideoCapture(0)

        # Check if the camera opened successfully
        if not camera.isOpened():
            print("Error: Could not open camera.")
            return None

        # Capture a single frame from the camera
        ret, frame = camera.read()

        # Release the camera
        camera.release()

        # Check if frame is captured successfully
        if not ret:
            print("Error: Could not read frame.")
            return None
        
        # Detect faces and predict mask/no mask
        locs, preds = detect_and_predict_mask(frame, faceNet, model)

        # Loop over the detected face locations and their corresponding predictions
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

        # Save the captured frame to the static folder
        # Format the current date and time
        # current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Use the formatted date and time in the file path
        # image_path = os.path.join("static/images", f"captured_image_{current_time}.jpg")

        image_path = os.path.join("static/images", "captured_image.jpg")
        cv2.imwrite(image_path, frame)

        # Get the temperature
        temperature = 35.5
        store_data(temperature, label, image_path)

        # Encode the frame in JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        return frame, label

    except Exception as e:
        print(f"Error in processing single frame: {e}")
        return None



## This is the code made by JingTong

# def generate_single_frame():
#     try:
#         server_socket.listen(1)
#         print("Waiting for connection from Raspberry Pi...")
#         client_socket, addr = server_socket.accept()
#         print(f"Connected to {addr}")
#         # Receive the image size first
#         image_size = int.from_bytes(client_socket.recv(4), 'big')

#         # Receive the image data
#         image_data = b''
#         while len(image_data) < image_size:
#             packet = client_socket.recv(4096)
#             if not packet:
#                 break
#             image_data += packet

#         # Save the received image to the specified path
#         with open("image.jpg", 'wb') as image_file:
#             image_file.write(image_data)
        
#         frame = cv2.imread("image.jpg")
#         # Detect faces and predict mask/no mask
#         locs, preds = detect_and_predict_mask(frame, faceNet, model)

#         # Loop over the detected face locations and their corresponding locations
#         for (box, pred) in zip(locs, preds):
#             (startX, startY, endX, endY) = box
#             (mask, withoutMask) = pred
#             # Determine the class label and color we'll use to draw the bounding box and text
#             label = "Mask" if mask > withoutMask else "No Mask"
#             color = (0, 255, 0) if label == "Mask" else (0, 0, 255)
#             # Include the probability in the label
#             label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)
#             # Display the label and bounding box rectangle on the output frame
#             cv2.putText(frame, label, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
#             cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

#         # Encode the frame in JPEG format
#         ret, buffer = cv2.imencode('.jpg', frame)
#         frame = buffer.tobytes()
#         return frame

#     except Exception as e:
#         print(f"Error in processing single frame: {e}")
#         return None
#     finally:
#         client_socket.close()
#         # server_socket.close()

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

@app.route('/entry', methods=['POST'])
def add_entry():
    try:
        temperature = request.form['temperature']
        mask_status = request.form['mask_status'].lower() == 'true'
        image = request.files['image']

        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        # Save the image file
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(image_path)

        # Create a new Entry instance and save it to the database
        new_entry = Entry(temperature=float(temperature), mask_status=mask_status, image_path=image_path)
        db.session.add(new_entry)
        db.session.commit()

        return jsonify({'message': 'Entry added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/entries', methods=['GET'])
def get_entries():
    entries = Entry.query.all()
    results = []
    for entry in entries:
        results.append({
            'id': entry.id,
            'timestamp': entry.timestamp,
            'temperature': entry.temperature,
            'mask_status': entry.mask_status,
            'image_path': entry.image_path
        })
    return jsonify(results)

@app.route('/api/real_time_data', methods=['GET'])
def get_real_time_data():
    latest_entry = Entry.query.order_by(Entry.timestamp.desc()).first()
    if latest_entry:
        return jsonify({
            'current_reading': {
                'temperature': latest_entry.temperature,
                'mask_status': latest_entry.mask_status,
                'timestamp': latest_entry.timestamp,
                'image_path': latest_entry.image_path  # Include the image path
            }
        })
    return jsonify({'error': 'No data available'}), 404

@app.route('/api/current_image', methods=['GET'])
def get_current_image():
    latest_entry = Entry.query.order_by(Entry.timestamp.desc()).first()
    if latest_entry:
        return send_from_directory(app.config['UPLOAD_FOLDER'], latest_entry.image_path.split('/')[-1])
    return jsonify({'error': 'No image available'}), 404

@app.route('/latest_prediction', methods=['GET'])
def get_latest_prediction():
    return jsonify(latest_prediction)


@app.route('/images/<filename>')
def get_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# def capture_and_upload():
#     while True:
#         frame_data = generate_single_frame()
#         if frame_data is None:
#             print("Error capturing frame.")
#             time.sleep(1)  # Wait before trying again
#             continue
#         time.sleep(1) 


if __name__ == "__main__":
    # thread = threading.Thread(target=capture_and_upload, daemon=True)
    # thread.start()
    # app.run(host='172.20.10.11', port=5000)
    app.run(host='0.0.0.0', port=5000)
