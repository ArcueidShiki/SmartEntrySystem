import RPi.GPIO as GPIO
from RPLCD.gpio import CharLCD



# Initialize the LCD
lcd = CharLCD(
    cols=16,
    rows=2,
    pin_rs=7,
    pin_e=8,
    pins_data=[25, 24, 23, 18],
    numbering_mode=GPIO.BCM)


lcd.clear()

lcd.write_string("Please wear a mask!")

GPIO.cleanup()