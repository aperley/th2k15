import cv2
import cv2.cv as cv
import numpy as np

# HSV ranges to detect bright orange

lower = [0,100,230]
upper = [20,200,256]

## Code for testing ##
#hand = cv2.imread('hand3.jpg')
#small_hand = cv2.resize(hand, (640,480))

# hand is a cropped, color image
def findFingerXY(hand):
        hsv_hand = cv2.cvtColor(hand, cv2.COLOR_BGR2HSV)
        hand = cv2.cvtColor(hand, cv2.COLOR_BGR2GRAY)

        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")

        mask = cv2.inRange(hsv_hand, lower, upper)
        output = cv2.bitwise_and(hsv_hand, hsv_hand, mask=mask)


        output = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(output, 110,255,0)

        # For robustness
        kernel = np.ones((5, 5), np.uint8)
        thresh = cv2.dilate(thresh, kernel, iterations=2)
        thresh = cv2.erode(thresh, kernel, iterations=2)

        thresh_copy = np.copy(thresh)
        thresh_copy = cv2.cvtColor(thresh_copy, cv2.COLOR_GRAY2BGR)

        # We might not even need this
        thresh_copy = np.copy(thresh)

        contours,hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                              cv2.CHAIN_APPROX_SIMPLE)

        contours = filter(lambda c: len(c) > 35, contours)
        if len(contours) > 0:
                cnt = contours[0]
                M = cv2.moments(cnt)
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])

                return (cx,cy)
        else:
                return (-5,-5)

