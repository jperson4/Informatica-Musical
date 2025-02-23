from const import *
import numpy as np

class Echo:
    def __init__(self, osc, val=.5, time=1, samplerate=SRATE, restar=False):
        self.osc = osc
        self.val = val
        _time = int(time*samplerate)
        self.time = _time
        self.frame = 0
        self.anterior = np.zeros(_time)
        self.restar = restar

    def next(self):
        signal = self.osc.next()
        chunk = len(signal)
        resta = 1
        if self.restar: 
            resta = 1-self.val # pongo esto porque no se si hacer que sea 1 o 1-val
            
        if self.frame + chunk <= self.time:  # si cabe
            signal = signal * resta + (self.anterior[self.frame:self.frame+chunk] * self.val)
            self.anterior[self.frame:self.frame+chunk] = signal
        else:
            rest = self.frame + chunk - self.time
            signal1 = signal[:self.time-self.frame] * resta + (self.anterior[self.frame:self.time] * self.val)
            signal2 = signal[self.time-self.frame:] * resta + (self.anterior[:rest] * self.val)
            signal = np.concatenate((signal1, signal2))
            self.anterior[self.frame:] = signal1
            self.anterior[:rest] = signal2
        self.frame = (self.frame + chunk) % self.time
        return signal
    
class Delay:
    def __init__(self, input, time=1, samplerate=SRATE):
        self.osc = input
        _time = int(time*samplerate)
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
    

    

    

    
