
from copy import deepcopy
from synt.function import *
from synt.const import *
from tkinter import *
import numpy as np

from synt.osc import *

# TODO ver si satura
class FilterIIR(Function):
    ''' recibe una funcion (generador de ondas) y devuelve su onda filtrada'''
    def __init__(self,signal:Function,alpha:Function, act=False, nombre='IIR',show=True):
        super().__init__(show, nombre)
        self.signal = signal
        self.mem = 0
        
        self.alpha = alpha
        _am = alpha.next(np.arange(0, CHUNK))
        
        if isinstance(_am, (list, np.ndarray)):
            self.alpha_mem = _am
        else:
            self.alpha_mem = 0
        # self.step = step 
        # por defecto inactivo
        self.act = act

    def fun(self, tiempo):
        data = self.signal.next(tiempo)
        
        _alf = self.alpha.next(tiempo)
        if isinstance(_alf, (list, np.ndarray)):
            _alpha = _alf
        else:
            _alpha = np.full(CHUNK, _alf)
        
        if self.act:
            data[0] = self.mem + self.alpha_mem * (data[0]-self.mem)
            for i in range(1,CHUNK):
                data[i] = data[i-1] + _alpha[i] * (data[i]-data[i-1])
            self.mem = data[CHUNK-1]
            
        self.mem = data[-1] # actualizamos memo con ultima muestra
        self.alpha_mem = float(_alpha[-1])
        
        return data

    def toggle(self):
        self.act = not self.act

    def activate(self):
        self.act = True

    def deactivate(self):
        self.act = False    

    def isActive(self):
        return self.act

    def doShow(self, tk, bg="#808090", side=TOP):
        _tk = super().doShow(tk, bg, side=TOP)
        # TODO hacer un boton para activar/desactivar
        self.alpha.addNombre('alpha')
        self.alpha.doShow(_tk, bg, side)
        act_button = Button(_tk, text='on/off', command=self.toggle)
        act_button.pack()
        return _tk
    # no hace falta teniendo el do show
    # def upAlpha(self):
        # self.alpha = min(2.0,max(0.1,self.alpha+self.step))

    # def downAlpha(self):
        # self.alpha = min(2.0,max(0.1,self.alpha-self.step))

class LPFilter(FilterIIR):
    def __init__(self,signal:Function,alpha:Function, act=False ,nombre='IIR',show=True):
        super().__init__(signal,alpha, nombre='LP',show=True)
        # _IIR1 = FilterIIR(Reverse(deepcopy(self.signal)), self.alpha, self.act)
        self.lp_0 = FilterIIR(deepcopy(self.signal), self.alpha, self.act)
        self.lp = FilterIIR(Reverse(self.lp_0), self.alpha, self.act)
        
    def fun(self, tiempo):
        if self.act:
            return self.lp_0.next(tiempo)
        else: 
            return self.signal.next(tiempo)
        # aplicamos dos veces para corregir el desplazamiento de fase
        
    def activate(self):
        self.act = True
        self.lp_0.activate()
        self.lp.activate()

    def deactivate(self):
        self.act = False  
        self.lp_0.deactivate()
        self.lp.deactivate

class HPFilter(FilterIIR):
    def __init__(self,signal:Function,alpha:Function, nombre='IIR',show=True):
        super().__init__(signal,alpha, nombre='LP',show=True)
        self.filt_alpha = C(2) - alpha
        self.lp = LPFilter(signal,self.filt_alpha, self.act)
    
    def fun(self, tiempo):
        if self.act:
            _sig = self.signal.next(tiempo)
            _lp = self.lp.next(tiempo)
            '''suena muy bajo'''
            return _sig - _lp
        else: 
            return self.signal.next(tiempo)
        
    def activate(self):
        self.act = True
        self.lp.activate()

    def deactivate(self):
        self.act = False  
        self.lp.deactivate
        
    

