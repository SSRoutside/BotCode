# This code will take sonar error measurements in cm and adjust the sterring and correction
# proportionally due to that error.

def calcControl(error, kp):
    # basic proportional equation
    control = int(kp * error)

    return control

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

    control = calcControl(error, kp)

    if error < 0:
        # left turn
        SetAndDriveLeft(forward=False, MV=control)
        SetAndDriveRight(forward=True, MV=control)
    else:
        # right turn
        SetAndDriveLeft(forward=True, MV=control)
        SetAndDriveRight(forward=False, MV=control) 




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

    control = calcControl

    if (left and (error < 0)) or (right and (error > 0)):
        # right turn
        SetAndDriveLeft(forward=True, MV=control)
        SetAndDriveRight(forward=False, MV=control)

    else:
        # left turn
        SetAndDriveLeft(forward=False, MV=control)
        SetAndDriveRight(forward=True, MV=control)

