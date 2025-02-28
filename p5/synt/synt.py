import numpy as np
from synt.const import *
from synt.function import *
from synt.envolv import *
from synt.mixer import *

from synt.osc import *

import math

class Synt(Osc):
    '''Los synt son un oscilador que emplea otro oscilador para formar la onda puede estar sujeto a una envolvente'''
    def __init__(self, freq:Function, onda:Osc, amp=Const(1), phase=Const(0), env=NoEnv):
        super().__init__(freq, None, None, amp, phase)
        self.onda = onda

        self.onda.setFreq(freq)
        self.onda.setAmp(amp)
        self.onda.setPhase(phase)
        self.env = env
    
    def mix(self, tiempo):
        return self.onda.next(tiempo) * self.env.next(tiempo)

    def setFreq(self, value):
        self.freq = value
        self.onda.setFreq(value)

    def setAmp(self, value):
        self.amp = value
        self.onda.setAmp(value)

    def setPhase(self, value):
        self.phase = value
        self.onda.setPhase(value)
        
    def getEnv(self):
        return self.env
    
    def setEnv(self, env):
        self.env = env

# TODO añadir un mixer
class PolySynt(Osc):
    def __init__(self, freqs:list[Function], ondas:list[Osc], amp=C(1), amps=[Const(1)], phases=[Const(0)], envs=[NoEnv()]):
        
        # esto lo pongo por poner pero en verdad no estan implementadas las funciones de la clase osc
        super().__init__(freqs[0], None, None, amp, phases[0])
        # ajsutar que todo tenga el mismo numero de elementos
        n = len(freqs)
        while len(ondas) < n:
            ondas.append(ondas[0])
        while len(amps) < n:
            amps.append(amps[0])
        while len(phases) < n:
            phases.append(phases[0])
        while len(envs) < n:
            envs.append(envs[0])
        
        self.n = n
        
        self.synts = []
        # usamos una lista de sintetizadores
        for i in range(0, n):
            self.synts.append(Synt(freqs[i], ondas[i], amps[i], phases[i], envs[i]))
            # = Synt(freqs[i], ondas[i], amps[i], phases[i], envs[i])
        
        # guardamos para poder devolverlas si se piden
        self.freqs = freqs
        self.amps = amps
        self.phases = phases  
        self.ondas = ondas
        self.frame = 0
        self.envs = envs
        self.amp = amp
        self.mixer = Mixer(self.synts)
        


    def mix(self, tiempo):
        onda = np.zeros(CHUNK)     
        fact = 1 / math.sqrt(len (self.synts))
        for s in self.synts:
            onda = onda + (s.next(tiempo) * fact)
        # onda = self.mixer.next(tiempo)
        return onda * self.amp.next(tiempo)

    def setAmps(self, amps):
        for i in range(0, self.n):
            self.synts[i].setAmp(amps[i])
        self.amps = amps

    def setPhases(self, phases):
        for i in range(0, self.n):
            self.synts[i].setPhase(phases[i])
        self.phases = phases

    def setFreqs(self, freqs):
        for i in range(0, self.n):
            self.synts[i].setFreq(freqs[i])
        self.freqs = freqs
        
    def getPhases(self):
        return self.phases
        
    def setAmp(self, val, i):
        self.synts[i].setAmp(val)
        
    def setFreq(self, val, i):
        self.synts[i].setFreq(val)
        
    def setPhase(self, val, i):
        self.synts[i].setPhase(val)

    def getAmp(self, i):
        return self.synts[i].amp

    def getFreq(self, i):
        return self.synts[i].freq

    def getPhase(self, i):
        return self.synts[i].phase
        
#TODO: hacerlo nuevo
class HarmSynt(PolySynt):
    def __init__(self, freq:Function, muls:Function, ondas, amp=C(1), amps=[Const(1)], phases=[Const(0)], env=NoEnv(), afinacion=notasAJ):
                
        self.muls = muls
        freqs = []
        for m in muls:
            freqs.append(m * freq)
        print(amp.next(np.zeros(CHUNK)))
        super().__init__(freqs, ondas, amp, amps, phases, [env])
        
    def setFreq(self, val):
        for m in range(0, len(self.muls)):
            self.freqs[m] = val * self.muls[m]
            self.synts[m].setFreq(self.freqs[m])
            
    def setEnv(self, env):
        for s in self.synts:
            s.setEnv(env)
        
    def getEnv(self):
        return self.synts[0].getEnv()
