from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
import time

#initiate the camera

picam2 = Picamera2()

#configure the camera for preview and capture
camera_config = picam2.create_still_configuration()
picam2.configure(camera_config)

#start the camera

picam2.start()

#Capture the image

print("capturing image... ")

picam2.capture_file("image.jpg")

print("Image saved as 'image.jpg'")

# Stop the camera
picam2.stop()