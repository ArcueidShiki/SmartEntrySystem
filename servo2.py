from gpiozero import Servo
from time import sleep

servo = Servo(18)
servo.value = 0.5
servo.min()
servo.max()
while True:
    servo.min()
    sleep(1)
    servo.mid()
    sleep(1)
    servo.max()
    sleep(1)