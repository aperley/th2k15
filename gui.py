import numpy as np
import cv2
import cv2.cv as cv
from crop import crop
from contours2 import getBounds


im = cv2.imread('test.png', cv2.CV_LOAD_IMAGE_GRAYSCALE)

disp = crop(im)

(contours, thresh) = getBounds(disp)

blank_thresh = np.copy(thresh)

def onContact(contourIdx):
    cnt = contours[contourIdx]
    color = (0,255,0)
    # Create an anonymous image to display till release
    t = np.copy(thresh)
    cv2.drawContours(t,[cnt],-1,color,-1)
    cv2.imshow('image',t)

def onRelease():
    cv2.imshow('image',blank_thresh)

def on_mouse(event, x, y, flags, thing):
    if event == cv.CV_EVENT_LBUTTONDOWN:
        print (x, y)
        for i, contour in enumerate(contours):
            dist = cv2.pointPolygonTest(contour, (x, y), False)
            if dist > 0:
                    onContact(i)
                    return
        onRelease()

                        
cv2.namedWindow('image')
cv.SetMouseCallback('image', on_mouse, 0)
cv2.imshow('image',thresh)

cv2.waitKey(0) & 0xFF
cv2.destroyAllWindows()
