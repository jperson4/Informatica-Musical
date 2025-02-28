import numpy as np
from synt.const import *
from synt.function import *
from math import sqrt

def mix(ondas:list[list]):
    n = len(ondas)
    ret = np.zeros(CHUNK)
    if n == 0:
        return ret
    
    fact = 1/sqrt(n)
    for o in ondas:
        ret = ret + (o * fact)
    return ret

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
        return self.mix(tiempo)
    
    def sqr(self, tiempo):  
        n = len(self.oscs)  
        ret = np.zeros(CHUNK)
        if n == 0:          
            return ret      
        fact = 1/sqrt(n)        
        for o in self.oscs: 
            ret = ret + (o.next(tiempo) * fact)
        return ret
    
    def media(self, tiempo):  
        n = len(self.oscs)  
        ret = np.zeros(CHUNK)
        if n == 0:          
            return ret      
        fact = 1/n        
        for o in self.oscs: 
            ret = ret + (o.next(tiempo) * fact)
        return ret
    
    def tanh(self, tiempo):
        ret = np.zeros(CHUNK)
        for o in self.oscs: 
            ret = ret + o.next(tiempo)
        return np.tanh(ret)        