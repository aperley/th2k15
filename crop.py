import cv2
import cv2.cv as cv
import numpy as np

def order_points(pts):
    # top-left, top-right, bottom-right, bottom-left
    rect = np.zeros((4, 2), dtype=np.float32)
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect

def four_point_transform(image, rect):
    (tl, tr, br, bl) = rect

    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[0] - bl[0]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[0] - tl[0]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
 
    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[1] - br[1]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[1] - bl[1]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")
 
    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
 
    # return the warped image
    return warped

def crop(im):
    preview = im.copy()
    imc = im.copy()
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    im = cv2.GaussianBlur(im, (9,9), 0)

    circles = cv2.HoughCircles(im, cv.CV_HOUGH_GRADIENT, 1, 20,
                               param1=200, param2=30,
                               minRadius=0, maxRadius=100)

    pts = []
    if circles is None:
        return False, None, preview, None

    for cir in circles[0]:
        pts.append(cir[0:2])
    pts = np.array(pts)
    print len(pts)

    rect = order_points(pts)
    tl, tr, br, bl = rect

    okay = (abs(np.sum((tl - tr)**2)**0.5 - np.sum((br - bl)**2)**0.5) < 50 and
           abs(np.sum((tl - bl)**2)**0.5 - np.sum((tr - br)**2)**0.5) < 50)


    mean = im.mean()
    for cir in rect:
        cv2.circle(im, (cir[0], cir[1]), 35, mean, -1)
        cv2.circle(preview, (cir[0], cir[1]), 20, (255, 0, 0), 3)

    warped = four_point_transform(imc, rect)
    return okay, warped, preview, rect

def doWarp(im, rect):
    return four_point_transform(im, rect)
