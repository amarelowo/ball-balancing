import serial
import time
from pid import *
esp = serial.Serial('COM4', baudrate=115200,timeout=.1)


def enviarDados(verficador, dado1, dado2, dado3):

    if verficador == "c":
        dado = verficador+";"+ format(dado1, '05')+";"+ format(dado2, '05')+";"+ format(dado3, '05')
        
    if verficador == "p":
        dado = verficador+";"+ format(dado1, '05d')+";"+ format(dado2, '05d')+";"+ format(dado3, '05d')
        if type(dado1) is int:
            if dado1 > 1000:
                dado1 = 1000
            elif dado1 < 0:
                dado1 = 0


    esp.write(bytes(dado,"utf-8"))
    retorno = esp.readline()
    print(dado,retorno)
    time.sleep(0.01)

    




## Codigo para testar o angulo do servo

# slamane = 0
# while slamane != -1:
#     slamane = int(input("escreve ai: "))
#     dado = format(slamane, '03d')
#     esp.write(bytes(dado,"utf-8"))
#     print(slamane)

