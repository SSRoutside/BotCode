from __future__ import division
import time
import numpy as np
import cv2
import pyrealsense as pyrs
import os
import datetime
import cv2
import coneDetWithShape
#to show the image

from matplotlib import pyplot as plt
import numpy as np
import motor_init




def nav_to_cone(x):
    e_last = 0
    e = 0
    

    #if you get a true value it updates counter, if it is false
    # it resets and once it reaches a threshold
    # or look at every fifth frame

#####################################################
##
##
##   NAVIGATION LOGIC 
##
##   Feed rgb image into cone_detection. If something
##   is returned, this means that a cone is in the 
##   robot's field of view, so move forward.
##   If not, turn around and search until the cone
##   is spotted.
##
##
##
##
##################################################


            ############################################################
            ##
            ##
            ##  PID- PROPORTIONAL LOGIC 
            ##  First, we get the error (which is found by subtracting the centerline from the center of mass
            ##  that is returned by find_cone (the (x,y) coordinate). Next, we multiply the error by a k value
            ##  that acts as a slope for how fast the robot can turn to the max value-- the slope for how quickly it turns to the max.
            ##  After this, we check this product against the threshold for the max speed of the motor (255). If the product is greater
            ##  than this threshold, we set this product to 255. Next, we check the sign of this product and either turn left if the
            ##  product is negative or turn right if the product is positive. 
            ##
            ##  NOTE: The gain (the k-term) is set by the hardware so this will be different for each robot
            ##  Start with k value of 1, test, then adjust from there
            ## 
            #######################################################################



    
    correction_needed = motor_init.isCorrectionNeeded(x)
    e = motor_init.getError(x)

    if correction_needed == True:
        print "error is %f" % (e)
        crt = motor_init.getCorrection(e, e_last, dt)
                ########################
                ##
                ##  Thresholding
                ##
                ########################
                # even though the error is a distance in the frame of view, it is still proportional to the speed
                # sets a max value
        if e > 255:
            e = 255

                # sets a min value
        if e < -255:
            e = -255

        mv = int(2 * e)
        speed = 150 #initialize
                # this is the range where it is fine to go straight forward
#                if e > -20 and e < 20:
 #                   motor_init.SetAndDriveLeft(.4, True, speed)
  #                  motor_init.SetAndDriveRight(.4, True, speed)
   #                 print 'error is negligible, going forward'
                ############################################
                ##
                ##  Check Whether to Turn Right or Left
                ##
                ############################################
                # these are the values for it to turn right
        if e >= 20:
                ### turn right ###
                ### this would make it turn on spot 
                ### for how long? until the cone is directly on centerline?           
                ### should we add a margin of acceptance, which says if the center of mass is within this window, its ok, so move forward?
       #     motor_init.SetAndDriveLeft(.4, False, mv)
        #    motor_init.SetAndDriveRight(.4, True, mv)
            rightL = False
            rightMV = mv
            leftL = True
            leftMV = mv
            print 'correcting right ((((BUT ACTUALLY LEFT)))'
               ### now go forward ###
                   # motor_init.SetAndDriveLeft(.4, True, speed)
                   # motor_init.SetAndDriveRight(.4, True, speed)
                   # print 'now going forward'

            # if e < 0
        if e <= -20:
                ### turn left ###
         #   motor_init.SetAndDriveLeft(.4, True, mv)
         #   motor_init.SetAndDriveRight(.4, False, mv)
            rightL = True
            rightMV = mv
            leftL = False
            leftMV = mv

            print 'correcting left ((((BUT ACTUALLY RIGHT))))'
                ### now go forward ###
                   # motor_init.SetAndDriveLeft(.4, True, speed)
                   # motor_init.SetAndDriveRight(.4, True, speed)
                   # print 'now going forward'
    else:
    #    motor_init.SetAndDriveLeft(.4, True, 250)
    #    motor_init.SetAndDriveRight(.4, True, 250)
        rightL = True
        rightMV = 250
        leftL = True
        leftMV = 250

        print 'error is negligible, going forward'

    return rightMV, rightF, leftMV, leftF

# else:
#
                ### go straight forward ###
 #               motor_init.SetAndDriveLeft(.4, True, 150)
  #              motor_init.SetAndDriveRight(.4, True, 150)
   #             print 'CHARGING FORWARD!!!!!!' 



 #       else:
  #          print 'spinning to locate cone'   
          #  e =  motor_init.getError(x) #its not going to have an error if cone (or anything orange) isnt present
   #       #  print "error is %f" % (e)
    #        MV = 150
     ##       motor_init.SetAndDriveLeft(.5, False, MV)
       #     motor_init.SetAndDriveRight(.3, True, MV)

      #  d = dev.depth #* dev.depth_scale * 1000
      #  d_im = dev.depth*0.05


        #e = dev.dac

  #      eh = np.size(e,0)
  #      ew = np.size(e,1)
  #      cv2.imshow('e', e)
  #      print(eh)
  #      print(ew)

       # f = dev.cad
       # fh = np.size(f,0)
       # fw = np.size(f,1)
        #print fh, fw

  #      cv2.imshow('f', f)
  #      print(fh)
  #      print(fw)


##############
       # d_im_col = cv2.applyColorMap(d_im.astype(np.uint8), cv2.COLORMAP_HSV)
################
       # d__im = cv2.circle(d_im_col, (x,y), 10, (255,255,255), 3)
       # cv2.imshow('', d__im)
        #res_dim = cv2.resize(d_im, None, fx=213,fy= 213, interpolation=cv2.INTER_AREA)
        #h = np.size(d_im,0)
        #w = np.size(d_im,1)

        #print h
        #print w

#        print(cv2.size(rgb_im))
#        print(cv2.size(d_im_col))

#        cd = np.concatenate((rgb_im,d_im_col), axis=1)


#        cv2.putText(cd, str(fps_smooth)[:4], (0,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0))

#        cv2.imshow('', cd)
#
#        cv2.imshow('IMAGE FROM CONE DETECTION', rgb_im)
#        cv2.imshow('', d_im_col)
   #     d = dev.dac
#        cv2.imshow('', cd)
     #   e_last = e
     #   input = cv2.waitKey(1)

      #  if input == ord('q'):
      #      break

      #  elif (input == -1):
      #      continue
      #  time.sleep(.25)
   # print("Good bye")
   # motor_init.turnOffMotors()
