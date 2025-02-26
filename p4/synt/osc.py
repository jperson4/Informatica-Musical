import numpy as np
import scipy.signal as sg

from synt.const import *
from synt.function import *

''' 
    osciladores: generan una onda nparray con unos parametros dados,
    las características particulares (bpm, etc) se declaran al
    inicializar el objeto correspondiente de la clase Osc o sus derivadas.
'''

class Osc(Function):    
    def __init__(self, freq:Function, max=C(1), min=C(-1), amp=None, phase=C(0)):
        super().__init__()
        self.freq = freq
        self.phase = phase
        self.frame = 0
        if amp is None:
            self.max = max
            self.min = min
            self.amp = None
        else: 
            self.max = None
            self.min = None
            self.amp = amp
    
    # esto va a ser lo que se modifique
    def fun(self, tiempo):
        return np.zeros(len(tiempo))        
            
    def getFreq(self):
        return self.freq

    def setFreq(self, value):
        self.freq = value

    def getMax(self):
        return self.max

    def setMax(self, value):
        self.max = value

    def getMin(self):
        return self.min

    def setMin(self, value):
        self.min = value

    def getAmp(self):
        return self.amp

    def setAmp(self, value):
        self.amp = value

    def getPhase(self):
        return self.phase

    def setPhase(self, value):
        self.phase = value
    
class Sine(Osc): # f(t) = amp * sin(t * 2pi * freq + phase)
    def __init__(self, freq:Function, max=C(1), min=C(0), amp=None, phase=C(0)):
        super().__init__(freq, max, min, amp, phase)
        
    def fun(self, tiempo):
        _freq = self.freq.next(tiempo)
        _phase = self.phase.next(tiempo)
        _amp = None
        _offset = 0

        # si se usa amp o max min
        if self.amp is None:
            _amp = (self.max.next(tiempo) - self.min.next(tiempo)) / 2
            _offset = (self.max.next(tiempo) + self.min.next(tiempo)) / 2
        else: 
            _amp = self.amp.next(tiempo)
        
        # funcion
        onda = np.sin(tiempo * (2 * np.pi * _freq/SRATE) + _phase)
        return onda * _amp + _offset
    
class Triangle(Osc): # f(t) = amp * arcsin(sin(t * 2pi * freq + phase)) * 2/pi   -> 2/pi es para que vaya de 1 a -1
    def __init__(self, freq:Function, max=C(1), min=C(0), amp=None, phase=C(0)):
        super().__init__(freq, max, min, amp, phase)

    def fun(self, tiempo):
        _freq = self.freq.next(tiempo)
        _phase = self.phase.next(tiempo)
        _amp = None
        _offset = 0

        # si se usa amp o max min
        if self.amp is None:
            _amp = (self.max.next(tiempo) - self.min.next(tiempo)) / 2
            _offset = (self.max.next(tiempo) + self.min.next(tiempo)) / 2
        else: 
            _amp = self.amp.next(tiempo)
        
        # funcion
        onda = (2 / np.pi) * np.arcsin(np.sin(tiempo * (2 * np.pi * _freq/SRATE) + _phase))
        return onda * _amp + _offset
    
class Sawtooth(Osc): # f(t) = amp * arctan(tan(t * 2pi * freq + phase)) * 2/pi   -> 2/pi es para que vaya de 1 a -1
    def __init__(self, freq:Function, max=C(1), min=C(0), amp=None, phase=C(0)):
        super().__init__(freq, max, min, amp, phase)

    def fun(self, tiempo):
        _freq = self.freq.next(tiempo)
        _phase = self.phase.next(tiempo)
        _amp = None
        _offset = 0

        # si se usa amp o max min
        if self.amp is None:
            _amp = (self.max.next(tiempo) - self.min.next(tiempo)) / 2
            _offset = (self.max.next(tiempo) + self.min.next(tiempo)) / 2
        else: 
            _amp = self.amp.next(tiempo)
        
        onda = (2 / np.pi) * np.arctan(np.tan(tiempo * (1 * np.pi * _freq/SRATE) + _phase))
        return onda * _amp + _offset

class Square(Osc):
    def __init__(self, freq:Function, max=C(1), min=C(0), amp=None, phase=C(0), duty=C(.5)):
        super().__init__(freq, max, min, amp, phase)
        self.duty = duty # no implementado

    def fun(self, tiempo):
        _freq = self.freq.next(tiempo)
        _phase = self.phase.next(tiempo)
        _amp = None
        _offset = 0

        # si se usa amp o max min
        if self.amp is None:
            _amp = (self.max.next(tiempo) - self.min.next(tiempo)) / 2
            _offset = (self.max.next(tiempo) + self.min.next(tiempo)) / 2
        else: 
            _amp = self.amp.next(tiempo)
        
        onda = sg.square((2*np.pi * tiempo) * _freq / SRATE + _phase)
        return onda * _amp + _offset

class Rep(Osc): # repite una funcion en base a la frecuencia
    def __init__(self, freq:Function, func:Function, max=C(1), min=C(-1), amp=None, phase=C(0)):
        super().__init__(freq, max, min, amp, phase)
        self.func = func
        
    def fun(self, tiempo):
        _tiempo = tiempo % self.freq.next() 
        _phase = self.phase.next(_tiempo)
        _tiempo = tiempo + _phase * SRATE # en este caso la fase son segundos
        _amp = None
        _offset = 0

        # si se usa amp o max min
        if self.amp is None:
            _amp = (self.max.next(_tiempo) - self.min.next(_tiempo)) / 2
            _offset = (self.max.next(_tiempo) + self.min.next(_tiempo)) / 2
        else: 
            _amp = self.amp.next(_tiempo)
        
        onda = self.func.next(_tiempo)
        
        return onda * _amp + _offset
