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
    def __init__(self, oscs:list[Function]):
        super().__init__()
        self.oscs = oscs
        
    def setOscs(self, oscs):
        self.oscs = oscs
        
    def fun(self, tiempo):
            n = len(self.oscs)
            ret = np.zeros(CHUNK)
            if n == 0:
                return ret
            
            fact = 1/sqrt(n)
            for o in self.oscs:
                ret = ret + (o.next(tiempo) * fact)
            return ret
