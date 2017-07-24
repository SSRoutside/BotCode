
from __future__ import division
import time
import numpy as np
import cv2
import pyrealsense as pyrs
import os
import datetime
import cv2
import cone_detection
#to show the image

from matplotlib import pyplot as plt
import numpy as np
import motor_init



with pyrs.Service() as a:
 
    dev = pyrs.Device()

    #dev.apply_ivcam_preset(0)
#    dev.set_device_option(7, 1)
    #dev.set_device_option(10,1)
    #dev.set_device_option(31,1)

    cnt = 0
    last = time.time()
    smoothing = 0.9
    fps_smooth = 30

    def nothing(x):
        pass


   
#if you get a true value it updates counter, if it is false
# it resets and once it reaches a threshold
# or look at every fifth frame

    while True:

        cnt += 1
        if (cnt % 10) == 0:
                now = time.time()
                dt = now - last
                fps = 10/dt
                fps_smooth = (fps_smooth * smoothing) + (fps * (1.0 -smoothing))
                last = now

        dev.wait_for_frames()

        c = dev.color # was color


      #  e = dev.dac
        f = dev.cad

     #   eh = np.size(e,0)
     #   ew = np.size(e,1)

        
        #cd = np.concatenate((e,f), axis=1)



#        cv2.imshow('', cd)
        c_col = cv2.cvtColor(c, cv2.COLOR_RGB2BGR)
        rgb_im = cv2.cvtColor(f, cv2.COLOR_RGB2BGR)
        cd = np.concatenate((c_col,rgb_im), axis=1)
        cv2.imshow('this is our image', cd)



      #  h = np.size(c,0)
      #  w = np.size(c,1)

        #depth aligned color
       # depth_and_color = dev.dac
       # d_and_c = 
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
       # cv2.imshow('raw', c)
        dark = cv2.imread('black.jpg')
        rgb_im, cone_present, x, y = cone_detection.find_cone(rgb_im, dark) #rgb
        

        #resized = cv2.resize(rgb_im, None,fx= 640/1920,fy= 480/1080, interpolation=cv2.INTER_AREA)
        #h = np.size(resized,0)
        #w = np.size(resized,1)
        
        #print h
        #print w
    #    dx = int(x* (640/1920))
    #    dy = int(y*(480/1080))
        if cone_present == True:
            print 'cone spotted, moving forward'    
            print(cone_present)
        #    depth = [x, y]
        #    print(depth)  


            e =  motor_init.getError(x)
            print "error is %f" % (e)
            if e > 0:
                ### turn right ###
           
                motor_init.SetAndDriveLeft(.4, True, e)
                motor_init.SetAndDriveRight(.4, False, e)
            

            elif e < 0:
                ### turn left ###
                motor_init.SetAndDriveLeft(.4, False, e)
                motor_init.SetAndDriveRight(.4, True, e)

            else:

                ### go forward straight ###
                motor_init.SetAndDriveLeft(.4, True, e)
                motor_init.SetAndDriveRight(.4, True, e)



        if cone_present == False:
            print 'spinning to locate cone'   
            e =  motor_init.getError(x)
            print "error is %f" % (e)

            motor_init.SetAndDriveLeft(.4, True, e)
            motor_init.SetAndDriveRight(.4, True, e)

        d = dev.depth #* dev.depth_scale * 1000
        d_im = dev.depth*0.05


        e = dev.dac

  #      eh = np.size(e,0)
  #      ew = np.size(e,1)
  #      cv2.imshow('e', e)
  #      print(eh)
  #      print(ew)

  #      f = dev.cad
  #      fh = np.size(e,0)
  #      fw = np.size(e,1)
  #      cv2.imshow('f', f)
  #      print(fh)
  #      print(fw)


##############3
        d_im_col = cv2.applyColorMap(d_im.astype(np.uint8), cv2.COLORMAP_HSV)
################        
        d__im = cv2.circle(d_im_col, (x,y), 10, (255,255,255), 3)
        cv2.imshow('', d__im)
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
        cv2.imshow('IMAGE FROM CONE DETECTION', rgb_im)
#        cv2.imshow('', d_im_col)
   #     d = dev.dac
#        cv2.imshow('', cd)
        input = cv2.waitKey(1)

        if input == ord('q'):
                break

        elif (input == -1):
                continue
    
    print("heeeeeeeeeeeeeeeeeeeeyyyy")
    motor_init.turnOffMotors()
