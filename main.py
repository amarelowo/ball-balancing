import cv2 as cv
import math
from config import *
from identificadores import *
from pid import *

bola = circulo(amareloInferior, amareloSuperior)
canaleta = retangulo(marromInferior,marromSuperior)
servo = pid( kP=1.0, kI=0, kD=0, setPoint=0)

capture =  cv.VideoCapture(1)


box, area = canaleta.encontrarPlataforma(capture)

print(box[0],box[2])
cArea = centroReta(box[0],box[2])
maxRange = cArea[0] - box[0][0]  
print(cArea,maxRange)

while True:

    success, frame = capture.read()
    if frame is None:
        break
    
    
    x, y, r = bola.coordenadas(frame)

    #box = canaleta.coordenadas(frame)
    

    #print(bola.encontrouCirculo()z)
    if bola.encontrouCirculo():
        #print(f"xBola: {x} | xArea: {cArea[0]}")
        dist = cArea[0] - x
    
        posServo = servo.process(dist)

        if maxRange < 0:
            maxRange = maxRange*(-1)

        posServoAjustada = map(posServo, in_min= -maxRange, in_max= maxRange, out_min=0, out_max=180)
        print(f"Dist: {dist}, pos: {posServo}, ajuste: {int(posServoAjustada)}")




        cv.circle(frame, (x, y), r, (0,255,0), 2)
        cv.putText(frame,f"Distancia: {dist}",(75,75),cv.FONT_HERSHEY_SIMPLEX, 1,(255,0,0),2,cv.LINE_AA)
        cv.line(frame,(x,y),(cArea),(255,0,255),2)

        
    
  
    cv.circle(frame, (cArea), 2,(0,255,255),3)

    #UMA IDEIA DO QUE O FILTRO DO IDENTIFICADOR ESTA CAPTANDO
    frame2 = cv.medianBlur(frame, 3)
    frame2 = cv.cvtColor(frame2, cv.COLOR_BGR2HSV)
    frameMarrom = cv.inRange(frame2, marromInferior, marromSuperior)
    frameAmarelo = cv.inRange(frame2, amareloInferior, amareloSuperior)

    cv.drawContours(frame,[box],0,(255,255,255),1)
    cv.putText(frame,"1",(box[0]),cv.FONT_HERSHEY_SIMPLEX, 1,(255,0,0),2,cv.LINE_AA)
    cv.putText(frame,"2",(box[1]),cv.FONT_HERSHEY_SIMPLEX, 1,(255,0,0),2,cv.LINE_AA)
    cv.putText(frame,"3",(box[2]),cv.FONT_HERSHEY_SIMPLEX, 1,(255,0,0),2,cv.LINE_AA)
    cv.putText(frame,"4",(box[3]),cv.FONT_HERSHEY_SIMPLEX, 1,(255,0,0),2,cv.LINE_AA)

    cv.imshow("Camera", frame)
    #cv.imshow("marrom", frameMarrom)
    cv.imshow("amarelo", frameAmarelo)

    key = cv.waitKey(30)
    if key == ord('q') or key == 27:
        break

cv.destroyAllWindows()