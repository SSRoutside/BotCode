from motor_init import *
from sonar_init import *
import numpy as np
import random, decimal

## camera init stuf: SHOULD BE INIT FILE SOON
import cv2
import pyrealsense as pyrs
import os
import datetime
import cone_detection
from matplotlib import pyplot as plt

########## start auto functions ############

def findCone(dev, cnt):
        print("starting cone detection")


#if you get a true value it updates counter, if it is false
# it resets and once it reaches a threshold
# or look at every fifth frame

        # while True:

        cnt += 1
        if (cnt % 10) == 0:
                now = time.time()
                dt = now - last
                fps = 10/dt
                fps_smooth = (fps_smooth * smoothing) + (fps * (1.0 -smoothing))
                last = now

        dev.wait_for_frames()

        c = dev.color
        rgb_im = cv2.cvtColor(c, cv2.COLOR_RGB2BGR)

        rgb_im, cone_present = cone_detection.find_cone(rgb_im)

        cv2.imshow('', rgb_im)

        return cone_present


def SetWallFollow():
    print("setting wall follow")
# This function runs all of the commands needed before the wall following decisions can be
# made in the main autonomous while loop. It will return all of the variables necessary to
# run

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
##    #front_log = []
##    #back_log = []

    # we may not need all of these variables
    return FRONT_TRIG, FRONT_ECHO, BACK_TRIG, BACK_ECHO, right, left, count, f_dist_frame, b_dist_frame, min_wall_skew, max_wall_skew, fb_skew

def WallFollow(FRONT_TRIG, FRONT_ECHO, BACK_TRIG, BACK_ECHO, right, left, count, f_dist_frame, b_dist_frame, min_wall_skew, max_wall_skew, fb_skew):
    print("executing wall follow")
# This function is used in the main autonomous loop to make driving decisions using the
# same method as wall_follow.py

    # reset turn count to zero
    turn_count = 0

    mod_num = count % 10

    # record distances from FRONT and BACK 
    f_dist = getDist(FRONT_TRIG, FRONT_ECHO)
    b_dist = getDist(BACK_TRIG, BACK_ECHO)

    # make drive decisions every 10 loops
    if mod_num == 0:
        # save distances in the last space in the array
        f_dist_frame[0:9] = f_dist
        b_dist_frame[0:9] = b_dist

        # use weighted average on each frame to determine average distance
        f_dist_av = np.average(f_dist_frame)
        b_dist_av = np.average(b_dist_frame)

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

        # determine distance between front and back sensors on wall side
        fb_align = f_dist_av - b_dist_av

        # determine if the robot could possibly turn a corner by detecting a large
        # measurement for fb_align
        if fb_align >= 100:
            corner = True

        else:
            corner = False

        if abs(fb_align) <= fb_skew:
            # the robot is aligned properly
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
            SetAndDriveRight(.80, True)
            SetAndDriveLeft(.80, True)
            print('driving straight')

    ##### all checks below this point mean adjustments must be made
        # Priority 1: fix distance to wall
        elif (too_close and right) or (too_far and left):
            # commands similar to dynamic turn to the left
            SetAndDriveRight(.90, True)
            SetAndDriveLeft(.30, True)
            print('correcting to left')

        elif (too_far and right) or (too_close and left):
            # commands similar to dynamic turn to the right
            SetAndDriveRight(.30, True)
            SetAndDriveLeft(.90, True)
            print('correcting to right')

        # Priority 2: turning a corner if one is detected
        # LENGTH OF TURN SHOULD BE ADJUSTED:
        # maybe the camera could be used to determine angle also.
        elif (corner and right):
            while turn_count < 10:
                # commands similar to harder dynamic turn to the right
                SetAndDriveRight(.20, True)
                SetAndDriveLeft(1.0, True)
                print('Turing Conrner: Right')

                # append turn_count
                turn_count += 1

                # wait: same as drive loop for simplicity
                time.sleep(0.025)

        elif (corner and left):
            while turn_count < 10:
                # commands similar to harder dynamic turn to the left
                SetAndDriveLeft(.20, True)
                SetAndDriveRight(1.0, True)
                print('Turing Conrner: Right')

                # append turn_count
                turn_count += 1

                # wait: same as drive loop for simplicity
                time.sleep(0.025)

        # making it to this point means distance is good, but alignment is not
        # Priority 3: align the robot to drive straight
        elif (align_back and right) or (align_front and left):
            # commands similar to static turn left
            SetAndDriveRight(.90, True)
            SetAndDriveLeft(.10, True)
            print('pivoting left')

        elif (align_front and right) or (align_back and left):
            # commands similar to static turn right
            SetAndDriveRight(.10, True)
            SetAndDriveLeft(.90, True)
            print('pivoting right')

######## end motor command section

    # ohterwise, just update the distance frames
    else:
        # save distances into resepctive arrays 
        f_dist_frame[0:mod_num - 1] = f_dist
        b_dist_frame[0:mod_num - 1] = b_dist

    # append count
    count += 1

    # wait to loop, determined by maximum possible length of sonar signal
    time.sleep(0.025)

def findWall(TRIG, ECHO):

    # initialize distance list, wall boolean, and loop conter (i)
    d_list = []
    i = 0
    wall = False

    while i <= 3:
        # get measurements from the left and right front sensors
        # append them to lists
        d_list.append(getDist(TRIG, ECHO))

        # increment count
        i += 1

    # average all of the numbers in each list
    d_av = np.mean(d_list)

    if d_av <= 400:
        # shows that there's a wall w/in 4m or less
        wall = True

    return wall


def oneWallCheck():
    # checks for a wall to one side of the robot
    rightWall = findWall(RF_TRIG, RF_ECHO)
    leftWall = findWall(LF_TRIG, LF_ECHO)

    return(rightWall or leftWall)

def twoWallCheck():
    # checks if there's a wall on both sides of the robot
    rightWall = findWall(RF_TRIG, RF_ECHO)
    leftWall = findWall(LF_TRIG, LF_ECHO)

    return(rightWall and leftWall)

def randomWalk():
    # initialize variables to be used to determine a "random"
    # direction and a random amount of time to drive a certain direction.
    time_constant = 5 ## might need to change
    turn_constant = 2 ## might need to change
    # will return 1 or 0
    random_direction = random.randint(0, 1) 
    # will return number between 0 and 1
    time_decimal = decimal.Decimal(random.random())
    turn_decimal = decimal.Decimal(random.random())

    # calculate time based on time_constant and random decimal (between 5 and 10 seconds)
    t = time_constant + (time_constant * time_decimal)

    # calculate length of turn based on time_constant and random decimal (between 2 and 4 seconds)
    turn = turn_constant + (turn_constant * turn_decimal)

    if random_direction == 1:
        # turn to the right
        SetAndDriveRight(.10, True)
        SetAndDriveLeft(.90, True)
        print('pivoting right')

        # continue in that direction for randomly determined time
        time.sleep(turn)

    else:
        # turn to the left
        SetAndDriveRight(.90, True)
        SetAndDriveLeft(.10, True)
        print('pivoting left')

        # continue in that direction for randomly determined time
        time.sleep(turn)

    # drive forward for specified amount of time
    SetAndDriveRight(.80, True)
    SetAndDriveLeft(.80, True)
    print('driving straight')

    # continue in that direction for randomly determined time
    time.sleep(t)
