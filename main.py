import cv2 as cv
from config import *
from identificadores import *


bola = circulo(azulInferior, azulSuperior)

capture =  cv.VideoCapture(1)
while True:

    success, frame = capture.read()
    if frame is None:
        break
    
    x, y, r = bola.coordenadas(frame)

    #print(bola.encontrouCirculo())
    if bola.encontrouCirculo():
        cv.circle(frame, (x, y), r, (0,255,0), 2)
        


    cv.imshow("Camera", frame)
    

    key = cv.waitKey(30)
    if key == ord('q') or key == 27:
        break