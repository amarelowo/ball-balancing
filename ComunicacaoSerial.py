import serial
import time
from pid import *
esp = serial.Serial('COM4', baudrate=115200,timeout=.1)


def enviarDados(dado):

    if dado > 1000:
        dado = 1000
    elif dado < 0:
        dado = 0

    dado = format(dado, '04d')
    esp.write(bytes(dado,"utf-8"))
    retorno = esp.readline()
    print(dado,retorno )
    
    ##parte que ta funcionando mas só leva um caractere
    # if dado > 90:
    #     sla = "l"
    # else:
    #     sla = "d"
    # esp.write(bytes(sla, "utf-8"))
    # print(type(sla), sla)
    
    time.sleep(0.01)
# slamane = 0
# while slamane != -1:
#     slamane = int(input("escreve ai: "))
#     dado = format(slamane, '03d')
#     esp.write(bytes(dado,"utf-8"))
#     print(slamane)

