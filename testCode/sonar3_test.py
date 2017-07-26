# imports
import mraa

import time


# pin numbers for TRIG and ECHO (corresponding to physical locations on UP Board (BCM-like))
TRIG = mraa.Gpio(23)
ECHO = mraa.Gpio(24)

# set trigger pin as output and echo pin as input
TRIG.dir(mraa.DIR_OUT)
ECHO.dir(mraa.DIR_IN)

# set trigger pin to low
TRIG.write(0)

# wait for sensor to settle (ensures low setting)
print("Waiting For Sensor To Settle")
time.sleep(2)
print("done waiting")

count = 0
obj_distance = 20
durationList = []

while count < 10:
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
    durationList.append(pulse_duration)


    # do physics... will give distance in cm
##    distance = pulse_duration * 17150

    # round distance to two decimal places
##    distance = round(distance, 2)

    # print distance
##    print("Distance: " + str(distance) + " cm")

    # repeat loop every 2 seconds
    time.sleep(2)

    # append count
    count += 1

print("measurements done")
print(durationList)
