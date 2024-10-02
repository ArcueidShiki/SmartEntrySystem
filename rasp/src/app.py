#!/usr/bin/python3

import io
import time
import smbus
import logging
import requests
import RPi.GPIO as GPIO
from http import server
from RPLCD.gpio import CharLCD
from picamera2 import Picamera2
from picamera2.outputs import FileOutput
from threading import Condition, Thread
from picamera2.encoders import JpegEncoder
from flask import Flask, Response, jsonify

app = Flask(__name__)

# Servo motor configuration
# Setup GPIO mode
GPIO.setmode(GPIO.BCM)
SERVO_PIN1 = 17
SERVO_PIN2 = 18
# Setup pins as output
GPIO.setup(SERVO_PIN1, GPIO.OUT)
GPIO.setup(SERVO_PIN2, GPIO.OUT)
# Setup PWM for both servos, 50Hz
PWM1 = GPIO.PWM(SERVO_PIN1, 50)
PWM2 = GPIO.PWM(SERVO_PIN2, 50)

# Start PWM with 0 duty cycle
PWM1.start(0)
PWM2.start(0)

def setangle(pwm, angle):
    # convert the angle to duty cycle and set it on the PWM pin
    duty = angle / 18 + 2
    pwm.ChangeDutyCycle(duty)

# Temperature sensor configuration
BUS = smbus.SMBus(1)
mlx90614_address = 0x5A

# LCD configuration PIN 11-16, 1-6
# 7,8, 25, 24, 23, 18

lcd = CharLCD(cols = 16,
              rows = 2,
              pin_rs = 7,
              pin_e = 8,
              pins_data = [25, 24, 23, 10],
              numbering_mode = GPIO.BCM)
# Max 32 length string. 16 x 2, LCD capacity.
DEFAULT_MSG = "Please Wait..."

def display_message(msg):
    lcd.clear()
    lcd.write_string(msg)

def read_temperature():
    temp = BUS.read_word_data(mlx90614_address, 0x07)
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

def setangle(pwm, angle):
    # convert the angle to duty cycle and set it on the PWM pin
    duty = angle / 18 + 2
    pwm.ChangeDutyCycle(duty)

def open_gate():
    setangle(PWM1, 135)
    setangle(PWM2, 45)
    time.sleep(2)
    setangle(PWM1, 0)
    setangle(PWM2, 180)
    time.sleep(2)

# Init angle
setangle(PWM1, 0)
setangle(PWM1, 180)
OPEN = True
CLOSE = False

def get_result():
    RESULT_API = "http://192.168.1.107:5000/result"
    try:
        while True:
            response = requests.get(RESULT_API)
            print("Get reponse")
            if response.status_code == 200:
                data = response.json()
                result = data.get('result', CLOSE)
                msg = data.get('message', DEFAULT_MSG)
                print(data)
                print(msg)
                if result == OPEN:
                    open_gate()
                # if not OPEN, remain close.
                display_message(msg)
            else:
                print(f"Failed to fetch result, status code: {response.status_code}")
            time.sleep(10)
    except Exception as e:
        PWM1.stop()
        PWM2.stop()
        GPIO.cleanup()
        print(f"Error fetching gate control result: {e}")

control_thread = Thread(target = get_result)
control_thread.daemon = True
control_thread.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, threaded=True)
