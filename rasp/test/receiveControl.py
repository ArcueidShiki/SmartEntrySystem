import RPi.GPIO as GPIO
import socket

# Set up GPIO for the servo
servo_pin = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)  # 50Hz PWM frequency
pwm.start(0)

def set_servo_angle(angle):
    duty = angle / 18 + 2  # Calculate duty cycle for the desired angle
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)

def start_server(host='0.0.0.0', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Servo control server listening on {host}:{port}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")

            # Receive angle command
            data = client_socket.recv(1024).decode()
            if data:
                angle = int(data)
                set_servo_angle(angle)
                client_socket.sendall(f"Angle set to {angle} degrees".encode())

            client_socket.close()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        pwm.stop()
        GPIO.cleanup()
        server_socket.close()

if __name__ == "__main__":
    start_server()
