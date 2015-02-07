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
    #img = cv2.GaussianBlur(img, (0, 0), 0.5)
    #ret, thresh = cv2.threshold(img, 120, 255, 1)
    thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    cv2.THRESH_BINARY_INV, 11, 3)


    kernel = np.ones((5, 5), np.uint8)
    thresh = cv2.dilate(thresh, kernel, iterations=2)
    thresh = cv2.erode(thresh, kernel, iterations=2)

    thresh_copy = np.copy(thresh)
    thresh_copy = cv2.cvtColor(thresh_copy, cv2.COLOR_GRAY2BGR)
    

    #Calculate contours
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)

    #print contours
    contours = filter(lambda c: len(c) > 50, contours)

    blank_thresh = np.copy(thresh_copy)

                            
    cv2.namedWindow('image')
    cv.SetMouseCallback('image', on_mouse, 0)
    cv2.imshow('image',thresh_copy)

    cv2.waitKey(0) & 0xFF
    cv2.destroyAllWindows()
    
    return (contours, thresh_copy)

def onContact(contours,contourIdx,thresh_copy):
    cnt = contours[contourIdx]
    color = (0,255,0)
    # Create an anonymous image to display till release
    t = np.copy(thresh_copy)
    cv2.drawContours(t,[cnt],-1,color,-1)
    cv2.imshow('image',t)

def onRelease(contourIdx,blank_thresh):
    cv2.imshow('image',blank_thresh)

def on_mouse(event, x, y, flags, thing):
    global mode
    if event == cv.CV_EVENT_LBUTTONDOWN:
        print (x, y)
        for i, contour in enumerate(contours):
            dist = cv2.pointPolygonTest(contour, (x, y), False)
            if dist > 0:
                    onContact(i)
                    return
        onRelease(0)



getBounds(disp)

