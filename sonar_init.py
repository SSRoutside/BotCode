import mraa
import time

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
    pulse_duration = pulse_end - pulse_start

    # do physics and get the distance in cm
    distance = pulse_duration * 17150

    return distance

############### end functions

# pin numbers for TRIG and ECHO (corresponding to physical locations on UP Board (BCM-like))

## CHANGE THESE PIN ADDRESSES AS NECESSARY

RF_TRIG = mraa.Gpio(23)
RF_ECHO = mraa.Gpio(24)

LF_TRIG = mraa.Gpio(31)
LF_ECHO = mraa.Gpio(32)

RB_TRIG = mraa.Gpio(37)
RB_ECHO = mraa.Gpio(38)

LB_TRIG = mraa.Gpio(36)
LB_ECHO = mraa.Gpio(40)

# set trigger pins low
RF_TRIG.write(0)
LF_TRIG.write(0)
RB_TRIG.write(0)
LB_TRIG.write(0)

# wait for sensors to settle (ensures low setting)
print("Waiting For Sensor To Settle")
time.sleep(2)
print("done waiting")
