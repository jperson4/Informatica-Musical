
from synt.function import *
from synt.const import *
from tkinter import *

from synt.osc import *
import matplotlib.pyplot as plt

# TODO ver si satura
class FilterIIR(Function):
    ''' recibe una funcion (generador de ondas) y devuelve su onda filtrada'''
    def __init__(self,signal:Function,alpha:Function, nombre='IIR',show=True):
        super().__init__(show, nombre)
        self.signal = signal
        self.mem = 0
        self.alpha = alpha
        # self.step = step 
        # por defecto inactivo
        self.act = False

    def fun(self, tiempo):
        data = self.signal.next(tiempo)
        if self.act:
            data[0] = self.mem + self.alpha.next(tiempo) * (data[0]-self.mem)
            for i in range(1,CHUNK):
                data[i] = data[i-1] + self.alpha.next(tiempo) * (data[i]-data[i-1])
            self.mem = data[CHUNK-1]
        self.mem = data[-1] # actualizamos memo con ultima muestra
        return data

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
        
        return _tk
    # no hace falta teniendo el do show
    # def upAlpha(self):
        # self.alpha = min(2.0,max(0.1,self.alpha+self.step))

    # def downAlpha(self):
        # self.alpha = min(2.0,max(0.1,self.alpha-self.step))
