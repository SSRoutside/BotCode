# import current autonomous functions
from auto_capabilities import *

# get all variables needed to run WallFollow
FRONT_TRIG, FRONT_ECHO, BACK_TRIG, BACK_ECHO, right, left, count, f_dist_frame, b_dist_frame, min_wall_skew, max_wall_skew, fb_skew = SetWallFollow

# main driving loop
while True:

    # determine if cone is in field of view
    cone_present = findCone()

    if cone_present:
        # enter motor commands that navigate in the direction of the cone.
        # for now, this is straigt, but it should be determined by the angle
        # to the centroid of the cone.
        setAndDriveLeft(1.0, True)
        setAndDriveRight(1.0, True)

    #### should there be centering before wall following if two walls?

    elif oneWallCheck():
        # run the wall following routine
        WallFollow(FRONT_TRIG, FRONT_ECHO, BACK_TRIG, BACK_ECHO, right, left, count, f_dist_frame, b_dist_frame, min_wall_skew, max_wall_skew, fb_skew)


    else: 
        # should maneuver randomly throughout "open" space
        randomWalk()
