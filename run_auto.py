# import current autonomous functions
import auto_capabilities as AC
import motor_init as MI

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
        cone_present = AC.findCone(dev, cnt)

        # determine if wall exists
        oneWall = AC.oneWallCheck()

        if oneWall == True:
            # run the wallFollowing sequence
            rightMV, rightF, leftMV, leftF, loop, sleep = AC.wallFollow()

        else:
            # set straight motorvalue (80% max)
            straight_MV = 204
            # run randomWalk when there is no other information available
            rightMV, rightF, leftMV, leftF, driveTime, turnTime, sleep = AC.randomWalk()

        loop += 1
