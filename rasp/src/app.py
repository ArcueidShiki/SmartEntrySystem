#!/usr/bin/python3

from flask import Flask, Response, jsonify, request
import io
import logging
from threading import Condition, Thread
from http import server
import smbus
import time
import RPi.GPIO as GPIO
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput

app = Flask(__name__)

# Servo motor configuration
GPIO.setmode(GPIO.BCM)
SERVO_PIN = 18
GPIO.setup(SERVO_PIN, GPIO.OUT)
PWM = GPIO.PWM(SERVO_PIN, 50)
PWM.start(0)

# Temperature sensor configuration
BUS = smbus.SMBus(1)
mlx99614_address = 0x5A

def read_temperature():
    temp = BUS.read_word_data(mlx99614_address, 0x07)
    return temp * 0.02 - 273.15

def set_angle(angle):
    duty = angle / 18 + 2
    GPIO.output(SERVO_PIN, True)
    PWM.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(SERVO_PIN, False)
    PWM.ChangeDutyCycle(0)

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

def control_servo():
    # 1 OPEN, 0 CLOSE
    angle = int(request.args.get('gate_', 0))
    # TODO  request the result from backend

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=8000, threaded=True)
    finally:
        PWM.stop()
        GPIO.cleanup()