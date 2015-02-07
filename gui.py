import numpy as np
import cv2
import cv2.cv as cv
from crop import crop
from contours2 import getBounds
from hand import findFingerXY

class XyloGui(object):
    def __init__(self, cam):
        self.cam = cam
        self.figerDotLoc = (-5,-5) #(x,y)

        
        
    def processFrame(self,frame):
        (x,y) = findFingerXY(frame)
        if x > 0:
            self.fingerDotLoc = (x,y)
            for i, contour in enumerate(self.contours):
                dist = cv2.pointPolygonTest(contour, (x, y), False)
                if dist > 0:
                    color = (0,255,0)
                    # Create an anonymous image to display till release
                    t = np.copy(self.thresh)
                    cv2.drawContours(t,[contour],-1,color,-1)
                    return t
        return self.blankThresh
            
            

    def on_mouse(self,event, x, y, flags, thing):
        if event == cv.CV_EVENT_LBUTTONDOWN:
            print (x, y)
            for i, contour in enumerate(self.contours):
                dist = cv2.pointPolygonTest(contour, (x, y), False)
                if dist > 0:
                        self.onContact(i)
                        return
            self.onRelease()

    def run(self):
        cv2.namedWindow('image')
        self.initTemplate()
        
        cv.SetMouseCallback('image', self.on_mouse, 0)
        #launch window

        while True:
            ret, im = self.cam.read()
            warped = crop.doWarp(im, self.rect)
            disp = self.processFrame(warped)
            cv2.imshow('image', disp)
            if cv2.waitKey(1) == ord('q'):
                cv2.destroyAllWindows()
                return
        

    def initTemplate(self):
        while True:
            ret, im = self.cam.read()
            okay, warped, preview, rect = crop.crop(im)
            cv2.imshow('image', preview)

            if cv2.waitKey(1) == ord('a'):
                self.template = warped
                self.rect = rect
                break
        (self.contours, self.thresh) = getBounds(self.template)
        self.blankThresh = self.thresh.copy()

def processFrame(frame,thresh):
    cv2.imShow('image',thresh)
    (x,y) = findFingerXY(frame)
    if x > 0:
        cv2.circle(thresh,(x,y), 4, (0,127,255), -1)
        cv2.imShow('image',thresh)

def onContact(self,contourIdx):
    self.contourIdx
    cnt = contours[contourIdx]
    color = (0,255,0)
    # Create an anonymous image to display till release
    t = np.copy(thresh)
    cv2.drawContours(t,[cnt],-1,color,-1)

def onRelease(self):
    cv2.imshow('image',blank_thresh)
                    

cv2.imshow('image',thresh)


