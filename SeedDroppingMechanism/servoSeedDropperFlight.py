import threading
import time
import rospy
from clover import srv
from std_srvs.srv import Trigger
import RPi.GPIO as GPIO

rospy.init_node('flight')

get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)

servo1 = 33				# PWM pin
GPIO.setmode(GPIO.BOARD)		#set pin numbering system
GPIO.setup(servo1,GPIO.OUT)
pwm1 = GPIO.PWM(servo1,50)		#create PWM instance with frequency
pwm1.start(0)				#start PWM of required Duty Cycle 

def servo_drop(seconds):
    print("Dropping")
    for num in range(seconds/2):
        pwm1.ChangeDutyCycle(10) # right +90 deg position
        sleep(0.5)
        pwm1.ChangeDutyCycle(5) # left -90 deg position
        sleep(0.5)
        print(num)
        time.sleep(2)


if __name__ == "__main__":
    # Take off and hover 2 m above the ground
    navigate(x=0, y=0, z=2, frame_id='body', auto_arm=True)

    # Wait for 5 seconds
    rospy.sleep(5)

    #dropping start for a 4 seconds
    y = threading.Thread(target=servo_drop, args=(4,))
    y.start()

    # Fly forward 1 m
    navigate(x=2, y=0, z=0, frame_id='body')

    # Wait for 5 seconds
    rospy.sleep(10)

    # Perform landing
    land()

pwm1.stop()
GPIO.cleanup()
