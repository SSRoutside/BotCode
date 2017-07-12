# imports to run sonar and drive motors
import mraa
import time
import numpy as np
from motor_init import *

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

LB_TRIG = mraa.Gpio(23)
LB_ECHO = mraa.Gpio(24)

# set trigger pins an output pins and echo pins as input pins
RF_TRIG.dir(mraa.DIR_OUT)
RF_ECHO.dir(mraa.DIR_IN)

LF_TRIG.dir(mraa.DIR_OUT)
LF_ECHO.dir(mraa.DIR_IN)

RB_TRIG.dir(mraa.DIR_OUT)
RB_ECHO.dir(mraa.DIR_IN)

LB_TRIG.dir(mraa.DIR_OUT)
LB_ECHO.dir(mraa.DIR_IN)

# set trigger pins low
RF_TRIG.write(0)
LF_TRIG.write(0)
RB_TRIG.write(0)
LB_TRIG.write(0)

# wait for sensors to settle (ensures low setting)
print("Waiting For Sensor To Settle")
time.sleep(2)
print("done waiting")

# get distances from both front sensors
##### WHAT HAPPENS IF A WALLL ISN'T SEEN ON ONE OR BOTH SIDES?
d_right = getDist(RF_TRIG, RF_ECHO)
d_left = getDist(LF_TRIG, LF_ECHO)

# decide to follow the closest wall and begin using distances corresponding to 
# the closest wall
if d_right >= d_left:
    # set FRONT and BACK elements to correspond with the side facing the left wall
    FRONT_TRIG = LF_TRIG
    FRONT_ECHO = LF_ECHO
    BACK_TRIG = LB_TRIG
    BACK_ECHO = LB_ECHO

    # boolean indicating left side is being used
    left = True
    right = False

else:
    # set FRONT and BACK elements to correspond with the side facing the right wall
    FRONT_TRIG = RF_TRIG
    FRONT_ECHO = RF_ECHO
    BACK_TRIG = RB_TRIG
    BACK_ECHO = RB_ECHO

    # boolean indicating right side is being used
    right = True
    left = False

# initialize loop count 
count = 1
# initialize arrays that will store distances to be averaged/smoothed
f_dist_frame = np.zeros((1,10))
b_dist_frame = np.zeros((1,10))
# initilize acceptable error ranges for front/back distances
# and distance to wall
min_wall_skew = 15
max_wall_skew = 25
fb_skew = 5 # SHOULD PROBABLY BE NARROWED
# initialize log lists for recording all distance measurements
front_log = []
back_log = []

# check frames to see if they look as expected
print(FRONT_dist_frame)
print(BACK_dist_frame)

# begin main while loop
while count <= 400:

    mod_num = count % 10

    # record distances from FRONT and BACK 
    f_dist = getDist(FRONT_TRIG, FRONT_ECHO)
    b_dist = getDist(BACK_TRIG, BACK_ECHO)

    # make drive decisions every 10 loops
    if mod_num == 0:
        # save distances in the last space in the array
        f_dist_frame[9] = f_dist
        b_dist_frame[9] = b_dist

        # use weighted average on each frame to determine average distance
        f_dist_av = np.average(f_dist_frame, range(1,10), weights=range(1,10))
        b_dist_av = np.average(b_dist_frame, range(1,10), weights=range(1,10))

        # append log lists
        front_log.append(f_dist_av)
        back_log.append(b_dist_av)

        # check distance averages to see if they're reasonable
        print(f_dist_av)
        print(b_dist_av)

        # determine if the robot is close enough to the wall
        if (f_dist_av >= min_wall_skew) and (f_dist_av <= max_wall_skew):
            wall_check = True
            too_far = False
            too_close = False

        else:
            wall_check = False

            # determine if the robot is too close or too far from the wall
            # boolean variables will be set to determine future motion
            if f_dist_av > max_wall_skew: # means further from wall, must move closer
                too_far = True
                too_close = False

            else: # means too close to wall, must move away
                too_far = False
                too_close = True

        # determine if the front and back are aligned
        fb_align = f_dist_av - b_dist_av

        if abs(fb_align) <= fb_skew:
            align_check = True
            align_back = False
            align_front = False

        else:
            align_check = False

            # determine which side is misaligned due to the sign of fb_align
            # used in deciding to adjust towards the outer side
            if align_check > 0: # means front is further from wall
                #means back should be aligned
                align_back = True
                align_front = False

            else: # means back is further from wall
                # means front should be aligned
                align_back = False
                align_front = True


######## decisions translated to motor commands

        # both are good, so simply drive forward
        if wall_check and align_check:
            setAndDriveRigt(.80, True)
            setAndDriveLeft(.80, True)

    ##### all checks below this point mean adjustments must be made
        # Priority 1: fix distance to wall
        elif (too_close and right) or (too_far and left):
            # commands similar to dynamic turn to the left
            setAndDriveRight(.50, True)
            setAndDriveLeft(.90, True)

        elif (too_far and right) or (too_close and left):
            # commands similar to dynamic turn to the right
            setAndDriveRight(.90, True)
            setAndDriveLeft(.50, True)

        # making it to this point means distance is good, but alignment is not
        # Priority 2: align the robot to drive straight
        elif (align_back and right) or (align_front and left):
            # commands similar to static turn back and left
            setAndDriveRight(.90, False)
            setAndDriveLeft(.30, True)

        elif (align_front and right) or (align_back and left):
            # commands similar to static turn back and right
            setAndDriveRight(.30, True)
            setAndDriveLeft(.90, False)

######## end motor command section

    # ohterwise, just update the distance frames
    else:
        # save distances into resepctive arrays 
        f_dist_frame[mod_num - 1] = f_dist
        b_dist_frame[mod_num - 1] = b_dist
        
    # append count
    count += 1

    # wait to loop, determined by maximum possible length of sonar signal
    time.sleep(0.025)


print(front_log)
print(back_log)
