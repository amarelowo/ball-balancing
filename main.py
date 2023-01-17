import cv2 as cv
import threading
import numpy as np

from config import *
from identificadores import *
from pid import *

configuracoes = {
"Esp-conectado": True
}

if (configuracoes["Esp-conectado"]):
    import ComunicacaoSerial



bola = circulo(amareloInferior, amareloSuperior)
canaleta = retangulo(marromInferior,marromSuperior)
servo = pid( kP=1.0, kI=0, kD=0, setPoint=0)

capture =  cv.VideoCapture(1)
box, maxRange, cArea, __ = canaleta.encontrarPlataforma(capture)


while True:

    __, frame = capture.read()
    if frame is None:
        break

    #UMA IDEIA DO QUE O FILTRO DO IDENTIFICADOR ESTA CAPTANDO
    frame2 = cv.medianBlur(frame, 3)
    frame2 = cv.cvtColor(frame2, cv.COLOR_BGR2HSV)
    frameMarrom = cv.inRange(frame2, marromInferior, marromSuperior)
    frameAmarelo = cv.inRange(frame2, amareloInferior, amareloSuperior)
    
    
    x, y, r = bola.coordenadas(frame)
    

    if bola.encontrouCirculo():
        dist = cArea[0] - x
    
        posServo = servo.process(dist)

        if maxRange < 0:
            maxRange = maxRange*(-1)

        posServoAjustada = map(posServo, in_min= -maxRange, in_max= maxRange, out_min=0, out_max=180)
        print(f"Dist: {dist}, pos: {posServo}, ajuste: {int(posServoAjustada)}")



        cv.circle(frame, (x, y), r, (0,255,0), 2)
        cv.line(frame,(x,y),(cArea),(255,0,255),2)
        cv.putText(frame,f"Distancia: {dist}",(75,75),cv.FONT_HERSHEY_SIMPLEX, 1,(255,0,0),2,cv.LINE_AA)

        #-------------- Envia os dados para a esp --------------
        if (configuracoes["Esp-conectado"]):
            data = threading.Thread(target=ComunicacaoSerial.enviarDados(int(posServoAjustada)))
            data.start()
            #ComunicacaoSerial.enviarDados(int(posServoAjustada))

  
    cv.circle(frame, (cArea), 2,(0,255,255),3)
    cv.drawContours(frame,[box],0,(255,255,255),1)
    # cv.putText(frame,"1",(box[0]),cv.FONT_HERSHEY_SIMPLEX, 1,(255,0,0),2,cv.LINE_AA)
    # cv.putText(frame,"2",(box[1]),cv.FONT_HERSHEY_SIMPLEX, 1,(255,0,0),2,cv.LINE_AA)
    # cv.putText(frame,"3",(box[2]),cv.FONT_HERSHEY_SIMPLEX, 1,(255,0,0),2,cv.LINE_AA)
    # cv.putText(frame,"4",(box[3]),cv.FONT_HERSHEY_SIMPLEX, 1,(255,0,0),2,cv.LINE_AA)

    cv.imshow("Camera", frame)
    cv.imshow("amarelo", frameAmarelo)
    #cv.imshow("marrom", frameMarrom)
    
    key = cv.waitKey(30)
    if key == ord('q') or key == 27:
        break


capture.release()
cv.destroyAllWindows()