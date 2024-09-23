# pip install picamera[array] request RPi.GPIO
import imutils
import socket
import struct
import time
import requests
import json
from picamera.array import PiRGBArray
from picamera import PiCamera
import smbus
import RPi.GPIO as GPIO
import jpg

# Configuration
BACKEND_URL = "http://172.20.10.11:5000/video_feed"
SERVO_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
PWM = GPIO.PWM(SERVO_PIN, 50)
PWM.start(0)
BUS = smbus.SMBus(1)
mlx99614_address = 0x5A
SERVO = GPIO.PWM(SERVO_PIN, 50)
SERVO.start(0)
camera = PiCamera()
camera.resolution = (640, 480)
camera.framrate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)

clien_socket = socket.socket(socket.AF_INET, socket.SOCKET_STREAM)
client_socket.connect(('172.20.10.11', 8000))

def encode_image(image_path):
    with open(image_path, 'rb') as f:
        return jpg.encode(f.read())

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
    try:

        img_encoded = encode_image('.jpg', image)
        client_socket.sendall(struct.pack("L", len(img_encoded)))
        client_socket.sendall(img_encoded)
        client_socket.sendall(struct.pack("f", temperature))
        # data = {
        #     'temperature': temperature
        # }
        # files = {
        #     'image': img_encoded.tobytes(),
        #     'data': json.dumps(data)
        # }
        # response = requests.post(BACKEND_URL, files=files)
        # return response.josn()
        response = client_socket.recv(1024).decode()
        return {'command': response}
    except Exception as e:
        print(f"Error sending data: {e}")
        return {}




def control_servo(command):
    if command == "open":
        servo = ChangeDutyCycle(7.5)    # 90 degrees
    elif command == "close":
        servo = ChangeDutyCycle(2.5)    # 0 degrees

def main():
    try:
        while True:
            # Loop over the frames from the video stream
            for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port = True):
                # Grab the frame from the video stream and resize it
                image = frame.array
                image = imutils.resize(image, width = 400)
                # Read temperature from the sensor
                temperature = read_temperature()
                if temperature is not None:
                    response = send_data(image, temperature)
                    # Control servo motor based on the response
                    if 'command' in response:
                        control_servo(response['command'])
                # Clear the stream in preparation for the next frame.
                rawCapture.truncate(0)
    except Exception as e:
        print(f"Error:in main loop: {e}")
    finally:
        # Clean up
        servo.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    main()
