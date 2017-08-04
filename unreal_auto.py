# import current autonomous functions
from auto_capabilities import *

# main driving loop
loop = 0
while loop <= 1000:

    # initialize flags as False
    oneWall = False

    # determine if wall exists
    oneWall = oneWallCheck()


    if oneWall == True:
        print("****** WallFollow")
        # get variables needed to run WallFollowing from setup function
        FRONT_TRIG, FRONT_ECHO, BACK_TRIG, BACK_ECHO, right, left, count, f_dist_frame, b_dist_frame, min_wall_skew, max_wall_skew, fb_skew = SetWallFollow()
        print("left: " + str(left))
        print("right: " + str(right))
        # run WallFollow using those same variables.
        WallFollow(FRONT_TRIG, FRONT_ECHO, BACK_TRIG, BACK_ECHO, right, left, count, f_dist_frame, b_dist_frame, min_wall_skew, max_wall_skew, fb_skew)


    else:
        print("****** RandomWalk")
        randomWalk()


turnOffMotors()
