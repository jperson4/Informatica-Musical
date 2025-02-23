import numpy as np
from synt.const import *
from synt.function import *
from synt.envolv import *

import synt.osc as osc

class Synt:
    def __init__(self, freq, onda, amp=Const(1), phase=Const(0), env=NoEnv()):
        self.freq = freq
        self.amp = amp
        self.phase = phase
        self.onda = onda
        self.frame = 0
        self.env = env
        
    def setAmp(self, amp):
        self.amp = amp
        
    def setOsc(self, onda):
        self.onda = onda
        
    def setPhase(self, phase):
        self.phase = phase
        
    def getPhase(self):
        return self.phase
    
    def getEnv(self):
        return self.env
    
    # tambien se puede usar como un oscilador
    def next(self, tiempo=None):
        if tiempo is None:
            tiempo = np.arange(self.frame, CHUNK + self.frame, 1) # array con el tiempo
        self.frame += CHUNK
        # print (self.onda)
        return self.onda.next(self.freq, tiempo, self.amp, self.phase) * self.env.next(tiempo)


class PolySynt:
    def __init__(self, freqs, ondas, amp=C(1), amps=[Const(1)], phases=[Const(0)], env=NoEnv()):
        n = len(freqs)
        while len(ondas) < n:
            ondas.append(ondas[0])
        while len(amps) < n:
            amps.append(amps[0])
        while len(phases) < n:
            phases.append(phases[0])
        self.n = n
        self.freqs = freqs
        self.amps = amps
        self.phases = phases  
        self.ondas = ondas
        self.frame = 0
        self.env = env
        self.amp = amp
        
    # def setAmps(self, amps):
        # self.amps = amps
        
    # def setOscs(self, ondas):
        # self.ondas = ondas
        
    # def setPhases(self, phases):
        # self.phases = phases
        
    # def getPhases(self):
        # return self.phases
        
    def next(self, tiempo=None):
        if tiempo is None:
            tiempo = np.arange(self.frame, CHUNK + self.frame, 1)
        self.frame += CHUNK
                
        res = np.zeros(CHUNK)
        _env = self.env.next(tiempo)
        for i in range(self.n):
            res = res + self.ondas[i].next(self.freqs[i], tiempo, self.amps[i] / C(len(self.freqs)), self.phases[i]) * _env
            
        
            
        return res * self.amp.next(tiempo) 
    
    def getEnv(self):
        return self.env
        
class HarmSynt(PolySynt):
    def __init__(self, nota, ondas, amp=C(1), amps=[Const(1)], phases=[Const(0)], env=NoEnv(), afinacion=notasAJ):
        
        _freqs = diatonicAcorde(nota, afinacion)
        freqs = []
        for f in _freqs:
            freqs.append(C(f))
        print(_freqs)
          
        super().__init__(freqs, ondas, amp, amps, phases, env)
