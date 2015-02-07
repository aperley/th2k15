import math
import numpy as np
import cv2
import cv2.cv as cv
import crop
from contours2 import getBounds
from hand import findFingerXY

from Queue import Queue
import threading
from pydub import AudioSegment
from pydub import playback
from pydub import effects
import webbrowser

class XyloGui(object):
    def __init__(self, cam, queue):
        self.cam = cam
        self.queue = queue
        self.fingerDotLoc = (-5,-5) #(x,y)
        self.lastIdx = None


        
    def sortContours(self):
        return self.contours
        maxes = map((lambda cnt : cnt[0][0]),self.contours)

        sortt = sorted(enumerate(maxes),
                       cmp=lambda a, b: cmp(a[1], b[1]))
        sortedCnt = []
        for (i,pair) in enumerate(sortt):
            sortedCnt.append(sortt[i])
        return sortedCnt
            

    def makeRainbowGradient(self, f1=0.5,f2=0.5,f3=0.5,
                            p1=0,p2=2,p3=4,c=128,w=127):
        self.rainbow = []
        for i in xrange(len(self.contours)):
            r = (math.sin(f1*i + p1))*w + c
            g = (math.sin(f2*i + p2))*w + c
            b = (math.sin(f3*i + p3))*w + c
            self.rainbow.append((b,g,r))
        return self.rainbow

    def assignNotes(self):
        self.notes = []
        for i in xrange(len(self.contours)):
            self.notes.append(0)
             
    def playNote(self,idx):
        if idx != self.lastIdx:
            self.lastIdx = idx
            print "Note %d: %d"%(idx, self.notes[idx]) 
            if self.queue.empty():
                self.queue.put(idx)
                #if idx == 3:
                #    webbrowser.open("https://www.youtube.com/watch?v=HMUDVMiITOU#t=19")        

    def initTemplate(self):
        doLock = False
        while True:
            ret, im = self.cam.read()
            assert(ret)
            okay, warped, preview, rect = crop.crop(im)
            cv2.imshow('image', preview[::-1, ::-1])

            if cv2.waitKey(1) == ord('a'):
                doLock = True
                print "Waiting for lock"

            if doLock and okay:
                self.template = warped
                self.rect = rect
                break
        (self.contours, self.thresh) = getBounds(self.template)
        self.contours = self.sortContours()
        self.makeRainbowGradient()
        self.default = np.zeros(np.shape(self.thresh),dtype='uint8')
        for i in xrange(len(self.contours)):
            color = self.rainbow[i]
            cv2.drawContours(self.default, [self.contours[i]],-1,color,3)
        self.assignNotes()

    def processFrame(self,frame):
        (x,y) = findFingerXY(frame)
        t = np.copy(self.default)
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
            self.lastIdx = None
            return t
        self.lastIdx = None
        return self.default
            

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
        
        #cv.SetMouseCallback('image', self.on_mouse, 0)
        #launch window

        while True:
            ret, im = self.cam.read()
            warped = crop.doWarp(im, self.rect)
            disp = self.processFrame(warped)
            cv2.imshow('image', disp[::-1, ::-1])
            if cv2.waitKey(1) == ord('q'):
                cv2.destroyAllWindows()
                self.queue.put(-1)
                return
        

    def onHit(self, i):
        print i
        if queue.empty():
            if i == 0:
                webbrowser.open("https://www.youtube.com/watch?v=HMUDVMiITOU")
            else:
                self.queue.put(i)

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
                    


def audioWorker(queue):
    files = [
        'PatchArena_marimba-060-c3.wav',
        'PatchArena_marimba-062-d3.wav',
        'PatchArena_marimba-064-e3.wav',
        'PatchArena_marimba-065-f3.wav',
        'PatchArena_marimba-067-g3.wav',
        'PatchArena_marimba-069-a3.wav',
        'PatchArena_marimba-071-h3.wav',
        'PatchArena_marimba-072-c4.wav',

    ]
    notes = map(AudioSegment.from_wav, files)
    while True:
        val = queue.get()
        if val < 0:
            return
        print "HIT:", val
        playback.play(notes[val][:300])

queue = Queue()
worker = threading.Thread(target=audioWorker, args=(queue,))
gui = XyloGui(cv2.VideoCapture(0), queue)
worker.start()
gui.run()


