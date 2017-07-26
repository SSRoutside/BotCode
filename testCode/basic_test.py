import logging


logging.basicConfig(level=logging.INFO)



import time
import numpy as np
import cv2
import pyrealsense as pyrs
import os
import datetime
from PIL import Image

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
        dev.set_device_option(31, 0)
        dev.set_device_option(29, 1)
        dev.set_device_option(30,3)
	cnt = 0
	last = time.time()
	smoothing = 0.9
	fps_smooth = 30

	while True:

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

                # raw depth data
		d_raw = dev.depth
                # depth data scaled to read milimeters
		d_mm = dev.depth * dev.depth_scale * 1000
                # data that is scaled to be seen nicely in the depth
                # depth picture as shown on the monitor
		d_im = dev.depth*0.05

		d_im_col = cv2.applyColorMap(d_im.astype(np.uint8), cv2.COLORMAP_HSV)

               # i_im = dev.infrared
               # np.resize(i_im, (480, 640))
               # im_size = print(i_im.size)


                # putting all three images : rgb, depth, and infrared together
                #cd1 = np.concatenate((c,d_im_col), axis=1)
		cd = np.concatenate((d_im_col,c), axis=1)


		cv2.putText(cd, str(fps_smooth)[:4], (0,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0))

		# what other colourmaps exist? are some more intuitive than others? Any that would be a problem for colourblind people?
		# good ones to use (because they have a lot of color bins):
		# COLORMAP_HSV
		# COLORMAP_JET
		# COLORMAP_RAINBOW

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
			cv2.imwrite(file_name +'_'+ str(datetime.date.today())+'_'+ time.strftime("%H:%M:%S")+'_'+ '_depth.PNG', d_im_col)
			cv2.imwrite(file_name +'_'+ str(datetime.date.today()) +'_'+ time.strftime("%H:%M:%S") +'_'+ '_color.PNG', rgb_im)

                        # open files to write binary
                        raw_out = open(file_name+'_'+str(datetime.date.today())+'_'+time.strftime("%H:%M:%S")+'_'+'RawOut','wb')
                        mm_out = open(file_name +'_'+ str(datetime.date.today())+'_'+ time.strftime("%H:%M:%S")+'_'+ 'MMOut', 'wb')
                        image_out = open(file_name +'_'+ str(datetime.date.today())+'_'+ time.strftime("%H:%M:%S")+'_'+ 'ImageOut', 'wb')

                        # write variables to the opened files (for raw data, for milimeter data, for image data as in the variables above)
                        raw_out.write(d_raw)
                        mm_out.write(d_mm)
                        image_out.write(d_im)

                        # close files
                        raw_out.close()
                        mm_out.close()
                        image_out.close()

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

