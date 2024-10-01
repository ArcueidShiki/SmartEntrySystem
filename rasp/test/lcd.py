import RPi.GPIO as GPIO
import time
from RPLCD.gpio import CharLCD

# backlight_pin = 12
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(backlight_pin, GPIO.OUT)

# pwm = GPIO.PWM(backlight_pin, 100)
# pwm.start(100)
# Initialize the LCD
lcd = CharLCD(
    cols=16,
    rows=2,
    pin_rs=7,
    pin_e=8,
    pins_data=[25, 24, 23, 10],
    numbering_mode=GPIO.BCM)


lcd.clear()

lcd.write_string("Please wear a mask!")

GPIO.cleanup()