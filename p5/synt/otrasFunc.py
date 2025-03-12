# en desuso

import numpy as np
import scipy.signal as sg

from synt.const import *
from synt.function import *
from synt.osc import *


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
    
class Tan(Osc): # f(t) = amp * tan(t * 2pi * freq + phase)
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