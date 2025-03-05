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
    def __init__(self, freq:Function, max=C(1), min=C(-1), amp:Function=None, phase=C(0), nombre="", show=False):
        super().__init__(show, nombre)
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
    
    def doShow(self, tk:Tk, bg="#808090", side=LEFT):
        _tk = super().doShow(tk, bg, side)
        if _tk is None:
            return None  
        self.freq.addNombre("freq")
        # self.freq.addNombre(self.nombre)
        self.freq.doShow(_tk, bg, side)
        if self.amp is not None:
            self.amp.addNombre("amp")
            # self.amp.addNombre(self.nombre)
            self.amp.doShow(_tk, bg, side)
        else:
            self.max.addNombre("max")
            # self.max.addNombre(self.nombre)
            self.min.addNombre("min")
            # self.min.addNombre(self.nombre)
            self.max.doShow(_tk, bg, side)
            self.min.doShow(_tk, bg, side)
        self.phase.addNombre("phase")
        # self.phase.addNombre(self.nombre)
        self.phase.doShow(_tk, bg, side)
        return _tk       
            
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
        
    def noteOff(self):
        pass
    
    def reset(self):
        self.frame = 0
    
class Sine(Osc): # f(t) = amp * sin(t * 2pi * freq + phase)
    def __init__(self, freq:Function, max=C(1), min=C(-1), amp=None, phase=C(0), nombre="Sine", show=False):
        super().__init__(freq, max, min, amp, phase, nombre, show)
        
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
    def __init__(self, freq:Function, max=C(1), min=C(-1), amp=None, phase=C(0), nombre="Triangle", show=False):
        super().__init__(freq, max, min, amp, phase, nombre, show)

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
    def __init__(self, freq:Function, max=C(1), min=C(-1), amp=None, phase=C(0), nombre="Sawtooth", show=False):
        super().__init__(freq, max, min, amp, phase, nombre, show)

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
    def __init__(self, freq:Function, max=C(1), min=C(-1), amp=None, phase=C(0), duty=C(.5), nombre="Square", show=False):
        super().__init__(freq, max, min, amp, phase, nombre, show)
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

class Rep(Osc):
    '''repite una funcion en base a una frecuencia'''
    def __init__(self, freq:Function, func:Function, max=C(1), min=C(-1), amp=None, phase=C(0), nombre="Rep", show=False):
        super().__init__(freq, max, min, amp, phase, nombre, show)
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
    
    def doShow(self, tk, bg="#808090", side=LEFT):
        _tk = super().doShow(tk, bg, side)
        if _tk is None:
            return None  
        self.func.addNombre("func")
        self.func.doShow(_tk)
    
class Sampler(Osc):
    '''reproduce una onda una vez a una velocidad especificada'''
    def __init__(self, freq:Function, sample:list, og_freq:Function=None, amp=C(1), samedur=False, nombre="Sampler", show=False):
        super().__init__(freq, None, None, amp, C(0), nombre, show)    
        self.sample = sample # onda
        self.state = 'on'
        
        if og_freq is None:
            self.og_freq = self.freq
        else:
            self.og_freq = og_freq
        self.sf = self.freq/self.og_freq
        
        if samedur is False:
            self.next = self._next
        
    def _next(self, tiempo = None): 
        '''
            cuando recibe el tiempo de otro parametro, cambia el tono pero el sample dura lo mismo
            (es como que lo coge por partes), para evitar esto, si samedur es False, usamos esta funcion
            que ignora el tiempo que se pasa por parametro
        '''
        _tiempo = np.arange(self.frame, self.frame + CHUNK)
        self.frame += CHUNK
        return self.fun(_tiempo) # devuelve vacío
        
    def fun(self, time):
        _sf = self.sf.next(time)
        if isinstance(_sf, list):
            _sf = _sf[0] # apaño
        
        # 1: obtenemos la parte que se va a reproducir
        parte = self.parteSample(int(time[0]), int(CHUNK*_sf))
        # 2: reducimos la parte para que quepa en un CHUNK
        puntos = np.arange(0, int(CHUNK*_sf)+1, step=_sf)[:CHUNK] # de 0 a N cada sf (puntos que queremos obtener)
        
        # len puntos = chunk / sf
        # _sample = np.interp(puntos, np.arange(0, int(CHUNK*_sf)+10)[:len(parte)], parte) # este falla a veces
        _sample = np.interp(puntos, np.linspace(0, CHUNK*_sf, len(parte)), parte)

        return _sample[:CHUNK] # en principio no haria falta el [:CHUNK]??
        
    def parteSample(self, _frame:int, N:int):
        '''devuelve de frame a N'''
        self.frame = _frame + N # hay que corregir el valor de self.frame
        if self.state == 'off' or _frame > len(self.sample):
            self.state = 'off'
            return np.zeros(CHUNK) 
        if _frame + N > len(self.sample):
            ret = np.concatenate((self.sample[_frame:], np.zeros(_frame + N - len(self.sample))))
            return ret[:N] # creo
        else:
            return self.sample[_frame:_frame+N]
        
        
    def doShow(self, tk, bg="#f0f0f0", side=LEFT):
        _tk = super().doShow(tk, bg, side)
        if _tk is None:
            return None  
        # self.freq.addNombre('freq')
        # self.freq.doShow(_tk)
        self.amp.addNombre('amp')
        self.amp.doShow(_tk)
        return _tk
        
    def setFreq(self, value):
        super().setFreq(value)
        self.sf = self.freq/self.og_freq
        
    def reset(self):
        super().reset()
        self.state = 'on'


class RSampler(Sampler): 
    '''reproduce una onda (con su frecuencia inicial a una frecuencia dada y en bucle'''
    def __init__(self, freq:Function, sample:list, og_freq:Function, amp=C(1), samedur=False, nombre="Rsampler", show=False):
        super().__init__(freq, sample, og_freq, amp, samedur, nombre, show)
        
    def parteSample(self, _frame:int, N:int):
        '''devuelve de frame a _frame + N de forma circular'''
        self.frame = _frame + N % len(self.sample)# hay que corregir el valor de self.frame
        if _frame > len(self.sample): # en principio nunca entra aqui
            return self.parteSample(_frame % len(self.sample), N) # recursion
        if _frame + N > len(self.sample):
            prev = self.sample[_frame:] # lo que queda
            rest = self.sample[:N - len(prev)]
            ret = np.concatenate((prev, rest))
            return ret[:N] # creo
        else:
            return self.sample[_frame:_frame+N]
        
        
class InstSampler(Osc):
    '''pone un sample al principio y luego otro durante el sustain y en el release'''
    def __init__(self, freq:Function, sAtk, fAtk:Function, sSus, fSus:Function=None, sRel=None, fRel=None, amp:Function = C(1), nombre="InstSampler", show=False):
        super().__init__(freq, None, None, amp, C(0), nombre, show)
        self.fAtk = fAtk
        if fSus is None:
            self.fSus = fAtk
        else:
            self.fSus = fSus
        
        if fSus is None:
            self.fRel = self.fSus
        else:
            self.fRel = fRel    
                      
        self.sAtk = Sampler(freq, sAtk, self.fAtk, amp=C(1, show=True),  show=show)
        self.sSus = RSampler(freq, sSus, self.fSus, amp=C(1, show=True), show=show)
        
        if sRel is None:
            # self.sRel = Sampler(freq, sSus, self.fRel, amp=C(1, show=True), show=show)
            self.sRel = self.sSus # es mejor asi para que no haya cambio
        else:
            self.sRel = Sampler(freq, sRel, self.fRel, amp=C(1, show=True), show=show)
        
        self.rel = False
        # self.sus_frame = 0
        
        
    def fun(self, tiempo):
        if self.sAtk.state == 'on':
            return self.sAtk.next()
        elif self.rel is False:
            # sus tiene que usar su propio tiempo 
            # _tiempo = np.arange(self.sus_frame, self.sus_frame + CHUNK)            
            # self.sus_frame += CHUNK
            return self.sSus.next()
        else: 
            return self.sRel.next()
        
    def noteOff(self):
        self.rel = True
        
    def reset(self):
        super().reset()
        self.rel = False
        self.sAtk.reset()
        self.sSus.reset()
        self.sRel.reset()
        
    def doShow(self, tk, bg="#808090", side=LEFT):
        _tk = super().doShow(tk, bg, side)
        self.sAtk.addNombre('atk sampler')
        self.sAtk.doShow(_tk, bg, side)
        self.sSus.addNombre('sus sampler')
        self.sSus.doShow(_tk, bg, side)
        self.sRel.addNombre('rel sampler')
        self.sRel.doShow(_tk, bg, side)
        
    def setFreq(self, value):
        super().setFreq(value)
        self.sAtk.setFreq(value)
        self.sSus.setFreq(value)
        self.sRel.setFreq(value)