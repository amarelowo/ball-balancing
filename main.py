import cv2 as cv
import time
from config import *
from identificadores import *


bola = circulo(amareloInferior, amareloSuperior)
canaleta = retangulo(marromInferior,marromSuperior)

capture =  cv.VideoCapture(1)


delta = 0
areaMaior = 0
t1 = time.time()
while True:

    success, frame = capture.read()
    if frame is None:
        break
    
    box = canaleta.coordenadas(frame)
    area = canaleta.areaRetangulo()
    #print(area)

    

    if canaleta.encontrouRetangulo():
        cv.drawContours(frame,[box],0,(0,0,0),2)

        if area > areaMaior:
            areaMaior = area
            boxMaior = box
            ##cv.drawContours(frame,[boxMaior],0,(255,255,255),6)

    

    if delta > 5:
        cv.destroyAllWindows()
        break

    #cv.imshow("Area", frame)
    delta = time.time() - t1
    print(round(delta,2))

    
print(boxMaior, area)

p1x = boxMaior[0][0]
p1y = boxMaior[0][1]
p2x = boxMaior[1][0]
p2y = boxMaior[1][1]
p3x = boxMaior[2][0]
p3y = boxMaior[2][1]
p4x = boxMaior[3][0]
p4y = boxMaior[3][1]

#print(p1,p2,p3,p4)
while True:

    success, frame = capture.read()
    if frame is None:
        break
    
    frame = frame[p2y-50:p1y+50, p2x-50:p3x+50]
    x, y, r = bola.coordenadas(frame)
    #box = canaleta.coordenadas(frame)
    cv.circle(frame,(10,10), 10,(0,0,0),10 )

    #print(bola.encontrouCirculo()z)
    if bola.encontrouCirculo():
        cv.circle(frame, (x, y), r, (0,255,0), 2)
        cv.putText(frame,f"{x},{y}",(x,y),cv.FONT_HERSHEY_SIMPLEX, 1,(255,0,0),2,cv.LINE_AA)
        
    
  

    #UMA IDEIA DO QUE O FILTRO DO IDENTIFICADOR ESTA CAPTANDO
    frame2 = cv.medianBlur(frame, 3)
    frame2 = cv.cvtColor(frame2, cv.COLOR_BGR2HSV)
    frameMarrom = cv.inRange(frame2, marromInferior, marromSuperior)
    frameAmarelo = cv.inRange(frame2, amareloInferior, amareloSuperior)

    cv.drawContours(frame,[boxMaior],0,(255,255,255),6)
    cv.putText(frame,"pt1",(boxMaior[0]),cv.FONT_HERSHEY_SIMPLEX, 1,(255,0,0),2,cv.LINE_AA)
    cv.putText(frame,"pt2",(boxMaior[1]),cv.FONT_HERSHEY_SIMPLEX, 1,(255,0,0),2,cv.LINE_AA)
    cv.putText(frame,"pt3",(boxMaior[2]),cv.FONT_HERSHEY_SIMPLEX, 1,(255,0,0),2,cv.LINE_AA)
    cv.putText(frame,"pt4",(boxMaior[3]),cv.FONT_HERSHEY_SIMPLEX, 1,(255,0,0),2,cv.LINE_AA)

    cv.imshow("Camera", frame)
    cv.imshow("marrom", frameMarrom)
    cv.imshow("amarelo", frameAmarelo)

    key = cv.waitKey(30)
    if key == ord('q') or key == 27:
        break

cv.destroyAllWindows()