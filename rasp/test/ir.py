import smbus
import time

bus = smbus.SMBus(1)
mlx99614_address = 0x5A

def read_temperature():
    temp = bus.read_word_data(mlx99614_address, 0x07)
    return temp * 0.02 - 273.15

try:
    while True:
        temperature = read_temperature()
        print(f"Temperature: {temperature: .2f} C")
        time.sleep(1)
except KeyboardInterrupt:
    print("Program stopped")