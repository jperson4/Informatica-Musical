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
    def __init__(self, freq:Function, max=C(1), min=C(-1), amp:Function=None, phase=C(0), tk:Tk=None, nombre="", show=False):
        super().__init__(show, tk, nombre)
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
    
    def doShow(self, tk:Tk=None):
        _tk = super().doShow(tk)
        _root = self.getRoot(_tk) # obtenemos el frame en el que vamos a añadir las cosas
        
        if _root is None:
            print("No has introducido un Tk")
            return None # para que acabe la recursion
        print("Has introducido un Tk")
        
        self.freq.addNombre("freq")
        self.freq.addNombre(self.nombre)
        self.freq.doShow(_root)
        if self.amp is not None:
            self.amp.addNombre("amp")
            self.amp.addNombre(self.nombre)
            self.amp.doShow(_root)
        else:
            self.max.addNombre("max")
            self.max.addNombre(self.nombre)
            self.min.addNombre("min")
            self.min.addNombre(self.nombre)
            self.max.doShow(_root)
            self.min.doShow(_root)
        self.phase.addNombre("phase")
        self.phase.doShow(_root)       
            
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
    def __init__(self, freq:Function, max=C(1), min=C(-1), amp=None, phase=C(0), tk:Tk=None, nombre="", show=False):
        super().__init__(freq, max, min, amp, phase, tk, nombre, show)
        
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
        p3 = _freq/SRATE
        p2 = tiempo * (2 * np.pi)
        p1 = p2 * p3
        onda = np.sin(p1 + _phase)
        # onda = np.sin(tiempo * (2 * np.pi * _freq/SRATE) + _phase)
        return onda * _amp + _offset
    
class Triangle(Osc): # f(t) = amp * arcsin(sin(t * 2pi * freq + phase)) * 2/pi   -> 2/pi es para que vaya de 1 a -1
    def __init__(self, freq:Function, max=C(1), min=C(-1), amp=None, phase=C(0), tk:Tk=None, nombre="", show=False):
        super().__init__(freq, max, min, amp, phase, tk, nombre, show)

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
    def __init__(self, freq:Function, max=C(1), min=C(-1), amp=None, phase=C(0), tk:Tk=None, nombre="", show=False):
        super().__init__(freq, max, min, amp, phase, tk, nombre, show)

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
    def __init__(self, freq:Function, max=C(1), min=C(-1), amp=None, phase=C(0), duty=C(.5), tk:Tk=None, nombre="", show=False):
        super().__init__(freq, max, min, amp, phase, tk, nombre, show)
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
    def __init__(self, freq:Function, func:Function, max=C(1), min=C(-1), amp=None, phase=C(0), tk:Tk=None, nombre="", show=False):
        super().__init__(freq, max, min, amp, phase, tk, nombre, show)
        self.func = func
        
    def fun(self, tiempo):
        _phase = self.phase.next(tiempo)
        _tiempo = tiempo
        # _tiempo = tiempo + _phase # TODO: ver como sacar la fase
        _tiempo = _tiempo % (SRATE/self.freq.next()) # frecuencia en Hz
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
    
    def doShow(self):
        super().doShow()
        self.func.addNombre("func")
        self.func.doShow()
    
class Sampler(Function):
    def __init__(self, sample:list, speed_factor:Function, tk:Tk=None, nombre="", show=False):
        super().__init__(tk, nombre)    
        self.sample = sample
        self.sf = speed_factor
        
    def fun(self, time):
        # TODO hacer el speed_factor
        _sample = self.sample
        frame = time[0]
        if frame > len(_sample):
            return np.zeros(CHUNK) # devuelve 0 si se ha pasado del sample
        if frame + CHUNK > len(_sample):
            ret = np.concatenate((_sample[frame:], np.zeros(frame + CHUNK - len(_sample))))
            return ret[:CHUNK] # creo
        else:
            return _sample[frame:frame+CHUNK]
        
    def doShow(self):
        super().doShow()
        self.sf.addNombre("sf")
        self.sf.doShow()


class RSampler(Osc):
    def __init__(self, freq, sample:list, sfreq, max=C(1), min=C(-1), amp=None, phase=C(0), tk:Tk=None, nombre="", show=False):
        super().__init__(freq, max, min, amp, phase)
        self.sample = sample
        # TODO 