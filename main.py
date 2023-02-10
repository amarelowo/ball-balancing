import cv2 as cv
import threading
import numpy as np

from config import *
from identificadores import *
from pid import *

configuracoes = {
"Esp-conectado": False
}

if (configuracoes["Esp-conectado"]):
    import ComunicacaoSerial


bola = circulo(COR["amarelo"])
canaleta = retangulo(COR["verde"])

capture =  cv.VideoCapture(1)
box, maxRange, cArea, __ = canaleta.encontrarPlataforma(capture)

while True:

    __, frame = capture.read()
    if frame is None:
        break
    
    xBola, yBola, raio = bola.coordenadas(frame)
    

    if bola.encontrouCirculo():
        dist = xBola - cArea[0] 

        
        distFormatada = map(dist, -maxRange,maxRange,0, 1000)

        cv.circle(frame, (xBola, yBola), raio, (0,255,0), 2)
        cv.line(frame,(xBola,yBola),(cArea),(255,0,255),2)
        cv.putText(frame,f"Dist: {dist} DistFor: {int(distFormatada)}",(75,75),cv.FONT_HERSHEY_SIMPLEX, 1,(255,0,0),2,cv.LINE_AA)

        #-------------- Envia os dados para a esp --------------
        if (configuracoes["Esp-conectado"]):
            data = threading.Thread(target=ComunicacaoSerial.enviarDados(int(distFormatada)))
            data.start()

    else:
        if (configuracoes["Esp-conectado"]):
            data = threading.Thread(target=ComunicacaoSerial.enviarDados(90))
            data.start()
  
    cv.circle(frame, (cArea), 2,(0,255,255),3)
    cv.drawContours(frame,[box],0,(255,255,255),1)
    # cv.putText(frame,"1",(box[0]),cv.FONT_HERSHEY_SIMPLEX, 1,(255,0,0),2,cv.LINE_AA)
    # cv.putText(frame,"2",(box[1]),cv.FONT_HERSHEY_SIMPLEX, 1,(255,0,0),2,cv.LINE_AA)
    # cv.putText(frame,"3",(box[2]),cv.FONT_HERSHEY_SIMPLEX, 1,(255,0,0),2,cv.LINE_AA)
    # cv.putText(frame,"4",(box[3]),cv.FONT_HERSHEY_SIMPLEX, 1,(255,0,0),2,cv.LINE_AA)

    cv.imshow("Camera", frame)
    
    key = cv.waitKey(30)
    if key == ord('q') or key == 27:
        break


capture.release()
cv.destroyAllWindows()