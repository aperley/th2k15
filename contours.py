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

    cv2.imshow('',thresh)
    cv2.waitKey(0) & 0xFF


    thresh_copy = np.copy(thresh)
    
    cv2.imshow('',thresh_copy)
    cv2.waitKey(0) & 0xFF
    

    #Calculate contours
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)

    print contours
    cv2.destroyAllWindows()

    #cv2.drawContours(thresh, contours, -1, (0,255,0), 3)


getBounds(disp)
