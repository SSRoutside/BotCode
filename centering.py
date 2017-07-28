# imports to run sonar and drive motors
from motor_init import *
from sonar_init import *
from Ptest import *

# initialize loop count
count = 1
# initialize arrays that will store distances to be averaged and smoothed
rf_dist_frame = np.zeros((1,10))
lf_dist_frame = np.zeros((1,10))
rb_dist_frame = np.zeros((1,10))
lb_dist_frame = np.zeros((1,10))
# initialize acceptable off-center error and front/back distances
center_error = 10 # maybe we could eventually make this proportional to gap size???
fb_skew = 5
# initialize log lists for recording all distance measurements
rf_log = []
lf_log = []
rb_log = []
lb_log = []

# begin main while loop
while count <= 400:

    mod_num = count % 10

    # get all distances
    rf_dist = getDist(RF_TRIG, RF_ECHO)
    lf_dist = getDist(LF_TRIG, LF_ECHO)
    rb_dist = getDist(RB_TRIG, RB_ECHO)
    lb_dist = getDist(LB_TRIG, LB_ECHO)

    # make drive decisions every 10 loops
    if mod_num == 0:
        # save distances in last array spaces
        rf_dist_frame[0:9] = rf_dist
        lf_dist_frame[0:9] = lf_dist
        rb_dist_frame[0:9] = rb_dist
        lb_dist_frame[0:9] = lb_dist

        # use weighted average on each frame to determine average distance
        rf_dist_av = np.average(rf_dist_frame)
        lf_dist_av = np.average(lf_dist_frame)
        rb_dist_av = np.average(rb_dist_frame)
        lb_dist_av = np.average(lb_dist_frame)

        # append log lists
        rf_log.append(rf_dist_av)
        lf_log.append(lf_dist_av)        
        rb_log.append(rb_dist_av)
        lb_log.append(lb_dist_av)

        # determine an overall average for each side
        right_av = rf_dist_av + rb_dist_av
        left_av = lf_dist_av + lb_dist_av

        # find the difference of the averages
        side_dif = right_av - left_av

        # determine if the robot is too far off center
        if abs(side_dif) >= center_error:
            centered = False

            # determine which side is closer to each object
            if side_dif > 0:
                # means the robot is closer to the right object
                right = True
                left = False

            else:
                # means robot is closer to the left object
                left = True
                right = False

        else:
            # means the robot is close enough to the center
            centered = True
            left = False
            right = False

        # determine if the robot is aligned
        fb_align = rf_dist_av - rb_dist_av ## CHANGE IF LEFT DISTS ARE BETTER

        if abs(fb_align) >= fb_skew:
            # The robot is not aligned
            align_check = False

        else:
            # The robot is aligned
            align_check = True

######## motor commands

        if centered and align_check:
            # both are good, so drive straight
            SetAndDriveRight(.80, True)
            SetAndDriveLeft(.80, True)
            print('driving straight')

    ##### all checks below this point mean adjustments must be made
        # Priority 1: fix distance to wall
        elif left or right:
            centeringPcontrol(left_av, right_av)

        elif not align_check:
            # commands similar to static turn back and left
            SetAndDriveRight(.90, True)
            SetAndDriveLeft(.10, True)
            print('pivoting left')

    # otherwise, just update the distance frames
    else:
        # save distances into resepctive arrays 
        rf_dist_frame[0:mod_num - 1] = rf_dist
        lf_dist_frame[0:mod_num - 1] = lf_dist
        rb_dist_frame[0:mod_num - 1] = rb_dist
        lb_dist_frame[0:mod_num - 1] = lb_dist

    # append count
    count += 1

    # wait to loop, determined by maximum possible length of sonar signal
    time.sleep(0.025)

print("RF LOG:")
print(rf_log)
print("LF LOG:")
print(lf_log)
print ("RB LOG:")
print(rb_log)
print("LB LOG:")
print(lb_log)
