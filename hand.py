import cv2
import cv2.cv as cv
import numpy as np

# HSV ranges to detect bright orange

lower = [2,200,200]
upper = [6,240,255]

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

        # We might not even need this
        thresh_copy = np.copy(thresh)

        contours,hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                              cv2.CHAIN_APPROX_SIMPLE)

        cnt = contours[0]
        M = cv2.moments(cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])

        return (cx,cy)

