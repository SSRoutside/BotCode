import motor_init as MI
import random
import time

def randomWalk():
    # will return 1 or 0
    random_direction = random.randint(0, 1)

    # calculate time based on time_constant and random decimal (between 5 and 10 seconds)
    driveTime = random.randint(3, 6)

    # calculate length of turn based on time_constant and random decimal (between 2 and 4 seconds)
    turnTime = random.randint(2,8)

    # initialize loop counts
    turnCount = 0
    driveCount = 0

    print random_direction

    if random_direction == 1:
        # turn to the right
        MI.SetAndDriveRight(.10, True)
        MI.SetAndDriveLeft(.90, True)
        print('pivoting right')

        # continue in that direction for randomly determined time
        time.sleep(turnTime)

    else:
        # turn to the left
        MI.SetAndDriveRight(.90, True)
        MI.SetAndDriveLeft(.10, True)
        print('pivoting left')

#    while turnCount < (turnTime/.25):

        # check for cone and exit randomWalk if found
#        if findCone() == True:
 #           print("Cone detected.")
  #          return

        # check for wall and exit randomWalk if found
#        if oneWallCheck() == True:
 #           print("Wall detected.")
  #          return

#        turnCount += 1
    time.sleep(turnTime)

    # drive forward for specified amount of time
    MI.SetAndDriveRight(.80, True)
    MI.SetAndDriveLeft(.80, True)
    print('driving straight')

#    while driveCount < (driveTime/.25):

        # check for cone and exit randomWalk if found
#        if findCone() == True:
 #           print("Cone detected.")
  #          return

        # check for wall and exit randomWalk if found
#        if oneWallCheck() == True:
 #           print("Wall detected.")
  #          return

#        driveCount += 1
    time.sleep(driveTime)

# Main control loop: set to run randomWalk function 5 times
# initialize loop counter
loop = 0

while loop <= 3:
    randomWalk()
    # append loop count
    loop += 1


# make sure motors stop after falling out of the while loop
MI.turnOffMotors()
