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
from motor_init import *



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

        c = dev.color
        rgb_im = cv2.cvtColor(c, cv2.COLOR_RGB2BGR)




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
    #    cv2.imshow('raw', c)
        rgb_im, cone_present = cone_detection.find_cone(rgb_im) #rgb
        if cone_present == False:
            print 'spinning to locate cone'    
            print(cone_present)
         #spin til you find a cone

        if cone_present == True:
            print 'spotted cone, moving forward'   



        d = dev.depth * dev.depth_scale * 1000
        d_im = dev.depth*0.05

        d_im_col = cv2.applyColorMap(d_im.astype(np.uint8), cv2.COLORMAP_HSV)
       
#        print(cv2.size(rgb_im))
#        print(cv2.size(d_im_col))

#        cd = np.concatenate((rgb_im,d_im_col), axis=1)


#        cv2.putText(cd, str(fps_smooth)[:4], (0,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0))

 #       cv2.imshow('', cd)

        cv2.imshow('', rgb_im)
#        cv2.imshow('', d_im_col)
        input = cv2.waitKey(1)

        if input == ord('q'):
                break

        elif (input == -1):
                continue
    
