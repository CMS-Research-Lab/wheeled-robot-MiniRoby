#==============================================================================
#description     :Trajectory generator
#author          :CMS
#python_version  :3
#dependencies    : numpy, math
#==============================================================================
import numpy as np
import math

class trayectoria:

    def __init__(self):
        self.path = 0.0
        self.ti = 0.0
        self.tf = 0.0
        self.xr = 0.0
        self.yr = 0.0
        self.xpr = 0.0
        self.ypr = 0.0
        self.t = 0.0
        self.phir = 0.0
        self.Xd = 0.7
        self.Yd = 0.1

        self.r1 = 10.0
        self.r2 = 15.0
        self.r3 = 6.0

        self.Vl = 0.0
        self.Wl = 0.0

        self.clear()

    def clear(self):
        self.SetPoint = 0.0
        self.PTerm = 0.0
        self.ITerm = 0.0
        self.DTerm = 0.0
        self.last_error = 0.0
        self.int_error = 0.0
        self.windup_guard = 24.0
        self.path = 0.0

    def generacionXY(self, t):
        if (t >= 0) and (t <44):
            #***********************************
            #Linear trajectory            
            #***********************************
            #vr = 0.15
            #wr = 0.0

            #***********************************
            #Circular trajectory
            #***********************************
            #vr = 0.25
            #wr = 0.5
            
            #***********************************
            #Sinusoidal trajectory            
            #v: linear velocity (m/s)
            #A: amplitude of the wave (m)
            #f: frequency (Hz)
            #***********************************
            
            v = 0.05
            A = 1.5
            frecuencia = 0.1
            omega = 2 * np.pi * frecuencia
            dx= v
            dy= A*omega*np.cos(omega*t)
            vr= np.sqrt(dx**2+dy**2)
            theta= math.atan2(dy,dx)
            dy_prev= A*omega*np.cos(omega*(t-0.001))
            theta_prev= math.atan2(dy_prev,dx)
            wr= (theta-theta_prev)/0.001
            wr=A*omega*np.cos(omega*t)
            vr=0.18
            
        else:
            vr = 0.0
            wr = 0.0

        self.phir = self.phir + wr * 0.001
        self.xrp = vr * np.cos(self.phir)
        self.yrp = vr * np.sin(self.phir)
        self.Xd = self.Xd + self.xrp * 0.001
        self.Yd = self.Yd + self.yrp * 0.001
        self.Vl = vr
        self.Wl = wr