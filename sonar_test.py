# imports for UP board GPIO and time
import Adafruit_GPIO as GPIO
import time

# grab a GPIO adapter from the current platform
gpio = GPIO.get_platform_gpio()

# pin numbers for TRIG and ECHO as connected on the UP board
TRIG = 23
ECHO = 24

print("Distance Measurement in progress.")

# set trigger pin as output and echo pin as input
gpio.setup(TRIG,GPIO.OUT)
gpio.setup(ECHO,GPIO.IN)

# set trigger pin to low (0V)
gpio.output(TRIG, False)

# wait for sensor to settle (ensures low setting)
print("Waiting For Sensor To Settle")
time.sleep(2)
print("done waiting")

# set trigger pin high for 10 nano-seconds
# sensor will send 8 sound-bursts
gpio.output(TRIG, True)
time.sleep(0.00001)
# set low again
gpio.output(TRIG, False)
print('dead yet?')

#### section monitors time needed to "listen" to
#### the rebounding signal

# record last low timestamp for ECHO pin (pulse_start)
while gpio.input(ECHO) == GPIO.LOW:
    pulse_start = time.time()

# record last high timestamp for ECHO pin (pulse_end)
while gpio.input(ECHO) == GPIO.HIGH:
    pulse_end = time.time()

print('still not dead')
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
