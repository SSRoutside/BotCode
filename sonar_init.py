import RPi.GPIO as GPIO
import time
import numpy as np

# function to get a distance from the sensors
def getDist(TRIG, ECHO):
    # set trigger pin high for 10 nan0-seconds
    # senosr will send 8 sound bursts
    TRIG.write(1)
    time.sleep(0.00001)
    # set low again
    TRIG.write(0)

#### section monitors time needed to "listen" to the rebounding signal

    # record last low timestamp for ECHO pin (pulse_start)
    while ECHO.read() == 0:
        pulse_start = time.time()

    # record last high timestamp for ECHO pin (pulse_end)
    while ECHO.read() == 1:
        pulse_end = time.time()


    # calculate difference between pulse_start and pulse_end
    # to determine the duration of the pulse
    try:
        pulse_duration = pulse_end - pulse_start

        # do physics and get the distance in cm
        distance = pulse_duration * 17150

        return distance

    except:
        pass

############### end functions

# select a numbering system for pin addressing
# BCM: numbers after GPIO on labeling pictures
# BOARD: physical numbers of pins (CHOSEN CURRENTLY, CAN BE CHANGED)
GPIO.setmode(GPIO.BOARD)

## CHANGE THESE PIN ADDRESSES AS NECESSARY

# address trigger pins and set them to output with an initial state of low
# the echo pins must also be addressed and set as input
RF_TRIG = GPIO.setup(7, GPIO.OUT, initial=GPIO.LOW)
RF_ECHO = GPIO.setup(11, GPIO.IN)

LF_TRIG = GPIO.setup(15, GPIO.OUT, initial=GPIO.LOW)
LF_ECHO = GPIO.setup(16, GPIO.IN)

RB_TRIG = GPIO.setup(12, GPIO.OUT, initial=GPIO.LOW)
RB_ECHO = GPIO.setup(13, GPIO.IN)

LB_TRIG = GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW)
LB_ECHO = GPIO.setup(22, GPIO.IN)

# wait for sensors to settle (ensures low setting)
print("Waiting For Sensor To Settle")
time.sleep(2)
print("done waiting")
