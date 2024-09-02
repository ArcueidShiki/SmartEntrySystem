from gpiozero import AngularServo
from time import sleep

servo = AngularServo(18 ,
                     min_angle=-42,
                     max_angle=44
                     )
while (True):
    servo.angle = -42
    sleep(2)
    servo.angle = 0
    sleep(2)
    servo.angle = 44
    sleep(2)
    
    
    
    
