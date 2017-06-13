import time as TIME
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import atexit

import logging
logging.basicConfig(level=logging.INFO)

# From Adafruit MotorHat example code
# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x60)


# get each motor
myMotor1 = mh.getMotor(1)
myMotor2 = mh.getMotor(2)
myMotor3 = mh.getMotor(3)
myMotor4 = mh.getMotor(4)

# auto disable motors on shutdown
def turnOffMotors():
        mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

# Open the joystick device. 
fn = '/dev/input/js0'
print('Opening %s...' % fn)
jsdev = open(fn, 'rb')


# go into driving robots with a loop

motorrunning = True

while motorrunning:

	evbuf = jsdev.read(8)

	# buttons being used
	off_button = 5

	# axis being used
	

	if evbuf:
		time, value, type, number = stuct.unpack('IhBB', evbuf)

		if type & 0x80:
			print('(initial)')

		# determines if signal from remote is coming from a button
		if type & 0x01:
			#off button
			if (number == off_button) and value:
				break

		# determines if signal from remote is coming from an axis
		if type & 0x02:
			
	#wait before looping again
	TIME.sleep(0.01)

print('Turning off...')
