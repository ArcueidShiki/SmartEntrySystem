import random
import flask
import pyautogui
import pytesseract
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
import threading
from flask_cors import CORS
from get_data_from_finalResult import store_data
from screenshot_specific_area import capture_specified_area
from convert_db_to_dashboard import convert_data_to_jason
# from store_data_to_database import store_data

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
    final_result = db.Column(db.Boolean, nullable=False)
    image_path = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()


def detect_and_predict_mask(frame, faceNet, model):
    # Detect faces in the frame and get predictions
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))
    faceNet.setInput(blob)
    detections = faceNet.forward()

    faces = []
    locs = []
    preds = []

    # Loop over the detections
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        # Filter out weak detections
        if confidence > 0.5:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # Ensure the bounding box coordinates are within the frame dimensions
            startX, startY = max(0, startX), max(0, startY)
            endX, endY = min(w, endX), min(h, endY)

            # Extract the face ROI, ensure it's not empty
            face = frame[startY:endY, startX:endX]
            if face.size == 0:
                continue  # Skip empty face regions

            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            face = cv2.resize(face, (224, 224))
            face = img_to_array(face)
            face = preprocess_input(face)

            faces.append(face)
            locs.append((startX, startY, endX, endY))

    # Make a prediction if any faces are found
    if len(faces) > 0:
        faces = np.array(faces, dtype="float32")
        preds = model.predict(faces, batch_size=32)

    return (locs, preds)
    

latest_prediction = {
    "temperature": 0.0,
    "label": "",
    "probability": 0.0,
    "final_result": ""
}


## This is the function to get video from local camera

def generate_frames1():



    global latest_prediction
    global temperature

    # Open a connection to the laptop's camera (0 is usually the default camera)
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Error: Could not open the camera.")
        return

    while True:

        # Fetch and return temperature from the given URL

        # response = requests.get("http://172.20.10.4:8000/temp")
        # if response.status_code == 200:
        #     print(response.json())
        #     temperature = response.json().get("temperature")
        #     print(type(temperature))
        #     print(temperature)
        # else:
        #     print(f"Failed to fetch temperature. Status code: {response.status_code}")



        # Get the temperature for testing
        temperature_options = [35.5, 36.5, 37.5]
         
        temperature = random.choice(temperature_options)

        # Capture frame-by-frame from the laptop's camera
        success, frame = camera.read()

        if not success:
            print("Error: Frame not captured correctly")
            continue

        # Resize the frame (optional, based on your needs)
        frame = imutils.resize(frame, width=400)

        # Call the mask detection function with the frame
        (locs, preds) = detect_and_predict_mask(frame, faceNet, model)

        # Process the predictions and draw bounding boxes
        for (box, pred) in zip(locs, preds):
            (startX, startY, endX, endY) = box
            (mask, withoutMask) = pred
            label = "Mask" if mask > withoutMask else "No Mask"
            probability = max(mask, withoutMask) * 100
            latest_prediction["temperature"] = temperature
            latest_prediction["label"] = label
            latest_prediction["probability"] = probability

            # Final Result
            if latest_prediction["label"] == "Mask" and latest_prediction["temperature"] <= 37:
                latest_prediction["final_result"] = "Open the door"
            else:
                latest_prediction["final_result"] = "Close the door"

            label_text = "{}: {:.2f}%".format(label, probability)
            color = (0, 255, 0) if label == "Mask" else (0, 0, 255)

            # Draw the label and bounding box on the frame
            cv2.putText(frame, label_text, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

        # Encode the frame in JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield the frame as a multipart message to be served in the response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


## This is the function to get video from raspberry pi
def generate_frames():
    global latest_prediction

    # global temperature

    while True:

        # # Get the temperature for testing
        # temperature_options = [35.5, 36.5, 37.5]
         
        # temperature = random.choice(temperature_options)


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

                        # latest_prediction["temperature"] = temperature

                        latest_prediction["label"] = label
                        latest_prediction["probability"] = probability

                        # # Final Result
                        # if latest_prediction["label"] == "Mask" and latest_prediction["temperature"] <= 37:
                        #     latest_prediction["final_result"] = "Open the door"
                        # else:
                        #     latest_prediction["final_result"] = "Close the door"


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
        # temperature = 35.5
        # store_data(temperature, label, image_path)

        # Encode the frame in JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        return frame, label

    except Exception as e:
        print(f"Error in processing single frame: {e}")
        return None


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
        temperature = float(request.form.get('temperature'))  # Ensure this is a float
        mask_status = request.form.get('mask_status') == 'True'  # Convert to boolean
        final_result = request.form.get('final_result') == 'True'  # Convert to boolean
        image_path = request.files['image'].filename  # Adjust as necessary

        # Log the received data
        print(f"Received: temperature={temperature}, mask_status={mask_status}, final_result={final_result}, image_path={image_path}")

        new_entry = Entry(
            temperature=temperature,
            mask_status=mask_status,
            final_result=final_result,
            image_path=image_path
        )

        db.session.add(new_entry)
        db.session.commit()
        return jsonify({"message": "Entry added successfully."}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


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
            'final_result': entry.final_result,
            'image_path': entry.image_path
        })
    return jsonify(results)

@app.route('/result', methods=['GET'])
def get_results():
    entries = Entry.query.all()
    results = []
    for entry in entries:
        results.append({



            'timestamp': entry.timestamp,
            'final_result': entry.final_result

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



def capture_screenshot():

    # Get the current time for the screenshot filename
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_filename = f"screenshot_{current_time}.png"

    # Capture the screenshot
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_filename)
    print(f"Screenshot saved as {screenshot_filename}")





# Function to start  background task

def start_background_task():
    task_thread = threading.Thread(target=convert_data_to_jason)
    task_thread.daemon = True
    task_thread.start()


def run_flask_app():
    global flask_running
    app.run(host='0.0.0.0', port=5000)



if __name__ == "__main__":
    

    # Start the Flask app in a separate thread
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.start()

    # Wait until the Flask app is running by checking for a response
    while True:
        try:
            # Make a request to the Flask app to check if it's running
            response = requests.get("http://127.0.0.1:5000")  # Adjust the endpoint as necessary
            if response.status_code == 200:
                print("Flask app is running.")
                break  # Exit the loop if Flask is up
        except requests.ConnectionError:
            time.sleep(0.1)  # Wait a bit before retrying

    start_background_task()

    try:
        

        # Capture the screenshot in a loop
        while True:
            if latest_prediction["label"]:
                screenshot_path = capture_specified_area("real-time", "last")
                

                # upload the data to the database
                store_data(screenshot_path)
            else:
                continue
    except KeyboardInterrupt:
        print("Stopping screenshot capture.")

    

    # Wait for the Flask app to finish
    flask_thread.join()