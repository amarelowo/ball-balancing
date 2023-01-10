import cv2 as cv

RAIO_MAXIMO = 100
RAIO_MINIMO = 250

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
        frame = cv.medianBlur(frame, 5)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        frameCores = cv.inRange(frame, self._lowerRange, self._upperRange)

        #ENCONTRA CONTORNOS DA COR ESPECIFICADA
        contours, __ = cv.findContours(frameCores, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        for i, c in enumerate(contours):
            contours_poly = cv.approxPolyDP(c, 3, True)
            center, radius = cv.minEnclosingCircle(contours_poly)

            if radius > RAIO_MINIMO and radius < RAIO_MAXIMO:
                self._xCoord = int(center[0])
                self._yCoord = int(center[1])
                self._radius = int(radius)

            else:
                self._xCoord = None
                self._yCoord = None
                self._radius = None

        return self._xCoord, self._yCoord, self._radius
        
    def encontrouCirculo(self):
        '''Verifica se o circulo foi encontrado
        '''
        if self._xCoord != None and self._yCoord != None:
            self._encontrou = True

        else:
            self._encontrou = False

        return self._encontrou            