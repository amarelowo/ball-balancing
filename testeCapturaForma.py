import cv2 as cv
import numpy as np
from config import *

capture =  cv.VideoCapture(1)
kernel = np.ones((5,5), np.uint8)

while True:

    success, frame = capture.read()
    if frame is None:
        break
    
    cv.imshow("Camera", frame)
    frame = cv.medianBlur(frame, 9)
    frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    frameCores = cv.inRange(frame, azulInferior, azulSuperior)
    # mask = cv.erode(frameCores, None, iterations=2)
    # mask = cv.dilate(frameCores,None,iterations=2)
    
    # frameGray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # frameA = cv.medianBlur(frameGray, 7)
    # frameA = cv.threshold(frameA, 90, 200, cv.THRESH_BINARY_INV)[1]
    # frameA = cv.morphologyEx(frameA, cv.MORPH_CLOSE, kernel)
    # canny = cv.Canny(frameA,50,100)

    # c = cv.HoughCircles(canny, cv.HOUGH_GRADIENT
    #                         ,dp=1.1
    #                         ,minDist=150
    #                         ,param1=200
    #                         ,param2=40
    #                         ,minRadius=30
    #                         ,maxRadius=100)

    # #c = np.uint16(np.around(c))

    # print(c)
    # # if c != None:
    # #     for i in c[0,:]:
    # #         cv.circle(frame,(int(i[0]),int(i[1])), int(i[2]),(0,255,0),2)
    # #         #cv.circle(frame,(int(c[0]),int(c[1])), 2,(255,0,0),10)

    #cv.imshow("Filtro", canny)
    

    cv.imshow("Filtro", frameCores)

    key = cv.waitKey(30)
    if key == ord('q') or key == 27:
        break