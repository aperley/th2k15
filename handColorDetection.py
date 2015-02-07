import cv2
import cv2.cv as cv
import numpy as np


## Code for testing ##
hand = cv2.imread('orange2.png')
hsv_hand = cv2.cvtColor(hand, cv2.COLOR_BGR2HSV)
hand = cv2.cvtColor(hand, cv2.COLOR_BGR2GRAY)


def on_mouse(event, x, y, flags, thing):
    if event == cv.CV_EVENT_LBUTTONDOWN:
        print (x, y), hsv_hand[(y,x)]
                             
cv2.namedWindow('image')
cv.SetMouseCallback('image', on_mouse, 0)
cv2.imshow('image',hsv_hand)

cv2.waitKey(0) & 0xFF
cv2.destroyAllWindows()
