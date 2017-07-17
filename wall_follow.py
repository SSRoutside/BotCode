# imports to run sonar and drive motors
import numpy as np
from motor_init import *
from sonar_init import *

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
print(f_dist_frame)
print(b_dist_frame)

# begin main while loop
while count <= 1000:

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

        # determine if the front and back are aligned
        fb_align = f_dist_av - b_dist_av

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
            SetAndDriveRigt(.80, True)
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

        # making it to this point means distance is good, but alignment is not
        # Priority 2: align the robot to drive straight
        elif (align_back and right) or (align_front and left):
            # commands similar to static turn back and left
            SetAndDriveRight(.90, False)
            SetAndDriveLeft(.30, True)
            print('pivoting left')

        elif (align_front and right) or (align_back and left):
            # commands similar to static turn back and right
            SetAndDriveRight(.30, True)
            SetAndDriveLeft(.90, False)
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


print(front_log)
print(back_log)
