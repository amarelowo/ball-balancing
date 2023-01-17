import cv2 as cv
import numpy as np
from config import *
import time


class circulo:

    def __init__(self, lowerRange, upperRange):
        self._upperRange = upperRange
        self._lowerRange = lowerRange
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
        # mask = cv.dilate(frameCores,None,iterations=2)
        
        #ENCONTRA CONTORNOS DA COR ESPECIFICADA
        contours, __ = cv.findContours(frame, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        for i, c in enumerate(contours):
            #epsilon = 0.01 * cv.arcLength(c, True)
            contours_poly = cv.approxPolyDP(c, 5, True)
            center, radius = cv.minEnclosingCircle(contours_poly)
            
            if radius > RAIO_MINIMO and radius < RAIO_MAXIMO:
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

    def __init__(self, lowerRange, upperRange):
        self._upperRange = upperRange
        self._lowerRange = lowerRange
        self._box = None

        self._primeiroPonto = None
        self._segundoPonto  = None
        self._terceiroPonto = None
        self._quartoPonto   = None

        self._area = 0


        self._encontrouRetangulo = False

    def seetCoord(self, frame):
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
            if aprox > AREA_MINIMA and aprox < AREA_MAXIMA:
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
        frame = self.seetCoord(frame)
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

            delta = time.time() - t
            if not self._box is None:
                if delta > 5:

                    break

            print(round(delta,2), area)    

        return self._box, self._area