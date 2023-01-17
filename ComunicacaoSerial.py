import serial
import time

esp = serial.Serial('COM4', baudrate=9600)


def enviarDados(dado):
    dado = format(dado, '03d')
    esp.write(bytes(dado, "utf-8"))
    print(dado)
    time.sleep(0.01)



