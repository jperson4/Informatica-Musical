import numpy as np
from synt.const import *
from synt.function import *
from synt.envolv import *
from copy import deepcopy
from copy import copy
from synt.mixer import *

from synt.osc import *

import math

class Synt(Function):
    '''Los synt son un oscilador que emplea otro oscilador para formar la onda puede estar sujeto a una envolvente'''
    def __init__(self, freq:Function, onda:Osc, amp:Const=Const(1), env=NoEnv(), 
                 nombre="Synt", show=True):
        super().__init__(show, nombre)
        self.onda = onda
        self.freq = freq
        self.amp = amp
        self.onda.setFreq(freq)
        self.env = env
    
    def fun(self, tiempo):
        return self.onda.next(tiempo) * self.env.next(tiempo) * self.amp.next(tiempo)
    
    def doShow(self, tk, bg="#808090", side=LEFT):
        _tk = super().doShow(tk)
        if _tk is None:
            return None  
        # self.amp.addNombre(self.nombre)

        # self.phase.addNombre(self.nombre)
        # self.freq.addNombre("freq")
        # self.freq.doShow(_tk)
        # self.phase.addNombre(self.nombre)
        # self.phase.addNombre("phase")
        # self.phase.doShow(_tk)
        # self.onda.addNombre(self.nombre)
        self.onda.addNombre("onda")
        self.onda.doShow(_tk, bg, side)
        # self.onda.addNombre(self.nombre)
        self.env.addNombre("env")
        self.env.doShow(_tk, bg, side)
        
        
        # raro
        # self.amp.addNombre("amp")
        # self.amp.doShow(_tk, bg, side)
        return _tk

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
class PolySynt(Function):
    def __init__(self, freqs:list[Function], ondas:list[Osc], amp=C(1), amps=[Const(1)], 
                 phases=[Const(0)], envs=[NoEnv()], fmix=tanh, nombre="polysint", show=True):
        super().__init__(show, nombre)
        # ajsutar que todo tenga el mismo numero de elementos
        n = len(freqs)
        self.n = n

        while len(ondas) < n:
            ondas.append(copy(ondas[0]))
        while len(amps) < n:
            amps.append(copy(amps[0]))
        while len(phases) < n:
            phases.append(copy(phases[0]))
        while len(envs) < n:
            envs.append(copy(envs[0]))
        
        self.synts = []
        # usamos una lista de sintetizadores
        for i in range(0, n):
            self.synts.append(Synt(freqs[i], ondas[i], amps[i], envs[i], str(i), self.show))
            # = Synt(freqs[i], ondas[i], amps[i], phases[i], envs[i])
        
        # guardamos para poder devolverlas si se piden
        self.amp = amp
        self.freqs = freqs
        self.amps = amps
        self.phases = phases  
        self.ondas = ondas
        self.frame = 0
        self.envs = envs
        self.amp = amp
        self.nombre = nombre
        self.show = show
        self.mixer = Mixer(self.synts, fmix)

    def fun(self, tiempo):
        # onda = np.zeros(CHUNK)     
        # fact = 1 / math.sqrt(len (self.synts))
        # for s in self.synts:
        #     onda = onda + (s.next(tiempo) * fact)
        onda = self.mixer.next(tiempo)
        return onda * self.amp.next(tiempo)
    
    def doShow(self, tk, bg="#808090", side=LEFT, showAll=True):
        _tk = super().doShow(tk, side=side)
        
        self.amp.doShow(_tk, bg, side, VERTICAL)
        if _tk is None:
            return None  
        if not showAll:
            return _tk
        for i in range(0, self.n):
            self.synts[i].doShow(_tk)
        # self.amp.addNombre("amp")
        # self.mixer.doShow(_tk)
        return _tk

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
    def __init__(self, freq:Function, muls:Function, ondas, amp=C(1, show=True), 
                 amps=[Const(1)], phases=[Const(0)], env=NoEnv(),
                 fmix=tanh ,nombre="harmsynt", show=True):      
        self.muls = muls
        self.freq = freq
        freqs = []
        for m in muls:
            freqs.append(m * freq)
        print(amp.next(np.zeros(CHUNK)))
        super().__init__(freqs, ondas, amp, amps, phases, [env], fmix, nombre, show)
        
    def setFreq(self, val):
        self.freq = val
            
        for m in range(0, len(self.muls)):
            self.freqs[m] = self.freq * self.muls[m]
            self.synts[m].setFreq(self.freqs[m])
            
    def setSliderFreq(self, _val):
        val = float(_val)
        if isinstance(self.freq, Const): # no creo que haga falta
            self.freq.setVal(val)
            
        for m in range(0, len(self.muls)):
            self.freqs[m] = self.freq * self.muls[m]
            self.synts[m].setFreq(self.freqs[m])        
            
    def doShow(self, tk, bg="#808090", side=LEFT):
        _tk = super().doShow(tk, side=side, showAll=False)
        if _tk is None:
            return None  
        for i in range(0, self.n):
            self.muls[i].addNombre("mul")
            self.muls[i].addNombre(i)
            self.muls[i].doShow(_tk, side=BOTTOM)
            
            self.synts[i].addNombre("synts")
            self.synts[i].addNombre(i)
            self.synts[i].doShow(_tk, side=BOTTOM)
        
        if self.freq.show and isinstance(self.freq, Const):
            slider=Scale(tk, from_=self.freq.fr, to=self.freq.to, resolution=self.freq.step, orient=HORIZONTAL, label=self.freq.nombre, command=self.setSliderFreq)
            slider.set(self.freq.valor)
            slider.pack(side=side)
        return _tk
        # self.amp.addNombre("amp")
        # self.amp.doShow(_tk)
            
    def setEnv(self, env):
        for s in self.synts:
            s.setEnv(env)
        
    def getEnv(self):
        return self.synts[0].getEnv()
