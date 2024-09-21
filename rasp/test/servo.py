import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
servo_pin = 18
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)

def set_angle(angle):
    duty = angle / 18 + 2
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)

try:
    print("Enter loop")
    while True:
        set_angle(0)
        time.sleep(2)
        set_angle(90)
        time.sleep(2)
        set_angle(180)
        time.sleep(2)
except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
    