import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import scipy.signal as sg
from synt.const import *
from synt.function import *

''' 
    osciladores: generan una onda nparray con unos parametros dados,
    las características particulares (bpm, etc) se declaran al
    inicializar el objeto correspondiente de la clase Osc o sus derivadas.
'''
# TODO: Son un poco redundantes con la clase function, lo mismo podría modificar el sintetizador para que use Function en todas partes
class Osc:    
    def __init__(self):
        pass
    
    def next(self, freq, tiempo, amp=Const(1), phase=Const(0)):
        return np.zeros(len(tiempo)) # devuelve vacío

class Sine(Osc):
    def __init__(self):
        super().__init__()
        
    def next(self, freq, tiempo, amp=Const(1), phase=Const(0)):
        _freq = freq.next(tiempo) # frecuencia sobre el tiempo
        _amp = amp.next(tiempo) # amplitud sobre el tiempo
        _phase = phase.next(tiempo) 
        onda = _amp * np.sin(tiempo * (2 * np.pi * _freq/SRATE) + _phase)
        return onda

class Square(Osc):
    def __init__(self, duty=Const(.5)):
        super().__init__()
        self.duty = duty

    def next(self, freq, tiempo, amp=Const(1), phase=Const(0)):
        # duty solo se puede usar en valor constante (por ahora)
        _duty = self.duty.next(tiempo)[0]
        _freq = freq.next(tiempo)  # frecuencia sobre el tiempo
        _amp = amp.next(tiempo)  # amplitud sobre el tiempo
        _phase = phase.next(tiempo)
        onda = _amp * sg.square(2*np.pi*tiempo*_freq/SRATE+_phase, _duty)
        return onda

class Triangle(Osc):
    def __init__(self):
        super().__init__()
        
    def next(self, freq, tiempo, amp=Const(1), phase=Const(0)):
        _freq = freq.next(tiempo)  # frecuencia sobre el tiempo
        _amp = amp.next(tiempo)  # amplitud sobre el tiempo
        _phase = phase.next(tiempo)
        onda = _amp * np.arcsin(np.sin(tiempo * (2 * np.pi * _freq/SRATE) + _phase))
        return onda
    
class Sawtooth(Osc):
    def __init__(self):
        super().__init__()
        
    def next(self, freq, tiempo, amp=Const(1), phase=Const(0)):
        _freq = freq.next(tiempo)  # frecuencia sobre el tiempo
        _amp = amp.next(tiempo)  # amplitud sobre el tiempo
        _phase = phase.next(tiempo)
        onda = (2 *  _amp / np.pi) * np.arctan(np.tan(tiempo * (1 * np.pi * _freq/SRATE) + _phase))
        return onda

class Kick(Osc):
    # no se que puede pasar si ponemos una funcion no constante en beat :0
    def __init__(self, bpm=C(130), beat=C(1), dur=C(1)):
        super().__init__()
        self.bpm = bpm
        self.dur = dur
        self.beat = beat

    def next(self, freq, tiempo, amp=Const(1), phase=Const(0)):
        _bpm = self.bpm.next(tiempo)
        _beat = self.beat.next(tiempo)
        _negra = (SRATE*60/_bpm)/4
        _tiempo = (tiempo + _negra * _beat) % (_negra * 4) # desplazamiento del tiempo
        _freq = freq.next(_tiempo)  # frecuencia sobre el tiempo
        _amp = amp.next(_tiempo)  # amplitud sobre el tiempo
        _phase = phase.next(_tiempo)
        onda = _amp * np.sin((SRATE / self.dur) * (np.pi * _freq/SRATE)/(_tiempo+.1) + _phase)
        return onda

class Sinc(Osc):
    def __init__(self):
        super().__init__()
        
    def next(self, freq, tiempo, amp=Const(1), phase=Const(0)):
        _freq = freq.next(tiempo) # frecuencia sobre el tiempo
        _amp = amp.next(tiempo) # amplitud sobre el tiempo
        _phase = phase.next(tiempo) 
        onda = np.sin(tiempo * 2 * np.pi * _freq/SRATE + _phase) / (tiempo * 2 * np.pi * _freq/SRATE)
        return onda * _amp


class ModSawtooth(Osc):
    def __init__(self, other:Function):
        super().__init__()
        self.other = other
        
    def next(self, freq, tiempo, amp=Const(1), phase=Const(0)):
        _freq = freq.next(tiempo)  # frecuencia sobre el tiempo
        _amp = amp.next(tiempo)  # amplitud sobre el tiempo
        _phase = phase.next(tiempo)
        _other = self.other.next(tiempo)
        onda = (2 *  _amp / np.pi) * np.arctan(np.tan(tiempo * (1 * np.pi * _freq/SRATE) + _phase) + _other)
        return onda
