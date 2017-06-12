# imports from dc_realsense_test.py
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import logging
logging.basicConfig(level=logging.INFO)

import time as TIME
import numpy as np
import cv2
import pyrealsense as pyrs
import atexit

# From Adafruit MotorHat example code
# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x60)

# imports from controller_ex
import os, struct, array
from fcntl import ioctl

# import from basic_nav_functions to turn on RealSense camera
import pyrealsense as pyrs

# initialize variables from basic_nav_functions

# motor state variables set to zero
cs_m1 = 0
cs_m2 = 0
cs_m3 = 0
cs_m4 = 0

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

# -- MOTOR CONTROL FUNCTIONS

def simple_lowpass(v_current, v_des):
    # low pass filter to mitigate discontinuities in motor commands
    v_new = int(round(c0*v_current + c1*(v_des - v_current)))
    # watch out for negative numbers...
    return v_new


def motorControl(vdLeft, vdRight):
    # basic differential control function for the four wheel motors
    global cs_m1, cs_m2, cs_m3, cs_m4

    vd_vec = [vdRight, vdRight, vdLeft, vdLeft]
    motorspeeds = [cs_m1, cs_m2, cs_m3, cs_m4]

    # lowpass filtering may be overkill, these motors seem pretty robust
    for wi in range(1, 5):
        # check speed difference
        if abs(vd_vec[wi-1]-motorspeeds[wi-1]) < thresh:
            v_new = vd_vec[wi-1]

        else:
            v_new = simple_lowpass(motorspeeds[wi - 1], vd_vec[wi-1])

        mot = mh.getMotor(wi)

        if v_new < 0:
            mot.setSpeed(-1 * v_new)
            mot.run(Adafruit_MotorHAT.BACKWARD)
        else:
            mot.setSpeed(v_new)
            mot.run(Adafruit_MotorHAT.FORWARD)

        # update current motor speed
	motorspeeds[wi - 1] = v_new

# BEGIN SEQUENTIAL EXECUTION

#--Mmc gather controller information as done in controller_ex

# Iterate over the joystick devices.
print('Available devices:')
for fn in os.listdir('/dev/input'):
    if fn.startswith('js'):
        print('  /dev/input/%s' % fn)

# We'll store the states here.
axis_states = {}
button_states = {}

# Axis and button mapping are joystick-specific
# Joystick (DragonRise Inc.   Generic   USB  Joystick  ) has 7 axes (X, Y, Z, Rx, Ry, Hat0X, Hat0Y)
# and 12 buttons (Trigger, ThumbBtn, ThumbBtn2, TopBtn, TopBtn2, PinkieBtn, BaseBtn, BaseBtn2, BaseBtn3, BaseBtn4, BaseBtn5, BaseBtn6).

# Run jscal -q to see the address mappings. Current output:
# jscal -u 7,0,1,2,3,4,16,17,12,288,289,290,291,292,293,294,295,296,297,298,299 /dev/input/js0

# All axes and buttons are mapped to a number above. But we don't know which! the below takes a guess but could be totally off

axis_names = {
    0x00 : 'lateral',
    0x01 : 'y',
    0x04 : 'left-z',
    0x03 : 'vertical',
    0x02 : 'lx',
    0x07 : 'rudder',
    0x12 : 'hat1x',
    0x16 : 'hat3x',
    0x17 : 'hat3y',
}

button_names = {
    0x120: 'rup', #also triagnle
    0x121: 'rright', #also circle
    0x122: 'rdown', #also x
    0x123: 'rleft', #also square
    0x124: 'l2',
    0x125: 'r2',
    0x126: 'l1',
    0x127: 'r1',
}

axis_map = []
button_map = []

# Open the joystick device.
fn = '/dev/input/js0'
print('Opening %s...' % fn)
jsdev = open(fn, 'rb')

# Get the device name.

# Get number of axes and buttons.
buf = array.array('B', [0])
ioctl(jsdev, 0x80016a11, buf) # JSIOCGAXES
num_axes = buf[0]

buf = array.array('B', [0])
ioctl(jsdev, 0x80016a12, buf) # JSIOCGBUTTONS
num_buttons = buf[0]

# Get the axis map.
buf = array.array('B', [0] * 0x40)
ioctl(jsdev, 0x80406a32, buf) # JSIOCGAXMAP

for axis in buf[:num_axes]:
    axis_name = axis_names.get(axis, 'unknown(0x%02x)' % axis)
    axis_map.append(axis_name)
    axis_states[axis_name] = 0.0

# Get the button map.
buf = array.array('H', [0] * 200)
ioctl(jsdev, 0x80406a34, buf) # JSIOCGBTNMAP

for btn in buf[:num_buttons]:
    btn_name = button_names.get(btn, 'unknown(0x%03x)' % btn)
    button_map.append(btn_name)
    button_states[btn_name] = 0

print('{:d} axes found '.format(num_axes))

print('{:d} buttons found '.format(num_buttons))

# Go into driving motors with a loop

motorrunning = True

# Start RealSense camera
pyrs.start()
py_dev = pyrs.Device(device_id = 0, streams = [pyrs.ColourStream(fps = 30), pyrs.DepthStream(fps=30)])

# begin loop
while motorrunning:

	evbuf = jsdev.read(8)

	if evbuf:
		time, value, type, number = struct.unpack('IhBB', evbuf)

		if type & 0x80:
			print("(initial)")

		if type & 0x01:
			# turn off robot by exiting while loop
			off_button = 5
			if (number == off_button) and value:
				break

		if type & 0x02:
			right_js = 2
			r_axis = 0x02

			left_js = 3
			l_axis = 0x03

			if number == left_js:
				# get percentage of power coming to left motors
				percent_power = (value / 32767.0) * -1
				axis_states[l_axis] = percent_power
				print (percent_power)

				# set motor speed proportional to percentage (0-255)
				motor_val = int(percent_power * 255)

				myMotor3.setSpeed(motor_val)
                                myMotor4.setSpeed(motor_val)

				# select backwards or forwards due to sign
                                if motor_val < 0:
                                        myMotor3.run(Adafruit_MotorHAT.BACKWARD)
                                        myMotor4.run(Adafruit_MotorHAT.BACKWARD)
                                else:
                                        myMotor3.run(Adafruit_MotorHAT.FORWARD)
                                        myMotor4.run(Adafruit_MotorHAT.FORWARD)

			if number == right_js:
				# get percentage of power coming to right motors
                                percent_power = value / 32767.0
                                axis_states[r_axis] = percent_power
                                print (percent_power)

				# set motor speed proportional to percentage (0-255)
				motor_val = int(percent_power * 255)

				myMotor1.setSpeed(motor_val)
				myMotor2.setSpeed(motor_val)

				# select backwards or forwards due to sign
				if motor_val < 0:
					myMotor1.run(Adafruit_MotorHAT.BACKWARD)
					myMotor2.run(Adafruit_MotorHAT.BACKWARD)
				else:
					myMotor1.run(Adafruit_MotorHAT.FORWARD)
					myMotor2.run(Adafruit_MotorHAT.FORWARD)
	# wait before looping again
	TIME.sleep(0.01)

print("Turning off...")
