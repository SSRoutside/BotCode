# import containing randomWalk function
from auto_capabilities import *
# import containing motor settings, functions, and initializations
from motor_init import *

count = 0

while count < 4:
    randomWalk()
    count += 1

turnOffMotors()
