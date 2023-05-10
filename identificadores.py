import cv2 as cv
import numpy as np
from config import *
import pid
import time


class circulo:

    def __init__(self, colorRange):
        self._upperRange = colorRange[1]
        self._lowerRange = colorRange[0]
        self._xCoord = None
        self._yCoord = None
        self._radius = None
        self._encontrou = False

    def setCoord(self, frame):
        '''Encontra o circulo através das cores especificadas
        '''
        
        #APLICAR FILTROS
        frame = cv.medianBlur(frame, 3)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        frame = cv.inRange(frame, self._lowerRange, self._upperRange)

        
        # mask = cv.erode(frameCores, None, iterations=2)
        # mask = cv.dilate(frameCores,None, iterations=2)
        
        #ENCONTRA CONTORNOS DA COR ESPECIFICADA
        contours, __ = cv.findContours(frame, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        for i, c in enumerate(contours):
            #epsilon = 0.01 * cv.arcLength(c, True)
            contours_poly = cv.approxPolyDP(c, 5, True)
            center, radius = cv.minEnclosingCircle(contours_poly)
            
            if radius > FORMATOS["RAIO-MINIMO"] and radius < FORMATOS["RAIO-MAXIMO"]:
                #print(center, int(radius))
                self._xCoord = int(center[0])
                self._yCoord = int(center[1])
                self._radius = int(radius)
                return
            
        
        self._xCoord = None
        self._yCoord = None
        self._radius = None

    def coordenadas(self, frame):
        self.setCoord(frame)
        return self._xCoord, self._yCoord, self._radius


    def encontrouCirculo(self):
        '''Verifica se o circulo foi encontrado
        '''
        if self._xCoord != None and self._yCoord != None:
            self._encontrou = True

        else:
            self._encontrou = False

        return self._encontrou            

class retangulo:

    def __init__(self, colorRange):
        self._upperRange = colorRange[1]
        self._lowerRange = colorRange[0]
        self._box = None

        self._primeiroPonto = None
        self._segundoPonto  = None
        self._terceiroPonto = None
        self._quartoPonto   = None

        self._area = 0
        self._centroArea = None
        self._maxRangeX = None
        self._maxRangeY = None


        self._encontrouRetangulo = False

    def setCoord(self, frame):
        #APLICAR FILTROS
        frame = cv.medianBlur(frame, 3)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        frame = cv.inRange(frame, self._lowerRange, self._upperRange)

        
        # frame = cv.erode(frame, None, iterations=2)
        # frame = cv.dilate(frame,None,iterations=2)

        contornos, __ = cv.findContours(frame, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

        #PERCORRE OS CONTORNOS IDENTIFICADOS ATÉ ENCONTRAR O RETANGULO
        for contorno in contornos:
            aprox = cv.contourArea(contorno)
            if aprox > FORMATOS["AREA-MINIMA"] and aprox < FORMATOS["AREA-MAXIMA"]:
                retg = cv.minAreaRect(contorno)
                box = cv.boxPoints(retg)
                box = np.int0(box)

                #atribui os pontos do retangulo
                self._box = box
                self._primeiroPonto = box[0]
                self._segundoPonto = box[1]
                self._terceiroPonto = box[2]
                self._quartoPonto = box[3]

                self._area = aprox

                return

    def coordenadas(self, frame):
        frame = self.setCoord(frame)
        return self._box

    def encontrouRetangulo(self):
        if not self._box is None:
            self._encontrouRetangulo = True   
        else:
            self._encontrouRetangulo = False

        return self._encontrouRetangulo

    def areaRetangulo(self):
        return self._area      

    def encontrarPlataforma(self, cam):        
        
        t = time.time()
        while True:
            __, frame = cam.read()
            
            if frame is None:
                print("Erro ao ler a webcam, tente novamente")
                break
            
            box = self.coordenadas(frame)
            area = self.areaRetangulo()

            if self.encontrouRetangulo():
                if area > self._area:
                    self._area = area
                    self._box = box
                    break

            delta = time.time() - t
            
            if delta > 3:
                break

            print(round(delta,2), area)    

        if not self._box is None:
            self._centroArea = pid.centroReta(self._box[0],self._box[2])
            self._maxRangeX = self._centroArea[0] - box[0][0]  
            if self._maxRangeX < 0:
                self._maxRangeX = self._maxRangeX*(-1)
            self._maxRangeY = self._centroArea[1] - box[0][1]  
            if self._maxRangeY < 0:
                self._maxRangeY = self._maxRangeY*(-1)    

        print(self._centroArea,(self._maxRangeX,self._maxRangeY))
        
        return self._box, (self._maxRangeX, self._maxRangeY), self._centroArea, self._area
    




def selecBox(capture):
    __, frame = capture.read()
    x1,y1,w,h = cv.selectROI("Selecione a plataforma", frame)
    print(x1,y1,w,h)
    
    p1 = (x1,y1)
    p2 = (x1+w, y1)
    p3 = (x1+w,y1+h)
    p4 = (x1, y1+h)
    box = (p1,p2,p3,p4)
    box = np.int0(box)
    print(box)

    newBox = [(0,0),(w,0),(w,h),(0,h)]
    newBox = np.int0(newBox)
    
    centroArea = pid.centroReta(newBox[0],newBox[2])
    maxRangeX = centroArea[0] - newBox[0][0]  
    if maxRangeX < 0:
        maxRangeX = maxRangeX*(-1)
    maxRangeY = centroArea[1] - newBox[0][1]  
    if maxRangeY < 0:
        maxRangeY = maxRangeY*(-1)  
    return box,newBox,(maxRangeX,maxRangeY),centroArea