import numpy as np
from synt.const import *
from synt.function import *
from math import sqrt

def sqr(oscs, tiempo):  
    n = len(oscs)  
    ret = np.zeros(CHUNK)
    if n == 0:          
        return ret      
    fact = 1/sqrt(n)        
    for o in oscs: 
        ret = ret + (o.next(tiempo) * fact)
    return ret

def media(oscs, tiempo):  
    n = len(oscs)  
    ret = np.zeros(CHUNK)
    if n == 0:          
        return ret      
    fact = 1/n        
    for o in oscs: 
        ret = ret + (o.next(tiempo) * fact)
    return ret

def tanh(oscs, tiempo):
    ret = np.zeros(CHUNK)
    for o in oscs: 
        ret = ret + o.next(tiempo)
    return np.tanh(ret)    

class Mixer(Function):
    def __init__(self, oscs:list[Function], fun=None):
        super().__init__()
        self.oscs = oscs
        self.mix = fun
        if fun == None:
            self.mix = sqrt
        
    def setOscs(self, oscs):
        self.oscs = oscs
        
    def fun(self, tiempo):
        return self.mix(self.oscs, tiempo)
    
    def doShow(self, tk, bg="#808090"):
        _tk = super().doShow(tk, bg)
        for o in range (0, len(self.oscs)):
            self.oscs[o].addNombre(str(o))
            self.oscs[o].doShow(_tk, bg, side=BOTTOM)
        return _tk
