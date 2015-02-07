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




def getBounds(img):
    # Grayscale and thresholding
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #img = cv2.GaussianBlur(img, (0, 0), 0.5)
    #ret, thresh = cv2.threshold(img, 120, 255, 1)
    thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    cv2.THRESH_BINARY_INV, 11, 3)


    kernel = np.ones((5, 5), np.uint8)
    thresh = cv2.dilate(thresh, kernel, iterations=1)
    thresh = cv2.erode(thresh, kernel, iterations=1)

    thresh_copy = np.copy(thresh)
    thresh_copy = cv2.cvtColor(thresh_copy, cv2.COLOR_GRAY2BGR)
    

    #Calculate contours
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)

    #print contours
    contours = filter(lambda c: len(c) > 50, contours)

    return (contours,thresh_copy)


    


