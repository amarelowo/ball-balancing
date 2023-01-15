import cv2 as cv
from config import *
from identificadores import *


bola = circulo(amareloInferior, amareloSuperior)
canaleta = retangulo(vermelhoInferior,vermelhoSuperior)


capture =  cv.VideoCapture(0)
while True:

    success, frame = capture.read()
    if frame is None:
        break
    
    x, y, r = bola.coordenadas(frame)
    box = canaleta.coordenadas(frame)

    #print(bola.encontrouCirculo())
    if bola.encontrouCirculo():
        cv.circle(frame, (x, y), r, (0,255,0), 2)
        cv.putText(frame,"bola",(x,y),cv.FONT_HERSHEY_SIMPLEX, 1,(255,0,0),2,cv.LINE_AA)
        
    if canaleta.encontrouRetangulo():
        cv.drawContours(frame,[box],0,(0,0,255),2)

        cv.putText(frame,"box1",box[1],cv.FONT_HERSHEY_SIMPLEX, 1,(255,0,0),2,cv.LINE_AA)
    
    #UMA IDEIA DO QUE O FILTRO DO IDENTIFICADOR ESTA CAPTANDO
    frame2 = cv.medianBlur(frame, 3)
    frame2 = cv.cvtColor(frame2, cv.COLOR_BGR2HSV)
    frame2 = cv.inRange(frame2, vermelhoInferior, vermelhoSuperior)

    cv.imshow("Camera", frame)
    cv.imshow("filtro", frame2)

    key = cv.waitKey(30)
    if key == ord('q') or key == 27:
        break