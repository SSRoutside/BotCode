# Released by rdb under the Unlicense (unlicense.org)
# Based on information from:
# https://www.kernel.org/doc/Documentation/input/joystick-api.txt

#import motor_init.py from BotCode
from motor_init import *

import time as TIME
import struct
import fcntl
from fcntl import ioctl

import os, struct, array
from fcntl import ioctl

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

axis_names = {
    0x00 : 'axis0', # Binary L/R axis for 4-way button
    0x01 : 'axis1', # right joystick analog input L/R
    0x02 : 'axis2', # right joystick analog input U/D
    0x03 : 'axis3', # Binary U/D axis for 4-way button
}

button_names = {

    0x120 : 'but0',  # Triangle AND right joystick up/down
    0x121 : 'but1',  # Circle AND right joystick left/right
    0x122 : 'but2',  # Cross AND right joystick up/down
    0x123 : 'but3',  # Square AND right joystick left/right
    0x124 : 'but4',  # L2
    0x125 : 'but5',  # R2
    0x126 : 'but6',  # L1
    0x127 : 'but7',  # R1
    0x128 : 'but8',  # select
    0x129 : 'but9',  # start
    0x130 : 'but10',
    0x131 : 'but11', # analog - sends no event output
}

axis_map = []
button_map = []

# Open the joystick device.
fn = '/dev/input/js0'
print('Opening %s...' % fn)
jsdev = open(fn, 'rb')

# set to non-blocking!!!
flag = fcntl.fcntl(jsdev, fcntl.F_GETFD)
fcntl.fcntl(jsdev, fcntl.F_SETFL, flag | os.O_NONBLOCK)

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

# Main control loop
# The following code is event-based. That means the values are ONLY updated on change.

# It might be more intuitive to update all buttons/axes in a continuous loop.

# how this works: every time something is pressed on the joystick, it logs an EVENT
# in the EVENT QUEUE
# We continuously read from the event queue. HOWEVER this means that if a value isn't changed,
# we don't see it in the queue.

# It MAY be possible to poll joystick values continuously (check joystick API and maybe evdev API?)
# but in the meantime we can write code that APPEARS continuous even though it is event-based

running = True

# constant for weaker turning side (during static turn)
turning = .30
# threshold for both motors while executing dynamic turn
dynamic_turning = .50

# Observe that axis map and button map contain the CURRENT STATE of each axis.

while running:

    # To see a continuously updated list of the current values of all buttons and axes, uncomment the below

    # print current controller state:
    #for butt in button_map:
    #    print("{name} : {val} ".format(name=butt, val=button_states[butt]))

    #for ax in axis_map:
    #    print("{name} : {val} ".format(name=ax, val=axis_states[ax]))

    # Use current joystick state to control robot

    # Axis 2 is the only analog axis BUT can act as 2 axes by combining with buttons
    # Axis 2 can be controlled by:
    # L/R on left toggle
    # U/D on right toggle (this also toggles the states of buttons 0 or 2)

    # Example code:

    # get value from axis 2
    ax2 = axis_map[2]
    ax2val = axis_states[ax2]

    # check button states
    butt0 = button_map[0]
    butt2 = button_map[2]
    butt4 = button_map[4] # brake button (left 2)
    butt6 = button_map[6] # off button (left 1)
    butt5 = button_map[5] # backward turn button (right 2)
    butt7 = button_map[7] # forward turn button (right 1)

    # There are several methods to determine which combination of button/axes has been set!
    # this is just one example

    # hit r2 and l2 as a "kill switch"
    if (button_states[butt4] and button_states[butt5]):
	break

    elif button_states[butt6]:
	myMotor1.setSpeed(0)
	myMotor2.setSpeed(0)
	myMotor3.setSpeed(0)
        myMotor4.setSpeed(0)

	myMotor1.run(Adafruit_MotorHAT.FORWARD)
	myMotor2.run(Adafruit_MotorHAT.FORWARD)
	myMotor3.run(Adafruit_MotorHAT.FORWARD)
        myMotor4.run(Adafruit_MotorHAT.FORWARD)

    elif (button_states[butt0] or button_states[butt2]):
	# eliminate noise from joystick
	if abs(ax2val) < .05:
	    myMotor1.setSpeed(0)
            myMotor2.setSpeed(0)
            myMotor3.setSpeed(0)
            myMotor4.setSpeed(0)

	else:
	    #get motor value based on percent and set speed
	    mv = getMotorValue(ax2val)
	    myMotor1.setSpeed(mv*4)
	    myMotor2.setSpeed(mv*4)
	    myMotor3.setSpeed(mv*4)
	    myMotor4.setSpeed(mv*4)

        # we should be moving forwards or backwards
        if ax2val > 0:
            print("Going backwards at {} ".format(ax2val))
	    # drive backwards
	    myMotor1.run(Adafruit_MotorHAT.BACKWARD)
	    myMotor2.run(Adafruit_MotorHAT.BACKWARD)
	    myMotor3.run(Adafruit_MotorHAT.BACKWARD)
            myMotor4.run(Adafruit_MotorHAT.BACKWARD)

        elif ax2val < 0:
            print ("Going forwards at {} ".format(ax2val))
	    mv = getMotorValue(ax2val*-1)
            myMotor1.setSpeed(mv*4)
            myMotor2.setSpeed(mv*4)
            myMotor3.setSpeed(mv*4)
            myMotor4.setSpeed(mv*4)

	    # drive forwards
	    myMotor1.run(Adafruit_MotorHAT.FORWARD)
            myMotor2.run(Adafruit_MotorHAT.FORWARD)
	    myMotor3.run(Adafruit_MotorHAT.FORWARD)
            myMotor4.run(Adafruit_MotorHAT.FORWARD)


    else: # we should be turning left or right
	# eliminate noise from joystick
        if abs(ax2val) < .05:
            myMotor1.setSpeed(0)
            myMotor2.setSpeed(0)
            myMotor3.setSpeed(0)
            myMotor4.setSpeed(0)

	    myMotor1.run(Adafruit_MotorHAT.FORWARD)
            myMotor2.run(Adafruit_MotorHAT.FORWARD)
            myMotor3.run(Adafruit_MotorHAT.FORWARD)
            myMotor4.run(Adafruit_MotorHAT.FORWARD)


	# if right 1 and joystick pressed left, turn left and move forward
	elif (button_states[butt7] and (ax2val < 0)):
	    # set low motor value to threshold
	    lowmv = getMotorValue(dynamic_turning)

	    print("Forward and left at {} ".format(ax2val))
	    # set high motor value to a value above threshold proportional
	    # to the joysick value, otherwise set it to the threshold
	    # value
	    if ((ax2val * -1) > dynamic_turning):
		highmv = getMotorValue(ax2val * -1)
	    else:
		highmv = lowmv

	    # left motors at lower speed and right motors at highter speed
	    # if the joystick is pushed further than threshold
            myMotor1.setSpeed(highmv)
            myMotor2.setSpeed(lowmv)
            myMotor3.setSpeed(highmv)
            myMotor4.setSpeed(lowmv)

	    # run all motors forward
	    myMotor1.run(Adafruit_MotorHAT.FORWARD)
	    myMotor2.run(Adafruit_MotorHAT.FORWARD)
            myMotor3.run(Adafruit_MotorHAT.FORWARD)
	    myMotor4.run(Adafruit_MotorHAT.FORWARD)

	# if right 2 and joystick pressed left, turn left and move backward
        elif (button_states[butt5] and (ax2val < 0)):
            # set low motor value to threshold
            lowmv = getMotorValue(dynamic_turning)

            print("Backward and left at {} ".format(ax2val))

            # set high motor value to a value above threshold proportional
            # to the joysick value, otherwise set it to the threshold
            # value
            if ((ax2val * -1) > dynamic_turning):
                highmv = getMotorValue(ax2val * -1)
            else:
                highmv = lowmv

            # left motors at lower speed and right motors at highter speed
            # if the joystick is pushed further than threshold
            myMotor1.setSpeed(highmv)
            myMotor2.setSpeed(lowmv)
            myMotor3.setSpeed(highmv)
            myMotor4.setSpeed(lowmv)

            # run all motors backward
            myMotor1.run(Adafruit_MotorHAT.BACKWARD)
            myMotor2.run(Adafruit_MotorHAT.BACKWARD)
            myMotor3.run(Adafruit_MotorHAT.BACKWARD)
            myMotor4.run(Adafruit_MotorHAT.BACKWARD)

	# if right 1 and joystick pressed right, turn right and move forward
        elif (button_states[butt7] and (ax2val > 0)):
            # set low motor value to threshold
            lowmv = getMotorValue(dynamic_turning)

            print("Forward and right at {} ".format(ax2val))

            # set high motor value to a value above threshold proportional
            # to the joysick value, otherwise set it to the threshold
            # value
            if (ax2val > dynamic_turning):
                highmv = getMotorValue(ax2val)
            else:
                highmv = lowmv

            # right motors at lower speed and left motors at highter speed
            # if the joystick is pushed further than threshold
            myMotor1.setSpeed(lowmv)
            myMotor2.setSpeed(highmv)
            myMotor3.setSpeed(lowmv)
            myMotor4.setSpeed(highmv)

            # run all motors forward
            myMotor1.run(Adafruit_MotorHAT.FORWARD)
            myMotor2.run(Adafruit_MotorHAT.FORWARD)
            myMotor3.run(Adafruit_MotorHAT.FORWARD)
            myMotor4.run(Adafruit_MotorHAT.FORWARD)

	# if right 2 and joystick pressed right, turn right and move backward
        elif (button_states[butt5] and (ax2val > 0)):
            # set low motor value to threshold
            lowmv = getMotorValue(dynamic_turning)

            print("Backward and right at {} ".format(ax2val))

            # set high motor value to a value above threshold proportional
            # to the joysick value, otherwise set it to the threshold
            # value
            if (ax2val > dynamic_turning):
                highmv = getMotorValue(ax2val)
            else:
                highmv = lowmv

            # right motors at lower speed and left motors at highter speed
            # if the joystick is pushed further than threshold
            myMotor1.setSpeed(lowmv)
            myMotor2.setSpeed(highmv)
            myMotor3.setSpeed(lowmv)
            myMotor4.setSpeed(highmv)

            # run all motors forward
            myMotor1.run(Adafruit_MotorHAT.BACKWARD)
            myMotor2.run(Adafruit_MotorHAT.BACKWARD)
            myMotor3.run(Adafruit_MotorHAT.BACKWARD)
            myMotor4.run(Adafruit_MotorHAT.BACKWARD)


        elif ax2val < 0:
	    # turn left
            print("Turning left at {} ".format(ax2val))
	    highmv = getMotorValue(ax2val * -1)
	    lowmv = getMotorValue(turning)

	    # left motors at lower speed and right motors at highter speed
	    myMotor1.setSpeed(highmv)
	    myMotor2.setSpeed(lowmv)
	    myMotor3.setSpeed(highmv)
            myMotor4.setSpeed(lowmv)

	    # run left motors backwards and right motors forwards
	    myMotor1.run(Adafruit_MotorHAT.FORWARD)
	    myMotor2.run(Adafruit_MotorHAT.BACKWARD)
	    myMotor3.run(Adafruit_MotorHAT.FORWARD)
            myMotor4.run(Adafruit_MotorHAT.BACKWARD)

        elif ax2val > 0 :
	    # turn right
            print("Turning right at {} ".format(ax2val))
	    highmv = getMotorValue(ax2val)
	    lowmv = getMotorValue(turning)

	    # right motors at lower speed and left motors at highter speed
            myMotor1.setSpeed(lowmv)
            myMotor2.setSpeed(highmv)
	    myMotor3.setSpeed(lowmv)
            myMotor4.setSpeed(highmv)

	    # run right motors backwards and left motors forwards
	    myMotor1.run(Adafruit_MotorHAT.BACKWARD)
            myMotor2.run(Adafruit_MotorHAT.FORWARD)
            myMotor3.run(Adafruit_MotorHAT.BACKWARD)
            myMotor4.run(Adafruit_MotorHAT.FORWARD)

        else:
            # axis is at 0, should we stop??
            print("Here is a good spot to stop")

    # Things to think about:
    # how can we change between turning on the spot and turning while moving forward or back?
    # what other controls might be useful?

    # check if anything has hit the event queue
    try:
            # read
            evbuf = jsdev.read(8)
            if evbuf:
                time, value, intype, number = struct.unpack('IhBB', evbuf)

                if intype & 0x01:
                    button = button_map[number]
                    if button:
                        button_states[button] = value

                if intype & 0x02:
                    axis = axis_map[number]
                    if axis:
                        fvalue = value / 32767.0
                        axis_states[axis] = fvalue

    except:
        pass

print("Code stopping...")
