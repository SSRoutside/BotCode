# import current autonomous functions
from auto_capabilities import *

    # what is this? does this need to be in the function or at the
    # beginning of the main file or camera_init?
with pyrs.Service() as a:

    dev = pyrs.Device()

    #dev.apply_ivcam_preset(0)
    #dev.set_device_option(11, 1)
    #dev.set_device_option(10,1)
    #dev.set_device_option(31,1)

    cnt = 0
    last = time.time()
    smoothing = 0.9
    fps_smooth = 30

    def nothing(x):
        pass

    # initialize loop counter
    loop = 0

    # main driving loop
    while loop <= 1000:

        # initialize flags as False
        oneWall = False

        cone_present = False
        print("Restart Variable: " + str(cone_present))

        # determine if cone is in field of view
        cone_present = findCone(dev, cnt)

        # initialize flags as False
        oneWall = False

        # determine if wall exists
        oneWall = oneWallCheck()

        if oneWall == True:
            # gather all necessary information and components for wall following
            FRONT_TRIG, FRONT_ECHO, BACK_TRIG, BACK_ECHO, right, left, count, f_dist_frame, b_dist_frame, min_wall_skew, max_wall_skew, fb_skew = SetWallFollow()

            # run wall following decision loop
            WallFollow(FRONT_TRIG, FRONT_ECHO, BACK_TRIG, BACK_ECHO, right, left, count, f_dist_frame, b_dist_frame, min_wall_skew, max_wall_skew, fb_skew)

        else:
            # run randomWalk when there is no other information available
            randomWalk()

        loop += 1
        time.sleep(.25)
