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
    config = input("Abrir modo coonfiguração de parametros PID?  1 - para sim | 2 - para não: ")
    print(config, type(config))
    if config == "1":
        novoKp = float(input("Novo kP: "))
        novoKi = float(input("Novo kI: "))
        novoKd = float(input("Novo kD: "))
        data = threading.Thread(target=ComunicacaoSerial.enviarDados("c", novoKp, novoKi, novoKd))
        data.start()



bola = circulo(COR["branco"])
canaleta = retangulo(COR["preto"])

capture =  cv.VideoCapture(1)
# box, maxRange, cArea, __ = canaleta.encontrarPlataforma(capture)
box,newBox, maxRange, cArea = selecBox(capture)

while True:

    __, frame = capture.read()
    if frame is None:
        break
    
    frame = frame[int(box[0][1]):int(box[2][1]),int(box[0][0]):int(box[2][0])]
    xBola, yBola, raio = bola.coordenadas(frame)
    

    if bola.encontrouCirculo():
        distX = xBola - cArea[0]
        distY = yBola - cArea[1]


        
        distFormatadaX = int(map(distX, -maxRange[0],maxRange[0],0, 500))
        distFormatadaY = int(map(distY, -maxRange[1],maxRange[1],0, 500))

        cv.circle(frame, (xBola, yBola), raio, (0,255,0), 2)
        # cv.line(frame,(xBola,cArea[1]),(cArea),(255,0,0),2)
        # cv.line(frame,(cArea[0],yBola),(cArea),(255,0,255),2)
        # cv.putText(frame,f"DistX: {distX} DistForX: {distFormatadaX}",(15,15),cv.FONT_HERSHEY_SIMPLEX, 0.5,(255,0,0),1,cv.LINE_AA)
        # cv.putText(frame,f"DistY: {distY} DistForY: {distFormatadaY}",(15,40),cv.FONT_HERSHEY_SIMPLEX, 0.5,(255,0,0),1,cv.LINE_AA)
        #-------------- Envia os dados para a esp --------------
        if (configuracoes["Esp-conectado"]):
            data = threading.Thread(target=ComunicacaoSerial.enviarDados("p",distFormatadaX,distFormatadaY,0))
            data.start()

    else:
        if (configuracoes["Esp-conectado"]):
            data = threading.Thread(target=ComunicacaoSerial.enviarDados("p",250,250,0))
            data.start()
  
    # cv.circle(frame, (cArea), 2,(0,255,255),3)
    # cv.drawContours(frame,[newBox],0,(255,255,255),1)
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