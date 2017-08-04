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

#   # get all variables needed to run WallFollow
#    FRONT_TRIG, FRONT_ECHO, BACK_TRIG, BACK_ECHO, right, left, count, f_dist_frame, b_dist_frame, min_wall_skew, max_wall_skew, fb_skew = SetWallFollow()

    # main driving loop
    loop = 0
    while loop <= 1000:

<<<<<<< HEAD
=======
        # initialize flags as False
        oneWall = False
>>>>>>> driveTest
        cone_present = False
        print("Restart Variable: " + str(cone_present))

        # determine if cone is in field of view
        cone_present = findCone(dev, cnt)

<<<<<<< HEAD
=======
        # determine if wall exists
        oneWall = oneWallCheck

>>>>>>> driveTest
        if cone_present == True:
            # enter motor commands that navigate in the direction of the cone.
            # for now, this is straigt, but it should be determined by the angle
            # to the centroid of the cone.
            print("This is my variable: " + str(cone_present))
            SetAndDriveLeft(1.0, True)
            SetAndDriveRight(1.0, True)

        #### should there be centering before wall following if two walls?

<<<<<<< HEAD
        else:
=======
        elif oneWall == True:
>>>>>>> driveTest
            FRONT_TRIG, FRONT_ECHO, BACK_TRIG, BACK_ECHO, right, left, count, f_dist_frame, b_dist_frame, min_wall_skew, max_wall_skew, fb_skew = SetWallFollow()

            WallFollow(FRONT_TRIG, FRONT_ECHO, BACK_TRIG, BACK_ECHO, right, left, count, f_dist_frame, b_dist_frame, min_wall_skew, max_wall_skew, fb_skew)

<<<<<<< HEAD
=======
        else:
            randomWalk()

>>>>>>> driveTest
        loop += 1
        time.sleep(.25)
