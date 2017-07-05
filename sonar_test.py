# imports for UP board GPIO and time
import Adafruit_GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# pin numbers for TRIG and ECHO as connected on the UP board
TRIG = 23
ECHO = 24

print("Distance Measurement in progress.")

# set trigger pin as output and echo pin as input
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

# set trigger pin to low (0V)
GPIO.output(TRIG, False)

# wait for sensor to settle (ensures low setting)
print("Waiting For Sensor To Settle") 
time.sleep(2)

# set trigger pin high for 10 nano-seconds
# sensor will send 8 sound-bursts
GPIO.output(TRIG, True)
time.sleep(0.00001)
# set low again
GPIO.output(TRIG, False)

#### section monitors time needed to "listen" to
#### the rebounding signal

# record last low timestamp for ECHO pin (pulse_start)
while GPIO.input(ECHO) == 0:
    pulse_start = time.time()

# record last high timestamp for ECHO pin (pulse_end)
while GPIO.input(ECHO) == 1:
    pulse_end = time.time()

# calculate difference between pulse_start and pulse_end
# to determine the duration of the pulse
pulse_duration = pulse_end - pulse_start

# do physics... will give distance in cm
distance = pulse_duration * 17150

# round distance to two decimal places
distance = round(distance, 2)

# print distance
print("Distance: ", distance, " cm")

# clean GPIO pins to ensure that all inputs/outputs reset
GPIO.cleanup()  
