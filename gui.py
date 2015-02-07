import math
import numpy as np
import cv2
import cv2.cv as cv
import crop
from contours2 import getBounds
from hand import findFingerXY

class XyloGui(object):
    def __init__(self, cam):
        self.cam = cam
        self.fingerDotLoc = (-5,-5) #(x,y)

    def makeRainbowGradient(f1=0.5,f2=0.5,f3=0.5,
                            p1=0,p2=2,p3=4,c=128,w=127):
        self.rainbow = []
        for i in xrange(len(contours)):
            r = (math.sin(f1*i + p1))*w + c
            g = (math.sin(f2*i + p2))*w + c
            b = (math.sin(f3*i + p3))*w + c
            rainbow.append((b,g,r))
        return self.rainbow

    def assignNotes(self):
        self.notes = []
        for i in xrange(len(self.contours)):
            self.notes.append(0)
             
    def playNote(self,idx):
        print "Note %d: %d"%(i, self.notes[i])           

    def initTemplate(self):
        doLock = False
        while True:
            ret, im = self.cam.read()
            okay, warped, preview, rect = crop.crop(im)
            cv2.imshow('image', preview[::-1, ::-1])

            if cv2.waitKey(1) == ord('a'):
                doLock = True
                print "Waiting for lock"

            if doLock:
                self.template = warped
                self.rect = rect
                break
        (self.contours, self.thresh) = getBounds(self.template)
        self.blankThresh = self.thresh.copy()
        self.makeRainbowGradient()
        self.assignNotes()

    def processFrame(self,frame):
        (x,y) = findFingerXY(frame)
        t = np.copy(self.thresh)
        if x > 0:
            self.fingerDotLoc = (x,y)
            for i, contour in enumerate(self.contours):
                dist = cv2.pointPolygonTest(contour, (x, y), False)
                if dist > 0:
                    self.playNote(i)
                    color = self.rainbow[i]                  
                    cv2.drawContours(t,[contour],-1,color,-1)
                    cv2.circle(t,(x,y), 10, (0,127,255), -1)
                    return t
            # No highlight, but yes finger    
            cv2.circle(t,(x,y), 10, (0,127,255), -1)
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
            cv2.imshow('image', disp[::-1, ::-1])
            if cv2.waitKey(1) == ord('q'):
                cv2.destroyAllWindows()
                return
        



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
                    

gui = XyloGui(cv2.VideoCapture(0))
gui.run()


