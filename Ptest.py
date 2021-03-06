from motor_init import *
# This code will take sonar error measurements in cm and adjust the sterring and correction
# proportionally due to that error.

def centeringPcontrol(left_dist, right_dist):
    # initialize constants
    # slope constant: should be played with based on behavior
    kp = 10  # based on calculation

    # derivative constant:
    ## should be added for better controll ## kd = something

    # determine error by determining the difference between the left and right measurements.
    # negative value: turn to the left (L : -, R : +)
    # positive value: turn to right (R : -, L : +)
    error = left_dist - right_dist

    control = int(kp * error)

    if error < -2:
        # left turn
        SetAndDriveLeft(forward=False, MV=control)
        SetAndDriveRight(forward=True, MV=control)
    elif error > 2:
        # right turn
        SetAndDriveLeft(forward=True, MV=control)
        SetAndDriveRight(forward=False, MV=control)
    else:
        # drive straignt
        SetAndDriveLeft(speed=.8, forward=True)
        SetAndDriveRight(speed=.8, forward=True)



def wallPcontrol(wall_dist, ideal_dist, left, right):
    # wall_dist is sonar measurement to wall
    # left and right are booleans indictating which side the wall is being followed on
    # ideal_dist is a constant giving the ideal distance away fron a wall


    # initialize constants
    # slope constant: should be played with based on behavior
    kp = 10  # based on calculation
 
    # derivative constant:
    ## should be added for better controll ## kd = something

    # error determined by subracting ideal_distance from wall_distance.
    # negative error: correct away from wall
    # postive error: correct towards wall
    error = wall_dist - ideal_dist

    control = int(kp * error)

    print(control)

    if (left and (error < -2)) or (right and (error > 2)):
        # right turn
        SetAndDriveLeft(forward=True, MV=control)
        SetAndDriveRight(forward=False, MV=control)

    elif (right and (error < -2)) or (left and (error > 2)):
        # left turn
        SetAndDriveLeft(forward=False, MV=control)
        SetAndDriveRight(forward=True, MV=control)

    else:
        # drive straight
        SetAndDriveLeft(speed=.8, forward=True)
        SetAndDriveRight(speed=.8, forward=True)
