
from webdriver_manager.chrome import ChromeDriverManager
import threading
from flask_cors import CORS
from get_data_from_finalResult import store_data
from screenshot_specific_area import capture_specified_area
from convert_db_to_dashboard import convert_data_to_jason
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from flask import Flask, render_template, Response, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import numpy as np
import cv2
import socket
import requests


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

db = SQLAlchemy(app)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    temperature = db.Column(db.Float, nullable=False)
    mask_status = db.Column(db.Boolean, nullable=False)
    final_result = db.Column(db.Boolean, nullable=False)


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
        if confidence > 0.8:
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
    "final_result": "",
    "result":False,
    "message": ""
}


def generate_frames():
    global latest_prediction

    while True:
        # Fetch the video stream
        url = 'http://192.168.1.106:8000/stream.mjpg'
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
                    
                    # Refetch temperature during each frame processing loop
                    temperature = 0.0
                    temp_response = requests.get("http://192.168.1.106:8000/temp")
                    if temp_response.status_code == 200:
                        temperature = temp_response.json().get("temperature")
                        # print(f"Temperature: {temperature}")
                    else:
                        print(f"Failed to fetch temperature. Status code: {temp_response.status_code}")

                    # Resize frame (if needed)
                    # frame = imutils.resize(frame, width=400)

                    # Detect mask and make predictions
                    (locs, preds) = detect_and_predict_mask(frame, faceNet, model)
                    for (box, pred) in zip(locs, preds):
                        (startX, startY, endX, endY) = box
                        (mask, withoutMask) = pred
                        label = "Mask" if mask > withoutMask else "No Mask"
                        probability = max(mask, withoutMask) * 100

                        # Update latest prediction with temperature and mask detection
                        latest_prediction["temperature"] = temperature
                        latest_prediction["label"] = label
                        latest_prediction["probability"] = probability

                        # Final Result decision based on mask and temperature
                        if latest_prediction["label"] == "Mask" and latest_prediction["temperature"] <= 37:
                            latest_prediction["final_result"] = "Open the door"
                            latest_prediction["result"] = True
                            latest_prediction["message"] = "Welcome."
                        else:
                            latest_prediction["final_result"] = "Close the door"
                            latest_prediction["result"] = False
                            if latest_prediction["label"] == "No Mask":
                                latest_prediction["message"] = "Sorry, you must wear a mask."
                            else:
                                latest_prediction["message"] = "Sorry, your temperatue is higher than 37C."
                        print(latest_prediction)
                        # Draw label and bounding box
                        label_text = "{}: {:.2f}%".format(label, probability)
                        color = (0, 255, 0) if label == "Mask" else (0, 0, 255)
                        cv2.putText(frame, label_text, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
                        cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

                    # Encode the frame to JPEG
                    ret, buffer = cv2.imencode('.jpg', frame)
                    frame = buffer.tobytes()

                    # Yield the frame as a multipart message
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            print(f"Failed to connect to the stream. Status code: {response.status_code}")




def upload_data(temperature, label, final_result):
    url = 'http://127.0.0.1:5000/entry'
    data = {
        'temperature': temperature,
        'mask_status': label,
        'final_result': final_result  # Ensure final_result is included
    }

    try:
        response = requests.post(url, data=data)
        if response.status_code == 201:
            print("Entry added successfully.")
        else:
            print(f"Failed to add entry: {response.text}")
    except Exception as e:
        print(f"Error in store_data: {e}")




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route('/entry', methods=['POST'])
def add_entry():
    try:
        temperature = float(request.form.get('temperature'))  # Ensure this is a float
        mask_status = request.form.get('mask_status') == 'True'  # Convert to boolean
        final_result = request.form.get('final_result') == 'True'  # Convert to boolean

        # Log the received data
        print(f"Received: temperature={temperature}, mask_status={mask_status}, final_result={final_result}")

        new_entry = Entry(
            temperature=temperature,
            mask_status=mask_status,
            final_result=final_result
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
            'final_result': entry.final_result
        })
    return jsonify(results)

@app.route('/result', methods=['GET'])
def get_results():
    print("Raspberry Pi got the result of the door................................................")
    print(f"The Result is: {latest_prediction}")
    temperature = latest_prediction["temperature"]
    final_result = latest_prediction["result"]
    if latest_prediction["label"] == "Mask":
        mask_status = True
    else:
        mask_status = False
    upload_data(temperature, mask_status, final_result)
    return jsonify({"result":latest_prediction["result"], "message": latest_prediction["message"]})



@app.route('/latest_prediction', methods=['GET'])
def get_latest_prediction():
    print("Dashboard got the latest_prediction")
    return jsonify(latest_prediction)

    


def start_background_task():
    task_thread = threading.Thread(target=convert_data_to_jason)
    task_thread.daemon = True
    task_thread.start()



start_background_task()


if __name__ == "__main__":
    
    app.run(host='0.0.0.0', port=5000)
