import numpy as np
from const import *
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

class Mixer(function):
    def __init__(self, oscs:list[function]):
        super().__init__()
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