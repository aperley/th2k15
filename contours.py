"""
import numpy
import cv2

img = cv2.imread('test1.jpg')
cv2.imshow('Contours', img)

cv2.waitKey(0) & 0xFF
cv2.destroyAllWindows()
"""

#640 480

import numpy as np
import cv2
import cv2.cv as cv
from crop import crop


im = cv2.imread('test.png', cv2.CV_LOAD_IMAGE_GRAYSCALE)
disp = crop(im)



def getBounds(img):
    # Grayscale and thresholding
    #imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img, 110, 255, 1)



    thresh_copy = np.copy(thresh)
    thresh_copy = cv2.cvtColor(thresh_copy, cv2.COLOR_GRAY2BGR)
    
    kernel = np.ones((5, 5), np.uint8)
    thresh = cv2.dilate(thresh, kernel, iterations=1)
    

    #Calculate contours
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)

    print contours

    cv2.drawContours(thresh_copy, contours, -1, (0,255,0), 3)


    def on_mouse(event, x, y, flags, thing):
        if event == cv.CV_EVENT_LBUTTONDOWN:
            print (x, y)
            for i, contour in enumerate(contours):
                dist = cv2.pointPolygonTest(contour, (x, y), False)
                if dist > 0:
                    print "We're inside contour %d" % i


    
    cv2.namedWindow('image')
    cv.SetMouseCallback('image', on_mouse, 0)
    cv2.imshow('image',thresh_copy)

    cv2.waitKey(0) & 0xFF
    cv2.destroyAllWindows()
    


getBounds(disp)
