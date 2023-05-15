import cv2 as cv
import numpy as np
from config import *
from identificadores import *

capture = cv.VideoCapture(1)
box,__,__,__ = selecBox(capture)

while(True):
    
    __,frame = capture.read()
    if frame is None:
        break

    frame = frame[int(box[0][1]):int(box[2][1]),int(box[0][0]):int(box[2][0])]
    kernel = np.ones((5,5), np.uint8)
    grey = cv.medianBlur(frame,3)    

    grey = cv.cvtColor(grey, cv.COLOR_BGR2HSV)
    grey = cv.inRange(grey,COR["branco"][0],COR["branco"][1])

    # grey = cv.cvtColor(grey, cv.COLOR_BGR2GRAY)
    # grey = cv.erode(grey, None, iterations=2)
    grey = cv.dilate(grey,None,iterations=2)

    # grey = cv.morphologyEx(grey, cv.MORPH_OPEN, kernel)
    # grey = cv.morphologyEx(grey, cv.MORPH_CLOSE, kernel)
    # grey = cv.threshold(grey,40,255,cv.THRESH_BINARY_INV)[1]
    # grey = cv.morphologyEx(grey, cv.MORPH_CLOSE, kernel)
    canny = cv.Canny(grey,100,200)

    circles = cv.HoughCircles(grey,cv.HOUGH_GRADIENT,
                              dp=2.5,minDist=1000,
                              param1=100,
                              param2=40,
                              minRadius=10, 
                              maxRadius=30)
    
    # Changing the dtype  to int
    
    if not circles is None:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            # draw the outer circle
            cv.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv.circle(frame,(i[0],i[1]),2,(255,0,0),2)

    cv.imshow("Canny", canny)
    cv.imshow("Cam", frame)
    key = cv.waitKey(30)
    if key == ord('q') or key == 27:
        break

capture.release()
cv.destroyAllWindows()