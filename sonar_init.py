import mraa
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
