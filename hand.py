import cv2
import cv2.cv as cv
import numpy as np

# HSV ranges to detect bright orange

lower = [2,200,200]
upper = [6,240,255]

hand = cv2.imread('hand3.jpg')
small_hand = cv2.resize(hand, (640,480))

hsv_hand = cv2.cvtColor(small_hand, cv2.COLOR_BGR2HSV)
small_hand = cv2.cvtColor(small_hand, cv2.COLOR_BGR2GRAY)


#cv2.imshow('HSV',hsv_hand)

lower = np.array(lower, dtype = "uint8")
upper = np.array(upper, dtype = "uint8")

mask = cv2.inRange(hsv_hand, lower, upper)
output = cv2.bitwise_and(hsv_hand, hsv_hand, mask=mask)

#show images

output = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(output, 110,255,0)


#cv2.imshow("lala", thresh)

def on_mouse(event, x, y, flags, thing):
        if event == cv.CV_EVENT_LBUTTONDOWN:
            print (x, y), hsv_hand[(y,x)]
            
  
cv2.namedWindow('image')
cv.SetMouseCallback('image', on_mouse, 0)
#cv2.imshow('image',small_hand)


cv2.waitKey(0) & 0xFF
cv2.destroyAllWindows()


