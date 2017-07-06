import logging


logging.basicConfig(level=logging.INFO)

import time
import numpy as np
import cv2
import pyrealsense as pyrs
import os
import datetime

check = True
global final_directory
global counter

counter = 0

while check  == True:
	 print(" ")
	 folder_name = raw_input("What folder would you like to save these images in? ")
	 if os.path.isdir(folder_name) == True:
		current_directory = os.getcwd()
		final_directory = os.path.join(current_directory, folder_name)
		if not os.path.exists(final_directory):
			os.makedirs(final_directory)
		check = False

	 if os.path.isdir(folder_name) == False:
		print(" ")
		print("That folder name does not exist. A new folder will be created in the current directory under that name. ")
		current_directory = os.getcwd()
		final_directory = os.path.join(current_directory, folder_name)
		if not os.path.exists(final_directory):
			os.makedirs(final_directory)
		check = False
		# for testing purposes, you can enter this: /Users/Jesus/Documents/REU 2017/misc-files


check2 = True
check3 = True

series_name = 'start'

while check2 == True:
	print(" ")
	series = raw_input("Would you like to save related images in a series? Images stored in this series will have the same file name with a counting number at the end. [y/n]   ")
	if series in ('y','Y'):
		while check3 == True:
			print(" ")
			series_name = raw_input("What would you like to name the series? ")
			if os.path.isfile(series_name) == True:
				print(" ")
				print("A file already exists with that name. ")
				check3 = True

			if os.path.isfile(series_name) == False:
				print(" ")
				print("That name will do I suppose...")
				check3 = False

			check2 = False

	else:
		print(" ")
		print("Well okay then, have fun thinking up a unique name for each picture... ")
		check2 = False


with pyrs.Service() as a:
 
    dev = pyrs.Device()
	#with pyrs.Service() as a, pyrs.Device() as dev:

    dev.apply_ivcam_preset(0)

    cnt = 0
    last = time.time()
    smoothing = 0.9
    fps_smooth = 30

    def nothing(x):
        pass
# Create a window
    img = np.zeros((300,512,3), np.uint8)
    cv2.namedWindow('Calibration')

# Switch for ON/OFF Emitter Functionality
    emitter_switch = '0 : OFF \n1 : ON'
    cv2.createTrackbar(emitter_switch, 'Calibration',0,1,nothing)


# Trackbars for changing camera settings
    cv2.createTrackbar('Gain','Calibration',1,63,nothing)
    cv2.createTrackbar('Exposure','Calibration',1,33,nothing)


#    while(1):
#   cv2.imshow('image',img)
#   k = cv2.waitKey(1) & 0xFF
    #if k == 27:
    #    break

    # get current positions of four trackbars
#   r = cv2.getTrackbarPos('R','image')
#    g = cv2.getTrackbarPos('G','image')
#    b = cv2.getTrackbarPos('B','image')
#    s = cv2.getTrackbarPos(switch,'image')
 
#    if s == 0:
#        img[:] = 0
#    else:
#        img[:] = [b,g,r]

#    cv2.destroyAllWindows()


    #emitter
   # dev.set_device_option(31,0)
   # print("emitter disabled")

    #gain
   # dev.set_device_option(29, 1)

    #exposure
   # dev.set_device_option(30, 3)


    while True:

        cv2.imshow('Calibration',img)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
        gain = cv2.getTrackbarPos('Gain','Calibration')
        exposure = cv2.getTrackbarPos('Exposure','Calibration')
        e_switch = cv2.getTrackbarPos(emitter_switch,'Calibration')
 
        if e_switch == 0:
            dev.set_device_option(31,0)
            dev.set_device_option(29, gain)
            dev.set_device_option(30, exposure)
        else:
            dev.set_device_option(31,1)
            dev.set_device_option(29, gain)
            dev.set_device_option(30, exposure)




	cnt += 1
	if (cnt % 10) == 0:
		now = time.time()
		dt = now - last
		fps = 10/dt
		fps_smooth = (fps_smooth * smoothing) + (fps * (1.0-smoothing))
		last = now

	dev.wait_for_frames()

	c = dev.color
	rgb_im = cv2.cvtColor(c, cv2.COLOR_RGB2BGR)

	d = dev.depth * dev.depth_scale * 1000
	d_im = dev.depth*0.05

	d_im_col = cv2.applyColorMap(d_im.astype(np.uint8), cv2.COLORMAP_HSV)

	cd = np.concatenate((c,d_im_col), axis=1)

	cv2.putText(cd, str(fps_smooth)[:4], (0,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0))

                
        cv2.imshow('', cd)
        input = cv2.waitKey(1)


	if input == ord('q'):
		break
		#if cv2.waitKey(1) & 0xFF == ord('q'):
		#    break
		#elif (0xFF == ord('a')):
	elif (input == ord('a')):
		print('got here')
		os.chdir(final_directory)

		counter = counter + 1
		# save depth and colour images if we hit 'a'.
			# Note that there are many, many ways to save images in Python.
			# OpenCV has one method in its library, but for faster image saving we could look into something like PIL.
		file_name= series_name + '_' + str(counter)
         #keeps count of the photo taken in this particular series
		cv2.imwrite(file_name +'_'+ str(datetime.date.today())+'_'+ time.strftime("%H:%M:%S")+'_'+ '_depth.PNG', d_im_col);
		cv2.imwrite(file_name +'_'+ str(datetime.date.today()) +'_'+ time.strftime("%H:%M:%S") +'_'+ '_color.PNG', rgb_im);
			# to-do: how do we save images to a specific folder? How can we let the user choose this folder on start up?
			# the above imwrite commands have the format of series_count_date_time.png

			# Jesus: I think we can add a raw_input line at the beginning of the code asking the user for a folder. We would also need to make sure that the inputed folder name actually exists. If in$
			# Jesus: check this website out for explanation of imwrite:
			# http://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html?highlight=imwrite

			# Can we add an incrementing number to the filename of colour/depth?
			# Jesus: add a counter in a for loop that sets the name of the file

			# What about having the user type a new filename every time we save?
			# Jesus: I like this idea. Gives the user a bit more freedom. Downside is that we don't know if its tree 6 or tree 7. Checking to see if the filename already exists would solve that probl$

	elif (input == -1):
		continue

