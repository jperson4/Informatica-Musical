
from synt.const import *
import numpy as np
import math

# TODO: en valores muy pequeños, intenta multiplicar arrays de tamaños distintos
class Delay:
    def __init__(self, input, time=1):
        self.osc = input
        _time = int(time * SRATE)
        self.time = _time
        self.frame = 0
        self.mem = np.zeros(_time)

    def next(self):
        signal = self.osc.next()
        chunk = len(signal)
        # se tiene que ir llenando desde atras :/
        if self.frame + chunk < self.time:  # si cabe
            _s = self.mem[self.frame:self.frame + chunk].copy()
            self.mem[self.frame:self.frame + chunk] = signal
            signal = _s
        else:
            rest = self.frame + chunk - self.time
            # cabe = selt.time - self.frame
            signal1 = self.mem[:rest].copy()
            signal2 = self.mem[self.frame:].copy()
            self.mem[:rest] = signal[chunk-rest:] 
            self.mem[self.frame:] =  signal[:chunk-rest]
            
            # self.mem[rest:chunk+rest] = signal
            _s = np.concatenate((signal2, signal1))
            # print(len(signal1))
            # print(len(signal1))
            # print(len(signal))
        self.frame = (self.frame + chunk) % self.time
        return _s

# TODO: en valores muy pequeños, intenta multiplicar arrays de tamaños distintos
class Echo:
    def __init__(self, osc, val=.5, time=1, restar=False):
        self.osc = osc
        self.val = val
        _time = int(time*SRATE)
        self.time = _time
        self.frame = 0
        self.mem = np.zeros(_time)
        self.restar = restar

    def next(self):
        signal = self.osc.next()
        chunk = len(signal)
        val_sig = 1
        val_echo = self.val
        # va un poco raro con restar = True
        if self.restar: 
            val_sig = math.sqrt(1-self.val) # pongo esto porque no se si hacer que sea 1 o 1-val
            val_echo = math.sqrt(self.val)
            
            # val_sig = 1-self.val
            # val_echo = self.val
            
        if self.frame + chunk <= self.time:  # si cabe
            signal = signal * val_sig + (self.mem[self.frame:self.frame+chunk] * val_echo)
            self.mem[self.frame:self.frame+chunk] = signal
        else:
            rest = self.frame + chunk - self.time
            # rest = len(self.mem)-self.frame
            # self.mem = np.concatenate((np.zeros(rest - len(self.mem)-self.frame), self.mem))
            signal1 = signal[:self.time-self.frame] * val_sig + (self.mem[self.frame:self.time] * val_echo)
            signal2 = signal[self.time-self.frame:self.time-self.frame+rest] * val_sig + (self.mem[:rest] * val_echo)
            signal = np.concatenate((signal1, signal2))
            self.mem[self.frame:] = signal1
            self.mem[:rest] = signal2
        self.frame = (self.frame + chunk) % self.time
        return signal
    
