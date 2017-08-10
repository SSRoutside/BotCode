import sonar_init as SI
import Ptest
import numpy as np
import random
import time

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

def makeWFArray(FRONT_TRIG, FRONT_ECHO, BACK_TRIG, BACK_ECHO, f_dist_frame, b_dist_frame):
# makes and returns arrays of disances to be used in WallFollow function

    # sample 10 distances, and average them
    for i in range(0, 10):
        # record distances from FRONT and BACK
        f_dist = SI.getDist(FRONT_TRIG, FRONT_ECHO)
        b_dist = SI.getDist(BACK_TRIG, BACK_ECHO)

        # save distances into resepctive arrays 
        f_dist_frame[0:i] = f_dist
        b_dist_frame[0:i] = b_dist

        time.sleep(.025)

    # determine average distance by averaging the elements in each frame
    f_dist_av = np.average(f_dist_frame)
    b_dist_av = np.average(b_dist_frame)

    return f_dist_av, b_dist_av

def wallFollow():
# This function runs all of the commands needed before the wall following decisions can be
# made in the main autonomous while loop. It will return all of the variables necessary to
# run

    # get sonar objects
    RF_TRIG, RF_ECHO, LF_TRIG, LF_ECHO, RB_TRIG, RB_ECHO, LB_TRIG, LB_ECHO = SI.setSonar()

    # get distances from both front sensors
    ##### WHAT HAPPENS IF A WALLL ISN'T SEEN ON ONE OR BOTH SIDES?
    d_right = SI.getDist(RF_TRIG, RF_ECHO)
    d_left = SI.getDist(LF_TRIG, LF_ECHO)

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

    # initialize arrays that will store distances to be averaged/smoothed
    f_dist_frame = np.zeros((1,10))
    b_dist_frame = np.zeros((1,10))
    # initilize acceptable error ranges for front/back distances
    # and distance to wall
    min_wall_skew = 35
    max_wall_skew = 45
    fb_skew = 5 # SHOULD PROBABLY BE NARROWED
    # initialize log lists for recording all distance measurements
##    #front_log = []
##    #back_log = []

    # call function to obtain front and back distance averages
    f_dist_av, b_dist_av = makeWFArray(FRONT_TRIG, FRONT_ECHO, BACK_TRIG, BACK_ECHO, f_dist_frame, b_dist_frame)

    # append log lists
##    front_log.append(f_dist_av)
##   back_log.append(b_dist_av)

    # check distance averages to see if they're reasonable
    print("FRONT DISTANCE: " + str(f_dist_av))
    print("BACK DISTANCE: " + str(b_dist_av))
 
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
        rightMV = 204
        rightF = True
        leftMV = 204
        rightF = True

        print('driving straight')

##### all checks below this point mean adjustments must be made

    # Priority 1: fix distance to wall using proportional control
    elif too_close or too_far:
        # get arguments for motor commands from proportional control function
        leftMV, leftF, rightMV, rightF = Ptest.wallPcontrol(f_dist_av, 20, left, right)

    # Priority 2: turning a corner if one is detected
    # LENGTH OF TURN SHOULD BE ADJUSTED:
    # MOTOR VALUES MAY NEED TO BE ADJUSTED (esp weak side)
    # maybe the camera could be used to determine angle also.
    elif (corner and right):
        # commands similar to harder dynamic turn to the right
        rightMV = 90
        rightF = True
        leftMV = 255
        leftF = True
        print('Turning Corner: Right')

        # set loop and sleep args to loop turn command 10 times
        # loop number may need to change!
        # sleep same as main loop sleep
        loop = 10
        sleep = .25
        print('Turning Corner: Left')

    elif (corner and left):
        # commands similar to harder dynamic turn to the left
        rightMV = 255
        rightF = True
        leftMV = 90
        leftF = True

        # set loop and sleep args to loop turn command 10 times
        # loop number may need to change!
        # sleep same as main loop sleep
        loop = 10
        print('Turning Corner: Left')

    # making it to this point means distance is good, but alignment is not
    # Priority 3: align the robot to drive straight
    elif (align_back and right) or (align_front and left):
        # commands similar to static turn left
        rightMV = 230
        rightF = True
        leftMV = 25
        leftF = True
        print('pivoting left')

    elif (align_front and right) or (align_back and left):
        # commands similar to static turn right
        rightMV = 25
        rightF = True
        leftMV = 230
        leftF = True
        print('pivoting right')

    # return motor values and directions... designed to update about every .25 seconds
    return rightMV, rightF, leftMV, leftF

######## end motor command section

def findWall(TRIG, ECHO):

    # initialize distance list, wall boolean, and loop conter (i)
    d_list = []
    i = 0
    wall = False

    while i <= 3:
        # get measurements from the left and right front sensors
        # append them to lists
        d_list.append(SI.getDist(TRIG, ECHO))

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

    # get sonar objects
    RF_TRIG, RF_ECHO, LF_TRIG, LF_ECHO, RB_TRIG, RB_ECHO, LB_TRIG, LB_ECHO = SI.setSonar()

    rightWall = findWall(RF_TRIG, RF_ECHO)
    leftWall = findWall(LF_TRIG, LF_ECHO)

    return(rightWall or leftWall)

def twoWallCheck():
    # checks if there's a wall on both sides of the robot

    # get sonar objects
    RF_TRIG, RF_ECHO, LF_TRIG, LF_ECHO, RB_TRIG, RB_ECHO, LB_TRIG, LB_ECHO = SI.setSonar()

    rightWall = findWall(RF_TRIG, RF_ECHO)
    leftWall = findWall(LF_TRIG, LF_ECHO)

    return(rightWall and leftWall)
