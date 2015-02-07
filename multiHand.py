import cv2
import cv2.cv as cv
import numpy as np

# HSV ranges to detect bright orange

lowerB = [0,100,220]
upperB = [15,200,255]

## Code for testing ##
#hand = cv2.imread('hand3.jpg')
#small_hand = cv2.resize(hand, (640,480))

# hand is a cropped, color image
def findFingerXY(hand):
        hsv_hand = cv2.cvtColor(hand, cv2.COLOR_BGR2HSV)
        hand = cv2.cvtColor(hand, cv2.COLOR_BGR2GRAY)

        lower = np.array(lowerB, dtype = "uint8")
        upper = np.array(upperB, dtype = "uint8")

        mask = cv2.inRange(hsv_hand, lower, upper)
        output = cv2.bitwise_and(hsv_hand, hsv_hand, mask=mask)

        cv2.imshow('thresh',output)
        output = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(output, 110,255,0)



        # For robustness
        kernel = np.ones((5, 5), np.uint8)
        thresh = cv2.dilate(thresh, kernel, iterations=5)
        thresh = cv2.erode(thresh, kernel, iterations=5)

        thresh_copy = np.copy(thresh)
        thresh_copy = cv2.cvtColor(thresh_copy, cv2.COLOR_GRAY2BGR)

        # We might not even need this
        thresh_copy = np.copy(thresh)

        contours,hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                              cv2.CHAIN_APPROX_SIMPLE)

        #print type(contours), type(contours[0]), type(contours[0][0])

        #print contours
        #print contours[2]
        #print "lala"
        #print contours[2][0]
        #print contours[2][0][0]
        #print contours[2][0][0][0]
        #print contours[2][0][0][1]
        contours = filter(lambda c: len(c) > 5, contours)
        coords = []
        if len(contours) > 0:
                for cnt in contours:
                        M = cv2.moments(cnt)
                        if M['m00'] != 0:
                                cx = int(M['m10']/M['m00'])
                                cy = int(M['m01']/M['m00'])
                                coords.append((cx,cy))
        return coords


