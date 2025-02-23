
import numpy as np
import scipy.signal as sg
from const import *

# clase abstacta oscilador
class Osc:
    def __init__(self, freq, shape, amp=1.0, phase=0.0, chunk=CHUNK, samplerate=SRATE):
        self.freq = freq
        self.amp = amp
        self.phase = phase
        self.samplerate = samplerate
        self.chunk = chunk
        self.onda = shape
        self.frame = 0
      
    def setFreq(self, freq):
        self.freq = freq
        
    def setChunk(self, chunk):
        self.chunk = chunk
      
    def setAmp(self, amp):
        self.amp = amp
      
    def getFreq(self):
        return self.freq

    def getAmp(self):
        return self.amp
    
    def getChunk(self):
        return self.chunk

    def next(self):
        onda = self.onda()
        self.frame += self.chunk
        return onda
  
class Sine(Osc):
    def __init__(self, freq, amp=1.0, phase=0.0, chunk=CHUNK, samplerate=SRATE):
        super().__init__(freq, self.sine, amp, phase, chunk, samplerate)

    def sine(self):
        tiempo = np.arange(self.frame, self.chunk + self.frame) # array con el tiempo
        onda = self.amp * np.sin(tiempo * (2 * np.pi * self.freq/self.samplerate) + self.phase)
        return onda


class Square(Osc):
    def __init__(self, freq, duty=0.5, amp=1.0, phase=0.0, chunk=CHUNK, samplerate=SRATE):
        super().__init__(freq, self.square, amp, phase, chunk, samplerate)
        self.duty = duty

    def square(self):
        # duty no está implementado
        tiempo = np.arange(self.frame, self.chunk + self.frame) # array con el tiempo
        # onda = np.where((tiempo - self.phase) * self.freq/self.samplerate % 1 < self.duty, self.amp, -self.amp)
        onda = self.amp * sg.square((2*np.pi * tiempo) * self.freq / self.samplerate + self.phase)
        return np.float32(onda)


class Triangle(Osc):
    def __init__(self, freq, amp=1.0, phase=0.0, chunk=CHUNK, samplerate=SRATE):
        super().__init__(freq, self.triangle, amp, phase, chunk, samplerate)

    def triangle(self):
        tiempo = np.arange(self.frame, self.chunk + self.frame) # array con el tiempo
        onda = (2 * self.amp / np.pi) * np.arcsin(np.sin(tiempo * (2 * np.pi * self.freq/self.samplerate) + self.phase))
        return onda


class Sawtooth(Osc):
    def __init__(self, freq, amp=1.0, phase=0.0, chunk=CHUNK, samplerate=SRATE):
        super().__init__(freq, self.sawtooth, amp, phase, chunk, samplerate)

    def sawtooth(self):
        tiempo = np.arange(self.frame, self.chunk + self.frame) # array con el tiempo
        onda = (2 * self.amp / np.pi) * np.arctan(np.tan(tiempo * (1 * np.pi * self.freq/self.samplerate) + self.phase))
        # si pongo 2 * np.pi...,(como dice wikipedia) creo que sale al doble de frecuencia de lo que debería
        return onda

class Kick(Osc):
    def __init__(self, freq, amp=1.0, phase=0.0, chunk=CHUNK, samplerate=SRATE, bpm=130, beat=0., dur = 1.):
        super().__init__(freq, self.kick, amp, phase, chunk, samplerate)
        self.bpm = bpm
        self.beat = beat % 4
        time = self.samplerate*60/self.bpm
        self.frame = int(time / 4 * beat)
        self.dur = dur

    # def kick(self):
    #     freq = self.freq
    #     time = self.samplerate*60/self.bpm
    #     if (self.frame > time):
    #         self.frame = 0
    #     tiempo = np.arange(self.frame, self.chunk + self.frame)
    #     onda = self.amp * np.sin(time * (np.pi * self.freq/self.samplerate)/(tiempo+.1) + self.phase)
    #     return onda
    
    def kick(self):
        freq = self.freq
        time = self.samplerate*60/self.bpm
        tiempo = np.zeros(0)
        if (self.chunk + self.frame >= time):
            t1 = np.arange(self.frame, time)
            t2 = np.arange(0, self.chunk - len(t1))
            self.frame -= time
            
            tiempo = np.concatenate((t1, t2))
        else:
            tiempo = np.arange(self.frame, self.chunk + self.frame)
            
        
        onda = np.sin((self.samplerate / self.dur) * (np.pi * self.freq/self.samplerate)/(tiempo+.1) + self.phase)
        return onda * self.amp
  
class HarmOsc(Osc):
    def __init__(self, freq, amps, shapes, amp=1.0, phase=0.0, chunk=CHUNK, samplerate=SRATE, norm=True):
        super().__init__(freq, self.harmOsc, amp, phase, chunk, samplerate)        
        # añade a shapes shapes[0] si el tamaño de shapes es menor que el de amps hasta que tengan el mismo tamaño
        if len(shapes) < len(amps):
            shapes = shapes + [shapes[0]] * (len(amps) - len(shapes))
        self.ondas = []
        for a in range(len(amps)):
            self.ondas.append(shapes[a](freq * (a + 1), amp=amps[a], phase=phase , chunk=chunk, samplerate=samplerate))
        self.norm = norm

    def setFreq(self, freq):
      # hay que cambiar las frecuencias 1 a una para cada onda
        self.freq = freq
        for o in range(len(self.ondas)):
            self.ondas[o].setFreq(freq * (o + 1))

    def harmOsc(self):
        harm = np.zeros(self.chunk)
        for o in self.ondas:
            harm = harm + o.next()
        if self.norm:
            harm = harm /  max(np.max(harm), -np.min(harm))
        return harm * self.amp
      
      
class Sumador(Osc):
    def __init__(self, ondas, amp=1., chunk=CHUNK, samplerate=SRATE, norm=True):
        super().__init__(0, self.suma, amp, 0, chunk, samplerate) 
        self.ondas = ondas
        for o in self.ondas:
            o.setChunk = chunk
        self.norm = norm
        
    def suma(self):
        signal = np.zeros(self.chunk)
        for o in self.ondas:
            signal = signal + o.next()
        if self.norm:
            signal = signal / max(np.max(signal), -np.min(signal))
        return signal * self.amp
            
                 
