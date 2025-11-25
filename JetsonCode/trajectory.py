Re#==============================================================================
Re#==============================================================================
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
        if (t >= 0):
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
            
            #***********************************
            #Complex trajectory
            #***********************************
            '''vr=0
            wr=0

            r1=10
            r2=15
            r3=6

            if (t>=0)and(t<1):
                ti=0
                tf=1
                vtf=0.095    
                vti=0
                wtf=0.35   
                wti=0
                a=(t-ti)/(tf-ti)
                vr=(a**3)*(r1-r2*a+r3*a**2)*(vtf-vti)+vti
                wr=(a**3)*(r1-r2*a+r3*a**2)*(wtf-wti)+wti
            elif (t>=1)and(t<5):
                vr=0.095
                wr=0.35
            elif (t>=5)and(t<6):
                ti=5       
                tf=6
                wtf=-0.35
                wti=0.35
                vtf=0.08
                vti=0.095
                a=(t-ti)/(tf-ti)
                vr=(a**3)*(r1-r2*a+r3*a**2)*(vtf-vti)+vti
                wr=(a**3)*(r1-r2*a+r3*a**2)*(wtf-wti)+wti
            elif (t>=6)and(t<10):
                vr=0.08
                wr=-0.35
            elif (t>=10)and(t<11):
                ti=10       
                tf=11
                wtf=0.25      
                wti=-0.35
                vtf=0.075    
                vti=0.08
                a=(t-ti)/(tf-ti)
                vr=(a**3)*(r1-r2*a+r3*a**2)*(vtf-vti)+vti
                wr=(a**3)*(r1-r2*a+r3*a**2)*(wtf-wti)+wti
            elif (t>=11)and(t<23):
                vr=0.075
                wr=0.25 
            elif (t>=23)and(t<24):
                ti=23       
                tf=24 
                wtf=-0.35      
                wti=0.25
                vtf=0.08    
                vti=0.075
                a=(t-ti)/(tf-ti)
                vr=(a**3)*(r1-r2*a+r3*a**2)*(vtf-vti)+vti
                wr=(a**3)*(r1-r2*a+r3*a**2)*(wtf-wti)+wti
            elif (t>=24)and(t<28):
                vr=0.08
                wr=-0.35
            elif (t>=28)and(t<30):
                ti=28       
                tf=30 
                wtf=0.35      
                wti=-0.35  
                vtf=0.095    
                vti=0.08
                a=(t-ti)/(tf-ti)
                vr=(a**3)*(r1-r2*a+r3*a**2)*(vtf-vti)+vti
                wr=(a**3)*(r1-r2*a+r3*a**2)*(wtf-wti)+wti
            elif (t>=30)and(t<38):
                vr=0.095
                wr=0.35
            elif (t>=38)and(t<40):
                ti=38       
                tf=40
                wtf=-0.3      
                wti=0.35  
                vtf=0.08    
                vti=0.095
                a=(t-ti)/(tf-ti)
                vr=(a**3)*(r1-r2*a+r3*a**2)*(vtf-vti)+vti
                wr=(a**3)*(r1-r2*a+r3*a**2)*(wtf-wti)+wti
            elif (t>=40)and(t<44):
                vr=0.08
                wr=-0.3
                print("t",t)
            elif (t>=44)and(t<45):
                print("t",t)
                ti=44       
                tf=45
                wtf=0.25     
                wti=-0.3  
                vtf=0.075    
                vti=0.08
                a=(t-ti)/(tf-ti)
                vr=(a**3)*(r1-r2*a+r3*a**2)*(vtf-vti)+vti
                wr=(a**3)*(r1-r2*a+r3*a**2)*(wtf-wti)+wti
            elif (t>=45)and(t<56):
                vr=0.075
                wr=0.25
            elif (t>=56)and(t<58):
                ti=56       
                tf=58 
                wtf=-0.3      
                wti=0.25  
                vtf=0.08    
                vti=0.075
                a=(t-ti)/(tf-ti)
                vr=(a**3)*(r1-r2*a+r3*a**2)*(vtf-vti)+vti
                wr=(a**3)*(r1-r2*a+r3*a**2)*(wtf-wti)+wti
            elif (t>=58)and(t<62):
                vr=0.08
                wr=-0.3
            elif (t>=62)and(t<64):
                ti=62       
                tf=64
                wtf=0.36      
                wti=-0.3
                vtf=0.088    
                vti=0.08
                a=(t-ti)/(tf-ti)
                vr=(a**3)*(r1-r2*a+r3*a**2)*(vtf-vti)+vti
                wr=(a**3)*(r1-r2*a+r3*a**2)*(wtf-wti)+wti
            elif(t>=64)and(t<67):
                vr=0.088
                wr=0.36
            elif (t>=67)and(t<69):
                ti=67       
                tf=69 
                wtf=0      
                wti=0.36  
                vtf=0    
                vti=0.088
                a=(t-ti)/(tf-ti)
                vr=(a**3)*(r1-r2*a+r3*a**2)*(vtf-vti)+vti
                wr=(a**3)*(r1-r2*a+r3*a**2)*(wtf-wti)+wti  
            else:
                vr=0.0
                wr=0.0'''       
            
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
