import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import scipy.signal as sg
from synt.const import *

'''
    Funciones: Al usar .next(tiempo), devuelven un np.array con los 
    valores que representan la función en el tiempo especificado.
    Pensadas para emular la programacion declarativa
    
'''

class Function:
    def __init__(self):
        pass
    
    def __mul__(self, other):
        return Mult(self, other)
    
    def __truediv__(self, other):
        return Div(self, other)
    
    def __add__(self, other):
        return Add(self, other)
    
    def __sub__(self, other):
        return Sub(self, other)

    def next(self, tiempo = None):
        if tiempo is None: 
            tiempo = np.arange(0, CHUNK)
        return self.fun(tiempo) # devuelve vacío
    
    # esto va a ser lo que se modifique en cada implementacion
    def fun(self, tiempo):
        return np.zeros(CHUNK)
    
    
    
class Add(Function): # f(x) = g(x) + h(x)
    def __init__(self, g, h):
        super().__init__()
        self.g = g
        self.h = h
        
    def next(self, tiempo):
        _g = self.g.next(tiempo)
        _h = self.h.next(tiempo)
        return _g + _h
    
class Sub(Function): # f(x) = g(x) - h(x)
    def __init__(self, g, h):
        super().__init__()
        self.g = g
        self.h = h
        
    def next(self, tiempo):
        _g = self.g.next(tiempo)
        _h = self.h.next(tiempo)
        return _g - _h  
    
class Mult(Function): # f(x) = g(x) * h(x)
    def __init__(self, g, h):
        super().__init__()
        self.g = g
        self.h = h
        
    def next(self, tiempo):
        _g = self.g.next(tiempo)
        _h = self.h.next(tiempo)
        return _g * _h
    
class Div(Function): # f(x) = g(x) / h(x)
    def __init__(self, g, h):
        super().__init__()
        self.g = g
        self.h = h
        
    def next(self, tiempo):
        _g = self.g.next(tiempo)
        _h = self.h.next(tiempo)
        return _g / _h  
    
class Const(Function): # f(t) = valor
    def __init__(self, valor):
        super().__init__()
        self.valor = valor
        
    def __neg__(self):
        return Const(-self.valor)
    
    def next(self, tiempo):
        return np.full(len(tiempo), self.valor)
    
    def getValor(self):
        return self.valor
    
    def setValor(self, valor):
        self.valor = valor

    
class C(Const): # misma que const pero mas corta
    def __init__(self, valor):
        super().__init__(valor)
        
class X(Function): # f(t) = valor*t
    def __init__(self, valor=C(1)):
        super().__init__()
        self.valor = valor / C(SRATE)
        
    def next(self, tiempo):
        return tiempo * self.valor.next(tiempo)
    
class X1(Function): # f(t) = valor*t sin 0
    def __init__(self, valor=C(1)):
        super().__init__()
        self.valor = valor / C(SRATE)
        
    def next(self, tiempo):
        return tiempo * self.valor.next(tiempo) + 0.00001
    
class XP(Function):
    def __init__(self, valor, pow):
        super().__init__()
        self.valor = valor
        self.pow = pow
    
    def next(self, tiempo):
        return tiempo * self.valor.next(tiempo) ** self.pow.next(tiempo) + 0.00001
            
    
class FunOsc(Function): 
    '''Funcion osciladora (seno, triangulo, etc)'''
    def __init__(self, freq:Function, max=C(1), min=C(0), amp=None, phase=C(0)):
        super().__init__()
        self.freq = freq
        self.phase = phase
        if amp is None:
            self.max = max
            self.min = min
            self.amp = None
        else: 
            self.max = None
            self.min = None
            self.amp = amp
            
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
        

class Sine(FunOsc): # f(t) = amp * sin(t * 2pi * freq + phase)
    def __init__(self, freq, max=C(1), min=C(0), amp=None, phase=C(0)):
        super().__init__(freq, max, min, amp, phase)
        
    def next(self, tiempo):
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
        onda = _amp * np.sin(tiempo * (2 * np.pi * _freq/SRATE) + _phase)
        return onda + _offset
    
class Triangle(FunOsc): # f(t) = amp * arcsin(sin(t * 2pi * freq + phase))
    def __init__(self, freq, max=C(1), min=C(0), amp=None, phase=C(0)):
        super().__init__(freq, max, min, amp, phase)

    def next(self, tiempo):
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
        onda = (2 * _amp / np.pi) * np.arcsin(np.sin(tiempo * (2 * np.pi * _freq/SRATE) + _phase))
        return onda + _offset
    
class Sawtooth(FunOsc): # f(t) = amp * arctan(tan(t * 2pi * freq + phase))
    def __init__(self, freq, max=C(1), min=C(0), amp=None, phase=C(0)):
        super().__init__(freq, max, min, amp, phase)

    def next(self, tiempo):
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
        
        
        onda = (2 * _amp / np.pi) * np.arctan(np.tan(tiempo * (1 * np.pi * _freq/SRATE) + _phase))
        return onda + _offset

class Square(FunOsc):
    def __init__(self, freq, max=C(1), min=C(0), amp=None, phase=C(0), duty=C(.5)):
        super().__init__(freq, max, min, amp, phase)
        self.duty = duty # no implementado

    def next(self, tiempo):
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
        
        onda = _amp * sg.square((2*np.pi * tiempo) * _freq / SRATE + _phase)
        return onda + _offset
    

class Tan(FunOsc): # f(t) = amp * tan(t * 2pi * freq + phase)
    def __init__(self, freq, max=C(1), min=C(0), amp=None, phase=C(0)):
        super().__init__(freq, max, min, amp, phase)

    def next(self, tiempo):
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
        
        onda = _amp * np.tan(tiempo * (2 * np.pi * _freq/SRATE) + _phase)
        return onda + _offset
    

