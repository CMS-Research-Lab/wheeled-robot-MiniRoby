#!/usr/bin/python
""" 
Title           : principal.py
Description     : Main program for trajectory tracking. It sends torque data via the serial port to Arduino, 
                  which is connected to a H-bridge. The program uses the kinematic model of a 
                  Rigid Mobile Robot (RMR) to estimate the robot's position. Arduino calculates the angular 
                  velocities of the wheels and sends them via USB to the program.
Author          : CMS, JSG, DLM
Date            : July 2025
Python_version  : 3.0
Dependencies    : matplotlib, numpy, scipy, serial, multiprocessing, RPi.GPIO
"""
#==============================================================================
import PD
import atan3
from time import time, sleep
import matplotlib.pyplot as plt
import trajectory
import serial
import scipy as sp
import numpy as np
from multiprocessing import Process, Value
import RPi.GPIO as GPIO

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)

# GPIO for the emergency stop button
paro = 17

# Assign the emergency stop button to the GPIO pin
GPIO.setup(paro,GPIO.IN)

# Sampling time
Ts = 0.001

# Create a connection with Arduino, specify connection speed
# Find the port: dmesg | grep "tty"
try:
    arduino = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)    
    sleep(1.8) 
    arduino.flushInput()
    arduino.flushOutput()
except:
    print("Check the connection with Arduino")

# Kinematic control
pd = PD.PD(5.0, 1.0, 5.0)
kpd = 0.6
kid = 0.1
kpi = 0.6
kii = 0.1

atan = atan3.atangente()

#*******************
# RMR parameters
# MiniRoby
#*******************
r = 0.0325 #Wheel radius
l = 0.09 #track width

# RMR arrays
x_list = []
y_list = []
phi_list = []
w = []
wd_list = []
wi_list = []
v_list = []

xd_list = []
yd_list = []

i = 0

# Initial conditions of the RMR
x = 0.67
y = 0.0
phi = 0.0

# Initialize variables
time_list = []
PWM_der = 0
PWM_izq = 0
wdr = 0.0
wir = 0.0
phir_list = []
vr_list = []
wr_list = []
v_list = []

# PI control variables
ed = 0.0
ei = 0.0
ud = 0.0
ui = 0.0
iei = 0.0
ied = 0.0

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
            print ("Arduino reading subprocess terminated")
            break

#*********************************************************
# Write to Arduino                                      *
#*********************************************************
def escritura_Arduino(terminar1, PWMD1, PWMI1):
    last = 0
    valor = ""
    while 1:
        if terminar1.value == 0:
            if PWMD1.value != last or PWMI1.value != last:                
                valor=str(PWMD1.value) + 'D' +',' +str(PWMI1.value) + 'I'+','
                arduino.write(bytes(valor,encoding='windows-1255'))
        else:
            sleep(0.01)
            valor=str(0) + 'D' +',' +str(0) + 'I'+','
            arduino.write(bytes(valor,encoding='windows-1255'))
            print ("Arduino writing subprocess terminated")
            break
#************************************************************************************************************************

terminar1 = Value('i', 0)
PWMI = Value('i', 0)
PWMD = Value('i', 0)
angularI = Value('f', 0.0)
angularD = Value('f', 0.0)

# Start subprocess for writing commands to Arduino
subproceso = Process(target=escritura_Arduino, args=(terminar1, PWMD, PWMI))
subproceso.start()

# Start subprocess for reading wheel speeds from Arduino
subproceso1 = Process(target=LecturaVelocidades)
subproceso1.start()

# Initialize test parameters
duracion = 0
duracion2 = []
inicio = 0
tauD = 0
tauI = 0

#ERRORES
errorX_list = []
errorY_list = []
ephi_list = []

phir=0.0
phir_list2=[]
path = trajectory.trayectoria()

j = 10
k = 0
inicio = time()
pulsos_list = []
xp_list = []
yp_list = []
ud_list = []
ui_list = []

q = 0
antduracion = 0.0
print ("Start of the experiment")

#tiempo de muestreo en segundos
milis = 0.001
mm = 1
t_experimento = 15.0	
inicio = time()

while duracion < t_experimento:
    duracion = time() - inicio
    if (duracion) >= (milis * mm):
        mm = mm + 1
        duracion2.append(duracion)
        Ts = (duracion - antduracion)

        #This emergency stop is not implemented yet, but it is designed to wirelessly stop the robot.
        if GPIO.input(paro) == 1:
            q = q + 1
            if 500 < q:
                print ("STOPPED BY THE USER")
                break

        path.generacionXY(duracion)
        xd = path.Xd
        yd = path.Yd
        vr = path.Vl
        wr = path.Wl
        
        # Calculate phi*
        atan.angulo(xd - x, yd - y, phi)
        phir = atan.atangt
        phir_list.append(phir)

        # Calculate phi error
        ephi = atan.ephi
        wir = angularI.value
        wdr = angularD.value

        # Control signal calculation
        pd.control(xd, yd, phir, x, y, phi, vr, wr, ephi)

        # Calculate angular velocity errors
        ed = (pd.wdf - wdr)
        ei = (pd.wif - wir)

        # PI Controls
        ied = ied + (ed * Ts)
        ud = (kpd * ed) + (kid * ied)
        iei = iei + (ei * Ts)
        ui = (kpi * ei) + (kii * iei)

        # Limit voltages to 11 volts
        if ud > 11.0:
            ud = 11
        elif ud < -11.0:
            ud = -11.0
        if ui > 11.0:
            ui = 11.0
        elif ui < -11.0:
            ui = -11.0

        # Convert control signal to PWM
        PWM_der = ud / 11.0
        PWM_izq = ui / 11.0

        PWMD.value = int(round(PWM_der, 2) * 100)
        PWMI.value = int(round(PWM_izq, 2) * 100)
        ui_list.append(PWMI.value)
        ud_list.append(PWMD.value)

        # Real RMR kinematic model
        x = x + ((((wdr + wir) * r) / 2) * sp.cos(phi)) * (0.001)
        y = y + ((((wdr + wir) * r) / 2) * sp.sin(phi)) * (0.001)
        phi = phi + ((((wdr - wir) * r) / (2 * l))) * (0.001)

        # Virtual RMR         
        phir = phir + ((((pd.wdf - pd.wif) * r) / (2 * l))) * (0.001)

        #Store variables every 0.1 second
        #this is only for the graphs; the calculations are performed every millisecond.
        if j == 10:
            # Errors
            errorX_list.append(xd - x)
            errorY_list.append(yd - y)
            ephi_list.append(ephi)

            # Voltages
            ud_list.append(PWMD.value)
            ui_list.append(PWMI.value)

            # Store robot variables
            x_list.append(x)
            y_list.append(y)
            phi_list.append(phi)
            wd_list.append(wdr)
            wi_list.append(wir)
            v_list.append(((wdr + wir) * r) / 2)
            w.append((r / (2 * l)) * (wdr - wir))

            #Reference RMR
            xd_list.append(xd)
            yd_list.append(yd)
            phir_list2.append(phir)	
            vr_list.append(path.Vl)
            wr_list.append(wr)

            time_list.append(duracion)
        if j >= 10:
            j = 1
        else:
            j = j + 1

        k = k + 1
        antduracion = duracion

PWMD.value = 0
PWMI.value = 0
terminar1.value = 1
valor=str(0) + 'D' +',' +str(0) + 'I'+','
arduino.write(bytes(valor,encoding='windows-1255'))

print ("End of the Experiment")

# Close the connection to Arduino
arduino.close()

#************************************************
# Plotting section
#************************************************
# 1. XY Trajectory
plt.subplot(3, 2, 1)
plt.plot(x_list, y_list, 'r', label='Actual Path', linewidth=2)
plt.plot(xd_list, yd_list, '--b', label='Desired Path', linewidth=1.5)
plt.plot(xd_list[-1], yd_list[-1], 'bo', markersize=8, label='Desired Finish')
plt.plot(xd_list[1], yd_list[1], 'bs', markersize=8, label='Desired Start')
plt.plot(x_list[-1], y_list[-1], 'ro', markersize=6, label='Actual Finish')
plt.plot(x_list[1], y_list[1], 'rs', markersize=6, label='Actual Start')
plt.xlabel('X [m]', fontsize=12)
plt.ylabel('Y [m]', fontsize=12)
plt.title('XY Trajectory of WMR', fontsize=14)
plt.legend(loc='upper right')
plt.grid(True)
plt.axis('equal')

# 2. Orientation Angle
plt.subplot(3, 2, 2)
angulo=np.unwrap(phi_list)
plt.plot(time_list, ((angulo)), 'r', label='Actual Angle')
plt.plot(time_list, np.unwrap((phir_list2), 'b--', label='Desired Angle')
plt.xlabel('T[s]', fontsize=12)
plt.ylabel('[rad]', fontsize=12)
plt.title('Orientation Angle', fontsize=14)
plt.legend()
plt.grid(True)

# 3. Linear Velocity
plt.subplot(3, 2, 3)
plt.plot(time_list, v_list, 'r', label='Actual')
plt.plot(time_list, vr_list, 'b--', label='Desired')
plt.xlabel('T[s]', fontsize=12)
plt.ylabel('[m/s]', fontsize=12)
plt.title('Linear Velocity', fontsize=14)
plt.legend()
plt.grid(True)

# Right Angular Velocity plot
plt.subplot(3, 2, 4)
plt.plot(time_list, w, 'r', label='Actual')
plt.plot(time_list, wr_list, 'b--', label='Desired')
plt.xlabel('T[s]', fontsize=12)
plt.ylabel('[rad/s]', fontsize=12)
plt.title('Angular Velocity')
plt.legend()
plt.grid(True)

# Left Angular Velocity
plt.subplot(3, 2, 5)
plt.plot(time_list, wi_list, 'r', label='Actual')
plt.xlabel('[s]', fontsize=12)
plt.ylabel('[rad/s]', fontsize=12)
plt.title('Left Wheel Angular Velocity', fontsize=14)
plt.legend()
plt.grid(True)

# Right Angular Velocity
plt.subplot(3, 2, 6)
plt.plot(time_list, wd_list, 'r', label='Actual')
plt.xlabel('T[s]', fontsize=12)
plt.ylabel('[rad/s]', fontsize=12)
plt.title('Right Wheel Angular Velocity', fontsize=14)
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig('graph.png', dpi=300, bbox_inches='tight')
plt.show()

#*************************************************
# Save data to files
#*************************************************
fichero = open('xlist.txt', 'w')
fichero.write(str(x_list))
fichero.close()

fichero = open('ylist.txt', 'w')
fichero.write(str(y_list))
fichero.close()

fichero = open('tlist.txt', 'w')
fichero.write(str(time_list))
fichero.close()

fichero = open('xdlist.txt', 'w')
fichero.write(str(xd_list))
fichero.close()

fichero = open('ydlist.txt', 'w')
fichero.write(str(yd_list))
fichero.close()

fichero = open('philist.txt', 'w')
fichero.write(str(phi_list))
fichero.close()

fichero = open('phid_list.txt', 'w')
fichero.write(str(phir_list2))
fichero.close()

fichero = open('wdlist.txt', 'w')
fichero.write(str(wd_list))
fichero.close()

fichero = open('wilist.txt', 'w')
fichero.write(str(wi_list))
fichero.close()

fichero = open('v_list.txt', 'w')
fichero.write(str(v_list))
fichero.close()

fichero = open('vr_list.txt', 'w')
fichero.write(str(vr_list))
fichero.close()

fichero = open('w.txt', 'w')
fichero.write(str(w))
fichero.close()

fichero = open('wr_list.txt', 'w')
fichero.write(str(wr_list))
fichero.close()

# Finalize processes
subproceso.join()
subproceso1.join()

sleep(1)
GPIO.cleanup()
