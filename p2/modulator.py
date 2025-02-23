from osc import *
from const import *
from modulator import *
from copy import copy
class Modulator:
    def __init__(self,signal,freq=1,v0=0.,v1=1.,srate=SRATE):
        self.signal = signal
        self.freq = freq
        self.v0 = v0
        self.v1 = v1
        self.t = 0
        self.srate = srate
    
    def next(self):
        # Generar el chunk de la señal original
        original_chunk = self.signal.next()
        
        # Generar la señal de modulación
        t = np.arange(self.t, self.t + len(original_chunk)) / self.srate
        modulation = (self.v1 - self.v0) / 2 * np.sin(2 * np.pi * self.freq * t) + (self.v1 + self.v0) / 2
        
        # Modulación de la señal original
        modulated_chunk = original_chunk * modulation
        
        # Actualizar el tiempo
        self.t += len(original_chunk)
        
        return modulated_chunk
    
class Modulator2:
    '''modula cualquier par de objetos osc'''
    def __init__(self, signal, shape, v0=0., v1=1., samplerate=SRATE, chunk=CHUNK):
        self.signal = signal
        self.shape = shape
        self.signal.setChunk(chunk)
        self.shape.setChunk(chunk)
        self.shape.setAmp((v1 - v0) / 2) # no va >:(
        # print(str(self.shape.getAmp()))
        self.v0 = v0
        self.v1 = v1
        self.samplerate = SRATE
        
    def next(self):
        original = self.signal.next()
        modulation = self.shape.next() + (self.v1 + self.v0) / 2
        # print(modulation[:29])
        modulated = original * modulation
        return modulated
        
        
