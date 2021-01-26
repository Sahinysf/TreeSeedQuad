
from time import sleep      # Import sleep from time
import RPi.GPIO as GPIO     # Import Standard GPIO Module

GPIO.setmode(GPIO.BOARD)      # Set GPIO mode to BCM
GPIO.setwarnings(False)

# PWM Frequency
pwmFreq = 100

# Setup Pins for motor controller
GPIO.setup(12, GPIO.OUT)    # PWMA
GPIO.setup(18, GPIO.OUT)    # AIN2
GPIO.setup(16, GPIO.OUT)    # AIN1
GPIO.setup(22, GPIO.OUT)    # STBY
GPIO.setup(15, GPIO.OUT)    # BIN1
GPIO.setup(13, GPIO.OUT)    # BIN2
GPIO.setup(11, GPIO.OUT)    # PWMB

pwma = GPIO.PWM(12, pwmFreq)    # pin 18 to PWM
pwmb = GPIO.PWM(11, pwmFreq)    # pin 13 to PWM
pwma.start(100)
pwmb.start(100)



def motor1():
    runMotor(0, 30, 0)
    sleep(.20)
    runMotor(0, 30, 1)
    sleep(.20)
    motorStop()


def motor2():
    runMotor(1, 30, 0)
    sleep(.20)
    runMotor(1, 30, 1)
    sleep(.20)
    motorStop()



def runMotor(motor, spd, direction):
    GPIO.output(22, GPIO.HIGH)
    in1 = GPIO.HIGH
    in2 = GPIO.LOW

    if(direction == 1):
        in1 = GPIO.LOW
        in2 = GPIO.HIGH

    if(motor == 0):
        GPIO.output(16, in1)
        GPIO.output(18, in2)
        GPIO.output(15, GPIO.LOW)
        GPIO.output(13, GPIO.LOW)
        pwma.ChangeDutyCycle(spd)

    elif(motor == 1):
        GPIO.output(16, GPIO.LOW)
        GPIO.output(18, GPIO.LOW)
        GPIO.output(15, in1)
        GPIO.output(13, in2)
        pwmb.ChangeDutyCycle(spd)


def motorStop():
    GPIO.output(22, GPIO.LOW)

## Main
##############################################################################
def main(args=None):
    while(True):
        print ("Which motor do you want to run?")
        x = input()
        if (x == 1):
            motor1()
        elif (x == 2):
            motor2()



if __name__ == "__main__":
    main()

