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

# get motor values between 0 and 255
def getMotorValue(percent):
	mv = percent * 255
	return mv

# Open the joystick device. 
fn = '/dev/input/js0'
print('Opening %s...' % fn)
jsdev = open(fn, 'rb')


# go into driving robots with a loop

motorrunning = True
c1 = .60
c2 = .30
c3 = .15

while motorrunning:

	evbuf = jsdev.read(8)

	# buttons being used
	off_button = 5
	brake_button = 4

	# axis being used
	UpDownAxis = 2
	UpDownAxis_ID = 0x02

	LeftRightAxis = 0
	LeftRightAxis_ID = 0x00
	

	if evbuf:
		time, value, type, number = stuct.unpack('IhBB', evbuf)

		if type & 0x80:
			print('(initial)')

		# determines if signal from remote is coming from a button
		if type & 0x01:

			# print id of button being hit
			print(value)
			#off button (right 2)
			if (number == off_button) and value:
				break

			# brake button (left 2)
			if number == brake_button and value:
				myMotor1.setSpeed(0)
                                myMotor2.setSpeed(0)
                                myMotor3.setSpeed(0)
                                myMotor4.setSpeed(0)

				myMotor1.run(Adafruit_MotorHAT.FORWARD)
                                myMotor2.run(Adafruit_MotorHAT.FORWARD)
                                myMotor3.run(Adafruit_MotorHAT.FORWARD)
                                myMotor4.run(Adafruit_MotorHAT.FORWARD)

		# determines if signal from remote is coming from an axis
		if type & 0x02:

			# behaviour when when js is pushed up or down
			if (number == UpDownAxis):
				mv = getMotorValue(c1)

				myMotor1.setSpeed(mv)
				myMotor2.setSpeed(mv)
				myMotor3.setSpeed(mv)
				myMotor4.setSpeed(mv)

				# if up
				if (value < 0):
					print('forward')
					myMotor1.run(Adafruit_MotorHAT.FORWARD)
					myMotor2.run(Adafruit_MotorHAT.FORWARD)
					myMotor3.run(Adafruit_MotorHAT.FORWARD)
					myMotor4.run(Adafruit_MotorHAT.FORWARD)
				#if down
				elif (value > 0):
					print('backward')
					myMotor1.run(Adafruit_MotorHAT.BACKWARD)
                                        myMotor2.run(Adafruit_MotorHAT.BACKWARD)
                                        myMotor3.run(Adafruit_MotorHAT.BACKWARD)
                                        myMotor4.run(Adafruit_MotorHAT.BACKWARD)

			# behaviour when js is pushed right
			if (number == LeftRightAxis) and (value > 0):
				print('right')
				# left motors at higher speed
				myMotor1.setSpeed(c2)
				myMotor2.setSpeed(c2)
				# right motors at lower speed
				myMotor3.setSpeed(c3)
                                myMotor4.setSpeed(c3)

				# left motors drive forward
				myMotor1.run(Adafruit_MotorHAT.FORWARD)
                                myMotor2.run(Adafruit_MotorHAT.FORWARD)
				# right motors drive backward
				myMotor3.run(Adafruit_MotorHAT.BACKWARD)
				myMotor4.run(Adafruit_MotorHAT.BACKWARD)

			# behaviour when js is pushed left
			if (number == LeftRightAxis) and (value < 0):
				print("left")
				# right motors at higher speed 
                                myMotor3.setSpeed(c2)
                                myMotor4.setSpeed(c2)
                                # left motors at lower speed 
                                myMotor1.setSpeed(c3)
                                myMotor2.setSpeed(c3)

                                # right motors drive forward 
                                myMotor3.run(Adafruit_MotorHAT.FORWARD)
                                myMotor4.run(Adafruit_MotorHAT.FORWARD)
                                # left motors drive backward 
                                myMotor1.run(Adafruit_MotorHAT.BACKWARD)
                                myMotor2.run(Adafruit_MotorHAT.BACKWARD)


	#wait before looping again
	TIME.sleep(0.01)

print('Turning off...')
