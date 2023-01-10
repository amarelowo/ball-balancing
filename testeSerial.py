import serial
import time

esp = serial.Serial('COM4', baudrate=9600)


while(True):
    dado = input("Digite l ou d, o para encerrar: ")
    if(dado == 'l' or dado == 'd'):
        esp.write(bytes(dado, "utf-8"))
        print(dado)
    else:
        break


# for i in range(1,100):
#     print(i)
#     esp.write(bytes(i))
#     time.sleep(1)