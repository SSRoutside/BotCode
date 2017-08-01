# motorhat import
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
# servohat import
#from Adafruit_PWM_Servo_Driver import PWM
import atexit

# From Adafruit MotorHat example code
# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x60)

# servo hat object
#pwm = PWM(0x40)

# get each motor: WORKS FOR LITTLE BLUE
myMotor1 = mh.getMotor(1) # right motor
myMotor2 = mh.getMotor(3) # left motor
myMotor3 = mh.getMotor(2) # right motor
myMotor4 = mh.getMotor(4) # left motor
print('motors set')

# get motor values between 0 and 255
def getMotorValue(percent):
    mv = percent * 255
    mv = int(mv)
    return mv


#########################
####### Are we picking the center line of the depth stream, rgb stream, or transformed rgb-depth stream?
##########################


def isCorrectionNeeded(x):
    needToCorrect = True
    centerLineOfFrame = 320
    coneCenterOfMass = x
    error = coneCenterOfMass - centerLineOfFrame

    # window of acceptable values
    if error > 315 and error < 325:
        need_to_correct = False
        return needToCorrect
    return needToCorrect 


def getError(x):
    cl = 320 #centerline of depth stream
    k = 1.2 #proportionality constant
    error = x - cl

    correction = k * error
    correction = int(correction)

    return correction

# used to set speed and direction of Right Motor Pairs
def SetAndDriveRight(speed=0, forward=True, MV=0):
    MV = getMotorValue(speed)

   # MV = getError(x)

    print ('MOTOR VALUE IS:  ' + str(MV))
    MV = abs(MV)
    myMotor1.setSpeed(MV)
    myMotor3.setSpeed(MV)

    if forward:
        myMotor1.run(Adafruit_MotorHAT.FORWARD)
        myMotor3.run(Adafruit_MotorHAT.FORWARD)
    else:
        myMotor1.run(Adafruit_MotorHAT.BACKWARD)
        myMotor3.run(Adafruit_MotorHAT.BACKWARD)


# used to set speed and direction of Left Motor Pairs
def SetAndDriveLeft(speed=0, forward=True, MV=0):
    MV = getMotorValue(speed)

   # MV = getError(x)

    print ('MOTOR VALUE IS:  ' + str(MV))
    MV = abs(MV)
    myMotor2.setSpeed(MV)
    myMotor4.setSpeed(MV)

    if forward:
        myMotor2.run(Adafruit_MotorHAT.FORWARD)
        myMotor4.run(Adafruit_MotorHAT.FORWARD)
    else:
        myMotor2.run(Adafruit_MotorHAT.BACKWARD)
        myMotor4.run(Adafruit_MotorHAT.BACKWARD)

# auto disable motors on shutdown
def turnOffMotors():
        mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)
