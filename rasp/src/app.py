#!/usr/bin/python3

import io
import time
import smbus
import logging
import RPi.GPIO as GPIO
from http import server
from RPLCD.gpio import CharLCD
from picamera2 import Picamera2
from picamera2.outputs import FileOutput
from threading import Condition, Thread
from picamera2.encoders import JpegEncoder
from flask import Flask, Response, jsonify, requests

app = Flask(__name__)

# Servo motor configuration
GPIO.setmode(GPIO.BCM)
SERVO_PIN = 21
GPIO.setup(SERVO_PIN, GPIO.OUT)
PWM = GPIO.PWM(SERVO_PIN, 50)
PWM.start(0)
OPEN = 0
CLOSE = 1

# Temperature sensor configuration
BUS = smbus.SMBus(1)
mlx99614_address = 0x5A

# LCD configuration
lcd = CharLCD(cols = 16,
              rows = 2,
              pin_rs = 7,
              pin_e = 8,
              pins_data = [25, 24, 23, 18],
              numbering_mode = GPIO.BCM)
DEFAULT_MSG = "Please wear mask and scan your temperature."

def display_message(msg):
    lcd.clear()
    lcd.write_string(msg)

def read_temperature():
    temp = BUS.read_word_data(mlx99614_address, 0x07)
    return temp * 0.02 - 273.15

@app.route('/temp', methods=['GET'])
def get_temp():
    return jsonify({'temperature': round(read_temperature(), 2)})

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

output = StreamingOutput()

@app.route('/stream.mjpg')
def stream():
    def generate_frames():
        try:
            while True:
                with output.condition:
                    output.condition.wait()
                    frame = output.frame
                # continuously generating frames
                yield (b'--FRAME\r\n'
                    b'Content-Type: image/jpeg\r\n'
                    b'Content-Length: ' + str(len(frame)).encode() + b'\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            logging.warning('Streaming error: %s', str(e))
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=FRAME')

def start_camera():
    picam2 = Picamera2()
    picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
    try:
        picam2.start_recording(JpegEncoder(), FileOutput(output))
        # address = ('', 8000)
        # server = StreamingServer(address, StreamingHandler)
        # server.serve_forever()
    except Exception as e:
        print(str(e))

camera_thread = Thread(target = start_camera)
camera_thread.start()

def set_angle(angle):
    duty = angle / 18 + 2
    GPIO.output(SERVO_PIN, True)
    PWM.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(SERVO_PIN, False)
    PWM.ChangeDutyCycle(0)

def open_gate():
    set_angle(0)
    time.sleep(3)
    set_angle(90)

def get_result():
    RESULT_API = "http://172.20.10.11:5000/result"
    while True:
        try:
            response = requests.get(RESULT_API)
            if response.status_code == 200:
                data = response.json()
                result = data.get('result', CLOSE)
                msg = data.get('message', DEFAULT_MSG)
                if result == OPEN:
                    open_gate(result)
                # if not OPEN, remain close.
                display_message(msg)
            else:
                print(f"Failed to fetch result, status code: {response.status_code}")
        except Exception as e:
            print(f"Error fetching gate control result: {e}")
        time.sleep(5)

control_thread = Thread(target = get_result)
control_thread.daemon = True
control_thread.start()

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=8000, threaded=True)
    finally:
        PWM.stop()
        GPIO.cleanup()