#!/usr/bin/python
""" 
Description     : This program tests the correct connection and direction of the motors by performing 
                  rotational tests
Author          : CMS, JSG, DLM
Date            : July 2025
Python_version  : 3.0
Dependencies    : time, matplotlib, serial, multiprocessing
"""
#==============================================================================

from time import time, sleep
import matplotlib.pyplot as plt
import serial
from multiprocessing import Process, Value

# Create a connection with Arduino and specify the connection speed
# To find the port: dmesg | grep "tty"
try:
    arduino = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
    sleep(1.8) 
    arduino.flushInput()
    arduino.flushOutput()
except:
    print("Check the connection with Arduino")

#**********************************************************
# Function to read the speeds calculated by Arduino
#**********************************************************
def LecturaVelocidades():
    serial=[]
    rx = 0
    cadena = ",,,"
    lastcadena = ",,,"
    texto = []
    inicio=time()

    while 1:
        if terminar1.value == 0:
            cadena = str(arduino.readline())
            if cadena != "":                
                lastcadena = cadena
                texto = cadena.split(",")
                rx += 1
                if len(texto) > 0:
                    try:
                        if texto[2] == "l":
                            angularI.value = float(texto[3])

                        if texto[0] == "b'r":
                            angularD.value = float(texto[1])
                    except:
                        print("Error reading encoder data")
        else:
            sleep(0.01)
            print ("Terminating Arduino reading subprocess")
            break

#*********************************************************
# Function to send commands to Arduino
#*********************************************************
def escritura_Arduino(terminar1, PWMD1, PWMI1):
    valor = ""
    while 1:
        if terminar1.value == 0:
            valor=str(PWMD1.value) + 'D' +',' +str(PWMI1.value) + 'I'+','
            arduino.write(bytes(valor,encoding='windows-1255'))
        else:
            sleep(0.01)
            valor=str(0) + 'D' +',' +str(0) + 'I'+','
            arduino.write(bytes(valor,encoding='windows-1255'))
            print ("Terminating Arduino writing subprocess")
            break
#************************************************************************************************************************

terminar1 = Value('i', 0)
PWMI = Value('i', 0)
PWMD = Value('i', 0)
angularI = Value('f', 0.0)
angularD = Value('f', 0.0)

subproceso = Process(target=escritura_Arduino, args=(terminar1, PWMD, PWMI))
subproceso.start()
subproceso1 = Process(target=LecturaVelocidades)
subproceso1.start()

Ts = 0.0
wd_list = []
wi_list = []

time_list = []
duracion = 0
inicio = 0
j = 10
inicio = time()
antduracion = 0.0
print ("Test1-Left wheel")
milis = 0.001
mm = 1
t_experimento = 3.0	
inicio = time()
while duracion < t_experimento:
    duracion = time() - inicio
    if (duracion) >= (milis * mm):
        mm = mm + 1
        Ts = (duracion - antduracion)
        PWMD.value = 0
        PWMI.value = 40
        if j == 10:
            wd_list.append(angularD.value)
            wi_list.append(angularI.value)
            time_list.append(duracion)
        if j >= 10:
            j = 1
        else:
            j = j + 1
        antduracion = duracion   
PWMD.value = 0
PWMI.value = 0
sleep(1)

duracion = 0
inicio = 0
j = 10
inicio = time()
antduracion = 0.0
print ("Test2-Right wheel")
milis = 0.001
mm = 1
t_experimento = 3.0	
inicio = time()
while duracion < t_experimento:
    duracion = time() - inicio
    if (duracion) >= (milis * mm):
        mm = mm + 1
        Ts = (duracion - antduracion)
        PWMD.value = -40
        PWMI.value = 0
        if j == 10:
            wd_list.append(angularD.value)
            wi_list.append(angularI.value)
            time_list.append(3+duracion)
        if j >= 10:
            j = 1
        else:
            j = j + 1
        antduracion = duracion
PWMD.value = 0
PWMI.value = 0
sleep(1)

duracion = 0
inicio = 0
j = 10
inicio = time()
antduracion = 0.0
print ("Test3-Both wheels")
milis = 0.001
mm = 1
t_experimento = 3.0	
inicio = time()
while duracion < t_experimento:
    duracion = time() - inicio
    if (duracion) >= (milis * mm):
        mm = mm + 1
        Ts = (duracion - antduracion)
        PWMD.value = 40
        PWMI.value = 40
        if j == 10:
            wd_list.append(angularD.value)
            wi_list.append(angularI.value)
            time_list.append(6+duracion)
        if j >= 10:
            j = 1
        else:
            j = j + 1
        antduracion = duracion
PWMD.value = 0
PWMI.value = 0
sleep(1)

duracion = 0
inicio = 0
j = 10
inicio = time()
antduracion = 0.0
print ("Test4-Both wheels in reverse")
milis = 0.001
mm = 1
t_experimento = 3.0	
inicio = time()
while duracion < t_experimento:
    duracion = time() - inicio
    if (duracion) >= (milis * mm):
        mm = mm + 1
        Ts = (duracion - antduracion)
        PWMD.value = -40
        PWMI.value = -40
        if j == 10:
            wd_list.append(angularD.value)
            wi_list.append(angularI.value)
            time_list.append(9+duracion)
        if j >= 10:
            j = 1
        else:
            j = j + 1
        antduracion = duracion

PWMD.value = 0
PWMI.value = 0
terminar1.value = 1
valor=str(0) + 'D' +',' +str(0) + 'I'+','
arduino.write(bytes(valor,encoding='windows-1255'))

print ("Graphs")  # Inform user about graph generation

# Close the connection to Arduino
arduino.close()

# Plot the results
plt.figure(1)
plt.plot(time_list, wi_list, 'r')
plt.xlabel('[t]')
plt.ylabel('[rad/s]')
plt.title('Left angular velocity')
plt.grid(True)

plt.figure(2)
plt.plot(time_list, wd_list, 'r')
plt.xlabel('[t]')
plt.ylabel('[rad/s]')
plt.title('Right angular velocity')
plt.grid(True)

plt.show()
plt.close()

print ("End of the test")  # Inform user that the test is completed

subproceso.join()
subproceso1.join()

sleep(1)

