import serial
import time

esp = serial.Serial('COM4', baudrate=115200,timeout=.1)


def enviarDados(dado):

    ##parte que ainda nao funcionou
    dado = format(dado, '03d')
    esp.write(bytes(dado,"utf-8"))
    
    ##parte que ta funcionando mas só leva um caractere
    # if dado > 90:
    #     sla = "l"
    # else:
    #     sla = "d"
    # esp.write(bytes(sla, "utf-8"))
    # print(type(sla), sla)
    
    time.sleep(0.01)



