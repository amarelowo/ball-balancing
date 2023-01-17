import time

def centroReta(p1,p2):
    return ((p1[0]+p2[0])//2,(p1[1]+p2[1])//2)

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min)*(out_max - out_min)/(in_max - in_min) + out_min



class pid:

    def __init__(self, kP, kI, kD, setPoint):
        
        self._kP = kP
        self._kI = kI
        self._kD = kD
        self._setPoint = setPoint
        self._lastProcess = 0
        self._lastSample = 0
        self._i = 0
        
        pass


    def process(self, sample):

        #Implementação PID
        erro = self._setPoint - sample

        deltaT = time.monotonic() - self._lastProcess
        self._lastProcess = time.monotonic()
        

        # P
        p = erro * self._kP

        # I
        self._i += erro * self._kI * deltaT

        # D
        d = (self._lastSample - sample) * self._kD * deltaT
        self._lastSample = sample
        

        # Soma tudo
        pid = p + self._i + d

        return pid