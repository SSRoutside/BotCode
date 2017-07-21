#from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
#import atexit

# From Adafruit MotorHat example code
# create a default object, no changes to I2C address or frequency
#mh = Adafruit_MotorHAT(addr=0x60)

# get each motor
#myMotor1 = mh.getMotor(1) # right motor
#myMotor2 = mh.getMotor(3) # left motor
#myMotor3 = mh.getMotor(2) # right motor
#myMotor4 = mh.getMotor(4) # left motor

# get motor values between 0 and 255
def getMotorValue(percent):
    mv = percent * 255
    mv = int(mv)
    return mv



def getError(x):
    cl = 320 #centerline of depth stream
    k = 1.2 #proportionality constant
    error = cl - x
    correction = error * k
    correction = int(correction)
        
    return correction

# used to set speed and direction of Right Motor Pairs
def SetAndDriveRight(speed, forward, MV):
#    MV = getMotorValue(speed)

   # MV = getError(x)


    myMotor1.setSpeed(MV)
    myMotor3.setSpeed(MV)

    if forward:
        myMotor1.run(Adafruit_MotorHAT.FORWARD)
        myMotor3.run(Adafruit_MotorHAT.FORWARD)
    else:
        myMotor1.run(Adafruit_MotorHAT.BACKWARD)
        myMotor3.run(Adafruit_MotorHAT.BACKWARD)


# used to set speed and direction of Left Motor Pairs
def SetAndDriveLeft(speed, forward, MV):
 #   MV = getMotorValue(speed)

   # MV = getError(x)


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

#atexit.register(turnOffMotors)
