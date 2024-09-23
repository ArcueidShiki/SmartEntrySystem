# pip install picamera[array] request RPi.GPIO
import cv2
import imutils
import time
import requests
import json
from picamera.array import PiRGBArray
from picamera import PiCamera
import smbus
import RPi.GPIO as GPIO

# Configuration
BACKEND_URL = "http://<backend_server_ip>:<port>/realtime"
SERVO_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
PWM = GPIO.PWM(SERVO_PIN, 50)
PWM.start(0)
BUS = smbus.SMBus(1)
mlx99614_address = 0x5A
SERVO = GPIO.PWM(SERVO_PIN, 50)
SERVO.start(0)

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

def send_data(image, temperature):
    _, img_encoded = cv2.imencode('.jpg', image)
    data = {
        'temperature': temperature
    }
    files = {
        'image': img_encoded.tobytes(),
        'data': json.dumps(data)
    }
    response = requests.post(BACKEND_URL, files=files)
    return response.josn()

def control_servo(command):
    if command == "open":
        servo = ChangeDutyCycle(7.5)
    elif command = "close":
        servo = ChangeDutyCycle(2.5)

def main():
    try:
        while True:
            # Loop over the frames from the video stream
            from frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port = True):
                # Grab the frame from the video stream and resize it
                image = frame.array
                image = imutils.resize(image, width = 400)
                # Read temperature from the sensor
                temperature = read_temperature()
                response = send_data(image, temperature)
                # Control servo motor based on the response
                if 'command' in response:
                    control_servo(response['command'])
                # Clear the stream in preparation for the next frame.
                rawCapture.truncate(0)
    except Exception as e:
        # Clean up
        servo.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    main()