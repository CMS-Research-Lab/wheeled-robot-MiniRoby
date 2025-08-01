import math

class atangente:
    def __init__(self):
        self.phid = 0.0
        self.phi = 0.0
        self.phiAnt = 0.0
        self.bandera=False

    def clear(self):
        self.phid = 0.0
        self.ephi = 0.0

    def angulo(self, ex, ey, phi):
        angulo = math.atan2(ey, ex)
        angulo=angulo%(2*math.pi)
        self.atangt=angulo
        error=self.atangt-phi        
        self.ephi=math.atan2(math.sin(error), math.cos(error))









