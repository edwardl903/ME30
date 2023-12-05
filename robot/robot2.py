from flask import Flask
import RPi.GPIO as GPIO

app = Flask(__name__)

GPIO.setmode(GPIO.BOARD)
motor_pin = 16
GPIO.setup(motor_pin, GPIO.OUT)

# Global PWM variable
pwm = None

# Function to set motor speed using PWM
def set_motor_speed(pin, speed):
    global pwm
    if pwm is not None:
        pwm.stop()  # Stop the previous PWM, if any
    pwm = GPIO.PWM(pin, 1000)  # 1000 Hz frequency, adjust based on your motor specs
    pwm.start(0)  # Initialize PWM with 0% duty cycle
    pwm.ChangeDutyCycle(speed)  # Set the duty cycle to control the motor speed

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/pinon')
def pin_on():
    GPIO.output(motor_pin, GPIO.HIGH)
    return 'I turned on the pin.'

@app.route('/digital/write/<pin_name>/<state>')
def digital_write(pin_name, state):
    pin = int(pin_name)
    if state.upper() in ['1', 'ON', 'HIGH']:
        set_motor_speed(motor_pin, 100)  # Set the speed to 70%, adjust as needed
        return 'Set pin {0} to HIGH'.format(pin_name)
    elif state.upper() in ['0', 'OFF', 'LOW']:
        set_motor_speed(motor_pin, 0)  # Set the speed to 70%, adjust as needed
        return 'Set pin {0} to MEDIUM speed'.format(pin_name)
    elif state.upper() == 'MED':
        set_motor_speed(motor_pin, 70)  # Set the speed to 70%, adjust as needed
        return 'Set pin {0} to MEDIUM speed'.format(pin_name)
    elif state.upper() == 'SLOW':
        set_motor_speed(motor_pin, 40)  # Set the speed to 40%, adjust as needed for slowest speed
        return 'Set pin {0} to SLOW speed'.format(pin_name)
    return 'Something went wrong'

if __name__ == '__main__':
    app.run(debug=True)
