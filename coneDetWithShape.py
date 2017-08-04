from __future__ import division
import cv2
# to show the image
from matplotlib import pyplot as plt
import numpy as np
from math import cos, sin

################################################################
##
##     CONVEX HULL PASSES ASPECT RATIO TEST
##
##  INPUT: hull with multiple points (  ,  )
##  OUTPUT: boolean
##
################################################################

def convexHullPassesAspectRatioTest(singleHull):
    # get bounding rectangler
    x, y, w, h = cv2.boundingRect(singleHull)

    aspect_ratio = float(w)/h

#    print ("the aspect ratio is %f" % (aspect_ratio))


       # if convex hull is not taller than it is wide, return False
    
    if aspect_ratio < 0.8:
 #       print 'passed the aspect ratio test'

        return singleHull, True

    else:
        # returns a bogus thing but we're checking the bool
        viable_hull = np.arange(1)
        return viable_hull, False
        
#        print "WHY DO WE HAVE THIS?!?!??!?!?!"
# we dont return 
#        return False
    

################################################################
##
##     CONVEXHULLISPOINTINGUP
##
##  INPUT: viable hull with multiple point (  ,  )
##  OUTPUT: boolean
##
################################################################


def convexHullIsPointingUp(hull, hull_counter):
    #get bounding rectangle again
    
    x, y, w, h = cv2.boundingRect(hull)

    # calculate vertical center of convex hull
    vert_center = int((float(h))/2.0)

    #declare list of points above vertical center
    listOfPointsAboveCenter = [] 

    #and list of points below vertical center
    listOfPointsBelowCenter = []


    # When we printed out each element, this is the format it printed out as :[[321 345 ]],...
    # letting us know that each element itself is a 2-d array with only one element (a single array) in it
    # So if you want to step through the hull list, you index first by which element of the outermost
    # list youre on : hull[point]. Then, you index by the element you want to see in the inner array,
    # hull[point][0], then you index by the specific number you want in this inner array (we want the
    # y-value so it would be: hull[point][0][1]).

    # we're using hull_counter b/c we did not know how to get the length of the hull array
    #  print 'this is the size', np.size(hull,0)

    # step through all points in convex hull
    # so, the way you step through a for loop WITH A NUMBER in Python is by using range
    for p in range(hull_counter):    
       # print "This is the point"
       # print p 
        if hull[p][0][1] < vert_center:
            # we dont want just the y-value, we append the whole point
            listOfPointsAboveCenter.append(hull[p][0])
        elif hull[p][0][1] >= vert_center:
            listOfPointsBelowCenter.append(hull[p][0])

    # This is how we initialized these:
    # First we looked up the documentation of boundingRect.
    # From documentation: "Let (x,y) be the top-left coordinate of the rectangle and (w,h) be its width and height"
    # Then we printed out all the elements in hull with a for loop
    # We saw that each element is a 2d array but printed out the type of ea element to verify
    # Then we indexed the hull array by 3 to get the X coordinate of the first element in the hull array
    # The command: print hull[0][0][0]
    # This is what we use to initialize these guys:

    # declare and initialize left and right most points below center
    intLeftMostPointBelowCenter = hull[0][0][0]

    intRightMostPointBelowCenter = hull[0][0][0]

    



    # determine left most point below center
    # when we ran this: for p in listOfPointsBelowCenter:
    # it produced the same error as the lil code block above
    # so we are again using the for loop syntax WITH A NUMBERRRRRR get it


    # an array is not the same thing as a list
    # From DocumentationL "They both can be used to store any data type (real numbers, 
    # strings, etc), and they both can be indexed and iterated through, but the similarities 
    # between the two don't go much further. The main difference between a list and an array is 
    # the functions that you can perform to them. For example, you can divide an array by 3, and 
    # each number in the array will be divided by 3 a"
    # So basically, an array is not a list. It does not have its numbers separated by a comma.
    # It is just [number {space} number]..] like a matrix
    # WOOOOOWWWWW
    # so above, we used hull_counter because hull is an array. here, we use range(len()) because
    # listOfPointsBelowCenter is a list.

    for p in range(len(listOfPointsBelowCenter)):
        if hull[p][0][0] < intLeftMostPointBelowCenter:
            intLeftMostPointBelowCenter = hull[p][0][0]

    for p in range(len(listOfPointsBelowCenter)):
        if hull[p][0][0] > intRightMostPointBelowCenter:
            intRightMostPointBelowCenter = hull[p][0][0]

   
    # to do this for loop, we first printed out the elements in listOfPointsAboveCenter to see
    # see note above for how to properly index it
    # print type(listOfPointsAboveCenter)
        


#    Here, we found out that the list is 2d not 3d
#    print "this is the list"
#    print listOfPointsAboveCenter
#    for p in listOfPointsAboveCenter:
#        print p 
    # step through all points above center
    for p in range(len(listOfPointsAboveCenter)):
        # if any point is farther left or right than extreme left and right most lower points
        if (listOfPointsAboveCenter[p][0] < intLeftMostPointBelowCenter) or  (listOfPointsAboveCenter[p][0] > intRightMostPointBelowCenter):
            # then shape does not constitute pointing up, return false
            print 'stopping here'
            return False    

    # if we get here, shape has passed pointing up checks  
    # return True

    print 'n    I T S  S S S  A  A  L L I I I V  V VE  E E E   '

    return True

    
##########################################################
##
##                FIND_CONTOURS
##  INPUT: edge image 
##  OUTPUT: a list of contours found in the image
##  input, gives all the contours, contour approximation compresses horizontal, 
##  vertical, and diagonal segments and leaves only their end points. For example, 
##  an up-right rectangular contour is encoded with 4 points.
##  Optional output vector, containing information about the image topology. 
##  It has as many elements as the number of contours.
##
#########################################################

def find_contours(image):
########## COPY IMAGE ###############

#    cv2.imshow('img in find contours', image)

    clone = image.copy()

########### MAKE IMAGE BINARY ###########
# Required for finding contours (better accuracy)
    ret, threshed_img = cv2.threshold(clone, 127, 255, cv2.THRESH_BINARY)

########## FIND CONTOURS ################
    r_image, contours, hierarchy = cv2.findContours(threshed_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # options for contour parameters: external and simple OR tree and none
    
    # sorts contours and gives the largest 10

###    contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
 #   print 'these are the contours', contours    

    # list of contours
    return contours








########### DRAW CONTOURS #################
##    for i in contours:
        # get convex hull
 ##       hull = cv2.convexHull(i)
        #print hull
        # draw the contour
  ##      cv2.drawContours(colimage, [hull], -1, (0, 255,0), 2)

    

        #i = hierarchy[i][0]
    #draw = cv2.drawContours(mod_image, contours, -1, (0,255,0), 10)
  ####  colimage = colimage - clone2
    #cv2.imshow("contours", colimage) 
    #cv2.drawContours(mod_image, contours, i, 'blue', CV_FILLED, 8, hierarchy)
   ### return colimage

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


#################################################################
##
##                   FIND_CONE
##   INPUT: an image
##   OUTPUT: a list
##
##
#################################################################
def find_cone(image):
    cone_spotted = False

#    cv2.imshow('ORIGINAL', image)
############ PRE-PROCESSING #############
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
 #   cv2.imshow('BGR2RGB', image)
    # we want to eliminate noise from our image. (Blurs an image using a Gaussian filter.)
    image_blur = cv2.GaussianBlur(image, (7, 7), 0)
  #  cv2.imshow('blur', image_blur)
    # unlike RGB, HSV separates luma, or the image intensity, from chroma or the color information.
    # just want to focus on color, segmentation
    image_hsv = cv2.cvtColor(image_blur, cv2.COLOR_RGB2HSV)
   # cv2.imshow('HSV', image_hsv)

###########  THRESHOLDING #############
    # Filter by colour
    # 0-10 hue
    #minimum orange amount, max orange amount
    min_orange = np.array([0, 193, 115])
    max_orange = np.array([15, 255, 255])
    mask1 = cv2.inRange(image_hsv, min_orange, max_orange)


    # Filter by brightness
    # brightness of a color is hue
    # 170-180 hue
    min_orange2 = np.array([159, 135, 132])
    max_orange2 = np.array([179, 255, 255])
    mask2 = cv2.inRange(image_hsv, min_orange2, max_orange2)


    # Thresholded Image (by both color and brightness)
    # looking for what is in both ranges
    # Combine masks
    # performs a logical OR       
    thresholded = (mask1 + mask2) - (mask1-mask2) - (mask2-mask1)

   # cv2.imshow('thresholded', thresholded)


    #kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    #morph the image. closing operation Dilation followed by Erosion. 
    #It is useful in closing small holes inside the foreground objects, 
    #or small black points on the object.
    #mask_closed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    #erosion followed by dilation. It is useful in removing noise
    #mask_clean = cv2.morphologyEx(mask_closed, cv2.MORPH_OPEN, kernel)
    #cv2.imshow("mask-clean", mask_clean)


############## CLONE IMAGE ################
# Clone thresholded image before smoothing
    thresholded_image = thresholded.copy()


############### ERODE #####################
    kernel = np.ones((5,5), np.uint8)
    eroded_image = cv2.erode(thresholded_image, kernel, 1)

    #cv2.imshow('eroded',eroded_image)


############## DILATE #####################

    img_dilation = cv2.dilate(eroded_image, kernel, iterations=1)

    #cv2.imshow('dilated',img_dilation)
  
########### GAUSSIAN BLUR ##################

    # Blurs an image using a Gaussian filter. input, kernel size, how much to filter, empty)
    image_blur = cv2.GaussianBlur(img_dilation, (7, 7), 0)
#    cv2.imshow('another blur', image_blur)
########### CANNY EDGE #####################
    edge = cv2.Canny(image_blur, 4000, 4500, apertureSize=5)
#    cv2.imshow('edge',edge)
    cloned_edge = edge.copy()
 #   cv2.imshow('cloned edge', cloned_edge)
########## UPDATING BOOLEAN  ###############
    
    actual_cone = mask1.any() and mask2.any()
#        print "AAAAAAAAAAAA"   

########### FIND CONTOURS #################
        # gets rid of noise in canny edge image
        # makes everything in the image a smooth shape
        # gets list of contours

    contours = find_contours(cloned_edge)
#    print 'these are the contours', contours
    copy_contours = contours
    cont_array = np.array(contours)

    if actual_cone == True:
        cone_spotted = True
        print 'GOT A CONE!!!!'

        # makes a binary image by converting to grayscale and then thresholding to B&W
        ###contour = cv2.cvtColor(contours, cv2.COLOR_BGR2GRAY)
        ###thresh, clone = cv2.threshold(contour, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        list_contours = []
########### APPROX POLY ###################
        for c in contours:
            peri = cv2.arcLength(c, True)
            #peri = .8
            approx = cv2.approxPolyDP(c, 8, True)
            list_contours.append(approx)

#            print "got the approx"

      
########## CONVEX HULL & DRAWING ##########
        thresh = thresholded.copy()
        h = np.size(thresh,0)
        w = np.size(thresh,1)
        blank = np.zeros([h,w,4],dtype=np.uint8)
       
        for i in list_contours:


        # get convex hull
            hull = cv2.convexHull(i)

        # next check to see if it's between 3 and 10 but in order to do that we need a counter
            hull_counter = 0
            for h in hull:
               hull_counter = hull_counter + 1

            # only draws convex hulls for polygons that have hulls between 3 and 10 AND that are pointing up
 #           print ("hull counter is %d" % ( hull_counter))

            list_cone_contours = []

            # check to see if it's between 3 and 10
          #  aHull = cv2.drawContours(blank , [hull], -1, (0, 255,0), 2)
          #  cv2.imshow("HULL" , aHull)
            if (hull_counter > 3) and (hull_counter < 10):

                # if convex hull is pointing up... 
                returnedHull, viableHullFound = convexHullPassesAspectRatioTest(hull)
                if (viableHullFound):
                   
                    if (convexHullIsPointingUp(returnedHull, hull_counter)):
                        # if we get in here we have passed all the ifs, 
                        # therefore the convex hull is a cone, so add to list
                        list_cone_contour = list_cone_contours.append(hull)
                        # and findtrafficdraw it
                        passed = cv2.drawContours(blank , [hull], -1, (0, 255,0), 2)
#                        cv2.imshow("PASSED", passed)
                        # else if convex hull was not pointing up, 
                        # return to top of For without adding to list of cones

                    else:
                        cx = 0
                        cy = 0
                        cone_spotted = False
                        return edge, cone_spotted, cx, cy



################ MOMENTS ###################
# used to get center of mass
     #   print copy_contours
        cnt = copy_contours[0]
      #  print cnt
        M = cv2.moments(cnt)

        print "GOT THE MOMENTS TOO"
        
        if (M['m00'] != 0): 
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00']) 
 #           print cx
  #          print cy
            circle = cv2.circle(blank, (cx,cy), 2, (255,255,255), 3)
   #         print "showing ;sdknhg"
    #        cv2.imshow('center of mass', circle)
#            cv2.waitKey(0)
   ###### this return should be inside the if statement ###########
        #cx = 0
        #cy = 0
            return blank, cone_spotted, cx, cy

    # else, if actual_cone == false:
    print 'no cone spotted'

    cx = 0
    cy = 0
    return edge, cone_spotted, cx, cy

#read the image
#image = cv2.imread('TEST.jpg')
#image = cv2.imread('cone_4_2017-07-06_11:41:55__color.PNG')
#image = cv2.imread('cone_5_2017-07-06_11:42:20__color.PNG')
#image = cv2.imread('cone1.PNG')
#detect it
#result = find_cone(image)


###############################
# then, clone original image so we don't have to alter original image
# next, draw found cones on image
# then draw small dot at center of mass of cone
# then show number of found traffic cones in info text box
#show updated image

##############################3



#find_biggest_contour(image)
#write the new image0
#cv2.imwrite('CONEINSIDE-FAR.PNG', result)
