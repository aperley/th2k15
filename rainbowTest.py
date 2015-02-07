import math
import numpy as np
import cv2
import cv2.cv as cv

contours = range(10)

hand = cv2.imread('hand1.jpg')
hand = cv2.resize(hand, (800,600))



def makeRainbowGradient(f1=0.5,f2=0.5,f3=0.5,
                        p1=0,p2=2,p3=4,c=128,w=127):
    rainbow = []
    for i in xrange(len(contours)):
        r = (math.sin(f1*i + p1))*w + c
        g = (math.sin(f2*i + p2))*w + c
        b = (math.sin(f3*i + p3))*w + c
        rainbow.append((b,g,r))
    return rainbow

rb = makeRainbowGradient()

for (i,color) in enumerate(rb):
    print color
    cv2.circle(hand, (50+50*i,50+50*i),40, color, -1)

cv2.imshow('lala',hand)

cv2.waitKey(0)
cv2.destroyAllWindows()




        
        
        
