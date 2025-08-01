import numpy as np
import time

class PD:

    def __init__(self, k11, k22, k33):

        #Robot parameters
        self.r = 0.065
        self.l = 0.18     

        #Gains
        self.k1 = k11
        self.k2 = k22
        self.k3 = k33
        self.alpha = 1 / self.k3

        #Matrix A
        self.A = np.array([[0.0, 0.0, 0.0],
                           [0.0, 0.0, 0.0],
                           [0.0, 0.0, 0.0]])

        #Matrix B
        self.B = np.array([[0.0], [0.0], [0.0]])

        self.wdf = 0.0
        self.wif = 0.0
        self.vf = 0.0
        self.wf = 0.0

        self.sample_time = 0.00
        self.current_time = time.time()
        self.last_time = self.current_time

    def control(self, xr, yr, phir, x, y, phi, vr, wr, ephi):

        self.A = ([[self.k2 * np.cos(phi), self.k2 * np.sin(phi), 0],
                  [-self.k2 * np.sin(phi), self.k2 * np.cos(phi), self.alpha],
                  [0.0, 0.0, 1.0]])

        self.B = ([[xr - x],
                   [yr - y],
                   [phir - phi]])

        AB = np.dot(self.A, self.B)
        e1 = AB[0, 0]
        e2 = AB[1, 0]
        e3 = AB[2, 0]

        self.vf = (vr * np.cos(e3)) + (self.k1 * e1)
        self.wf = wr + (vr * self.k2 * e2) + (self.k3 * np.sin(e3))
        self.wdf = (self.vf / self.r) + ((self.l * self.wf) / self.r)
        self.wif = (self.vf / self.r) - ((self.l * self.wf) / self.r)

    def setSampleTime(self, sample_time):
        self.sample_time = sample_time


