from __future__ import division
import cv2
#to show the image
from matplotlib import pyplot as plt
import numpy as np
from math import cos, sin

green = (0, 255, 0)

def greeting():
    print "Hello, world."


def show(image):
    # Figure size in inches
    plt.figure(figsize=(10, 10))

    # Show image, with nearest neighbour interpolation
    #plt.imshow(image, interpolation='nearest')

def overlay_mask(mask, image):
	#make the mask rgb
    rgb_mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
    #calculates the weightes sum of two arrays. in our case image arrays
    #input, how much to weight each. 
    #optional depth value set to 0 no need
    img = cv2.addWeighted(rgb_mask, 0.5, image, 0.5, 0)
    return img

#def get_mask(image):
 #   mask = np.zeros(image.shape, np.uint8)
  #  return mask


def find_contours(image,colimage):
########## COPY IMAGE ######################
    clone = image.copy()
    clone2 = colimage.copy()
    #cv2.imshow('image', clone)
    #input, gives all the contours, contour approximation compresses horizontal, 
    #vertical, and diagonal segments and leaves only their end points. For example, 
    #an up-right rectangular contour is encoded with 4 points.
    #Optional output vector, containing information about the image topology. 
    #It has as many elements as the number of contours.
    #we dont need it

########### FIND CONTOURS #################

    ret, threshed_img = cv2.threshold(clone, 127, 255, cv2.THRESH_BINARY)


#######ASPECT RATIO HAS 3 OR GREATER
####### STRAIGHT FORWARD WAY TO ELIMINATE FALSE POSITIVES



    #pseudo_col = cv2.cvtColor(clone, cv2.COLOR_GRAY2RGB)
    r_image, contours, hierarchy = cv2.findContours(threshed_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #mod_image, contours, hierarchy = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    #cv2.imshow('new image', mod_image)

########### DRAW CONTOURS #################
    for i in contours:
        # get convex hull
        hull = cv2.convexHull(i)
        #print hull
        # draw the contour
        cv2.drawContours(colimage, [hull], -1, (0, 255,0), 2)

    

        #i = hierarchy[i][0]
    #draw = cv2.drawContours(mod_image, contours, -1, (0,255,0), 10)
    colimage = colimage - clone2
    #cv2.imshow("contours", colimage) 
    #cv2.drawContours(mod_image, contours, i, 'blue', CV_FILLED, 8, hierarchy)
    return colimage

    #for cnt in contours:
     #   hull = cv2.convexHull(contours[cnt],)
    #cv2.imshow('hull', hull) 

    #cv2.waitKey(0)
     
############ CONVEX HULLS ###################
  #  cnt = np.asarray(contours[0])
  #  hull = cv2.convexHull(cnt, returnPoints = False)
  #  for cnt in contours:
  #  hull = cv2.convexHull(cnt)
    #points cnt= hull[i]
    #cv2.imshow(points)
    #cv2.imshow("hull", hull)
    #print hull
   # cv2.drawContours(clone, [hull],-1, (0,0,255),1)

   # cv2.imshow("hull", clone)

    # Isolate largest contour
   # contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
   # biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]

############## Don't think we need this. - Jesus ##########

    #mask = np.zeros(image.shape, np.uint8)
    #cv2.imshow('mask', mask)
    #cv2.drawContours(mask, [biggest_contour], -1, 255, -1)
    #return mask

#############################################################3

def circle_contour(image, contour):
    # Bounding ellipse
    image_with_ellipse = image.copy()
    #easy function
    ellipse = cv2.fitEllipse(contour)
    #add it
    cv2.ellipse(image_with_ellipse, ellipse, green, 2, cv2.LINE_AA)
    return image_with_ellipse


def find_cone(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cone_spotted = False
    # Make a consistent size
    #get largest dimension

#    max_dimension = max(image.shape)

    #The maximum window size is 700 by 660 pixels. make it fit in that
#    scale = 700/max_dimension

    #resize it. same width and hieght none since output is 'image'.
 #   image = cv2.resize(image, None, fx=scale, fy=scale)
    

    #we want to eliminate noise from our image. clean. smooth colors without
    #dots
    # Blurs an image using a Gaussian filter. input, kernel size, how much to filter, empty)
    image_blur = cv2.GaussianBlur(image, (7, 7), 0)

    #t unlike RGB, HSV separates luma, or the image intensity, from
    # chroma or the color information.
    #just want to focus on color, segmentation
    image_hsv = cv2.cvtColor(image_blur, cv2.COLOR_RGB2HSV)
    #cv2.imwrite('HSV-BLUR.jpg', image_blur_hsv)
   

###########  THRESHOLDING #############
    # Filter by colour
    # 0-10 hue
    #minimum red amount, max red amount
    min_orange = np.array([0, 193, 115])
    max_orange = np.array([15, 255, 255])

#    min_orange = np.array([0, 135, 135])
#    max_orange = np.array([15, 255, 255])

    #max_orange = np.array([179, 255, 255])
    #layer
    mask1 = cv2.inRange(image_hsv, min_orange, max_orange)
#    cv2.imshow("m1", mask1) 

    min_orange2 = np.array([159, 135, 132])
    max_orange2 = np.array([179, 255, 255])

    mask2 = cv2.inRange(image_hsv, min_orange2, max_orange2)
   # cv2.imshow("m2", mask2)

   
    #brightness of a color is hue
    # 170-180 hue
    #min_orange2 = np.array([0, 100, 80])
    #min_orange2 = np.array([170, 100, 80])
    #max_orange2 = np.array([0, 256, 256])
    #mask2 = cv2.inRange(image_blur_hsv, min_orange2, max_orange2)

    #cv2.imshow("mask1",mask1)
    #cv2.imshow("mask2",mask2)
   

    #mask = (mask1 - mask2) + (mask2-mask1)
    mask = (mask1 + mask2) - (mask1-mask2) - (mask2-mask1)
#    cv2.imshow("mask", mask)



    #looking for what is in both ranges
    # Combine masks
    #mask = mask1 + mask2
    # Clean up
    #we want to circle our strawberry so we'll circle it with an ellipse
    #with a shape of 15x15
    #kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    #morph the image. closing operation Dilation followed by Erosion. 
    #It is useful in closing small holes inside the foreground objects, 
    #or small black points on the object.
    #mask_closed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    #erosion followed by dilation. It is useful in removing noise
    #mask_clean = cv2.morphologyEx(mask_closed, cv2.MORPH_OPEN, kernel)
    #cv2.imshow("mask-clean", mask_clean)


############## CLONE IMAGE ################
    thresholded_image = mask.copy()


############### ERODE #####################
    kernel = np.ones((5,5), np.uint8)
    eroded_image = cv2.erode(thresholded_image, kernel, 1)


############## DILATE #####################

    img_dilation = cv2.dilate(eroded_image, kernel, iterations=1)
  #  cv2.imshow("dilated", img_dilation)

########### GAUSSIAN BLUR ##################

    # Blurs an image using a Gaussian filter. input, kernel size, how much to filter, empty)
    image_blur = cv2.GaussianBlur(img_dilation, (7, 7), 0)
  #  cv2.imshow('blurred', image_blur)

########### CANNY EDGE #####################
    edge = cv2.Canny(image_blur, 4000, 4500, apertureSize=5)
    cloned_edge = edge.copy()


   # if 


    #cloned_edge = cloned_edge/2.0
   # low = np.array([0,0,0])
   # high = np.array([.6, .6, .6])
    actual_cone = mask1.any() and mask2.any()
    if actual_cone == True:
 
        cone_spotted = True
    #cv2.imshow("canny", edge)
    
########### FIND CONTOURS #################
# gets rid of noise in canny edge image
# makes everything in the image a smooth shape
        contour = find_contours(edge, image_hsv)
        contour = cv2.cvtColor(contour, cv2.COLOR_BGR2GRAY)
        thresh, contour = cv2.threshold(contour, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
   # for i in 
 # cv2.imshow('contours', con)
 #   cv2.imshow('contour', contour)

    #cv2.imshow('edge', edge)
    # Find biggest cone
    #get back list of segmented cone and an outline for the biggest one
   # mask_cones = find_biggest_contour(mask_clean)
    #cv2.imshow('contours',mask_cones)
    # Overlay cleaned mask on image
    # overlay mask on image, strawberry now segmented
    #overlay = overlay_mask(mask_clean, image)

    # at this point, the contours are found

########### APPROX POLYGONS ################ 
   # epsilon = .3 #0.1*cv2.arcLength(contour, True)
    #approx = cv2.approxPolyDP(contour, epsilon, True)
    #cv2.imshow("approx", approx)
    #For Each contour As Contour(Of Point) In listOfContours 'for each contour
   # 'draw on imgContours in case show steps is chosen
#CvInvoke.cvDrawContours(imgContours, contour, New MCvScalar(255), New MCvScalar(255), 100, 1, LINE_TYPE.CV_AA, New Point(0, 0))

################ MOMENTS ###################
        M = cv2.moments(contour)
    #print M
        if (M['m00'] != 0): 
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00']) 
            print cx
            print cy
            contour = cv2.circle(contour, (cx,cy), 2, (255,255,255), 3)
    #cv2.imshow('center of mass', contour)
    #area = cv2.contourArea(contour)
    #print 'area'
    #print M['m00']

   # approxPolyDP(contour, approx, 5, true);
   # area1 = contourArea(approx)
   # print area1
##########################################
#not really needed
    # Circle biggest strawberry
    #circle the biggest one
    #circled = circle_contour(overlay, big_cone_contour)
#    show(circled)
    
    #we're done, convert back to original color scheme
    #bgr = cv2.cvtColor(circled, cv2.COLOR_RGB2BGR)
###########################################    

#    cv2.waitKey(0)
    #cv2.destroyAllWindows()

        return contour, cone_spotted
    return edge, cone_spotted

#read the image
#image = cv2.imread('TEST.jpg')
#image = cv2.imread('cone_4_2017-07-06_11:41:55__color.PNG')
#image = cv2.imread('cone_5_2017-07-06_11:42:20__color.PNG')
#detect it
#result = find_cone(image)
#find_biggest_contour(image)
#write the new image0
#cv2.imwrite('CONEINSIDE-FAR.jpg', result)

