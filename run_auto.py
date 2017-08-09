# import current autonomous functions
import auto_capabilities as AC
# import motor commands and initialization
import motor_init as MI
import time

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

    # initialize randomWalk counter
    randCount = 0

    # main environment sampling loop
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
            rightMV, rightF, leftMV, leftF = AC.wallFollow()

        else:
            # reaching this point means there is no pre-programmed event to
            # execute based on the surroundings. a "randomWalk" command will
            # be sent.

            # set left and right to drive forwards for all random commands
            rightF = True
            leftF = True

            # random direction to decide direction of turn
            direction = random.randint(0,1)

            if randCount < 10:
                # send a turn command
                # strong side set to 90% capacity, weak side set to 10% capacity
                if direction == 1:
                    # turn right
                    rightMV = 25
                    leftMV = 230

                else:
                    # turn left
                    rightMV = 230
                    leftMV = 25

            elif (randCount >= 10) and (randCount < 30):
                # send a command to drive straight
                # value corresponds to 80% of maximum power
                rightMV = 204
                leftMV = 204

            else:
                # reset randCount to zero
                randCount = 0

                # also set motors to straight
                rightMV = 204
                leftMV = 204

        # set motor values basedon returns from above
        MI.SetAndDriveRight(rightF, rightMV)
        MI.SetAndDriveLeft(leftF, leftMV)

        # incrememt overall loop count
        loop += 1

    # turn off motors at stop of driving while loop
    # instead of "with" loop
    MI.turnOffMotors()
