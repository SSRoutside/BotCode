import time
import numpy as np
import cv2
import pyrealsense as pyrs
import atexit
import os
import datetime
import logging

from scipy import ndimage
from scipy.ndimage import morphology as scmorph

# set up logging level
#logging.basicConfig(level=logging.INFO)

count = 0

def main():
    # Start realsense (if available)
    
    pyrs.start()
    
    # Set up device for colour and depth streaming.
    # How might you add a raw IR stream?
    #py_dev = pyrs.Device(device_id = 0, streams = [pyrs.ColourStream(fps = 30), pyrs.DepthStream(fps=30)])

    # Jesus's changes:

    check = True
    while check  == True:
         print(" ") 
         folder_name = raw_input("What folder would you like to save these images in? ")
         if os.path.isdir(folder_name) == True: 
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

        
baseline_name = series_name
baseline_name = baseline_name + '_1.jpg'



# to get date and time: datetime.date.today()


            
    
    # Run forever! (until quitting)
    while True:
        
        py_dev.wait_for_frame()
        c_im = py_dev.colour
        
        # Convert colour frame into a single RGB image
        rgb_im = c_im[..., ::-1] #y tho
        
        # scale depth frames to avoid colour wrapping. Is this the best scaling factor for our purposes? Try changing it
        d_im = py_dev.depth * 0.05 #what units this be in

        # Convert the 3D depth frame to a 2D colour map:
        d_im_col = cv2.applyColorMap(d_im.astype(np.uint8), cv2.COLORMAP_HSV)
        # what other colourmaps exist? are some more intuitive than others? Any that would be a problem for colourblind people?
        # good ones to use (because they have a lot of color bins):
        # COLORMAP_HSV
        # COLORMAP_JET
        # COLORMAP_RAINBOW

        
        # combine the two images into one array, for display
        cd = np.concatenate((rgb_im, d_im_col), axis=1)
        # axis 1 is side by side view
        # axis 0 is one on top of other view
        
        # show two images in one frame (default name)
        # To-do: what if we want to display multiple frames? look at the OpenCV imshow documentation for tips
        cv2.imshow('', cd)

        # To-do: how about displaying a point-cloud using VTK, in a different window?
        # Visiting vtk info another day
        
        input = cv2.waitKey(1):
        # quit if we hit 'q'
        if (input == ord('q')):
            break
        elif (input == ord('a')):
            os.chdir(final_directory)
            
            counter++;
            # save depth and colour images if we hit 'a'.
            # Note that there are many, many ways to save images in Python.
            # OpenCV has one method in its library, but for faster image saving we could look into something like PIL.
            baseline_name = baseline_name + '_'+counter+'.jpg' #keeps count of the photo taken in this particular series
            cv2.imwrite(baseline_name + '_depth.PNG', d_im_col);
            cv2.imwrite(baseline_name + '_color.PNG', rgb_im);
            # to-do: how do we save images to a specific folder? How can we let the user choose this folder on start up?

            # Jesus: I think we can add a raw_input line at the beginning of the code asking the user for a folder. We would also need to make sure that the inputed folder name actually exists. If input does not match an existing folder, would keep asking user for a folder name.

            # Jesus: check this website out for explanation of imwrite:
            # http://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html?highlight=imwrite
            
            # Can we add an incrementing number to the filename of colour/depth?

            # Jesus: add a counter in a for loop that sets the name of the file
            
            # What about having the user type a new filename every time we save?

            # Jesus: I like this idea. Gives the user a bit more freedom. Downside is that we don't know if its tree 6 or tree 7. Checking to see if the filename already exists would solve that problem.
            
        elif (input == -1):
            continue



if __name__ == '__main__':
    main()
