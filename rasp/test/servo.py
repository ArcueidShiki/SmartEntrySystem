import RPi.GPIO as GPIO
import time
# GPIO.setmode(GPIO.BCM)
# servo_pin = 17
# GPIO.setup(servo_pin, GPIO.OUT)
# pwm = GPIO.PWM(servo_pin, 50)
# pwm.start(0)

# def set_angle(angle):
#     duty = angle / 18 + 2
#     GPIO.output(servo_pin, True)
#     pwm.ChangeDutyCycle(duty)
#     time.sleep(1)
#     GPIO.output(servo_pin, False)
#     pwm.ChangeDutyCycle(0)

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

# Init angle
setangle(PWM1, 0)
setangle(PWM1, 180)
try:
    print("Enter loop")
    while True:
        setangle(PWM1, 135)
        setangle(PWM2, 45)
        time.sleep(2)
        setangle(PWM1, 0)
        setangle(PWM2, 180)
        time.sleep(2)
except KeyboardInterrupt:
    PWM2.stop()
    PWM1.stop()
    GPIO.cleanup()
finally:
    GPIO.cleanup()
    