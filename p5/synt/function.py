import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import scipy.signal as sg
from synt.const import *

from tkinter import *

'''
    Funciones: Al usar .next(tiempo), devuelven un np.array con los 
    valores que representan la función en el tiempo especificado.
    Pensadas para emular la programacion declarativa
    
'''

class Function:
    def __init__(self, tk:Tk, nombre=""):
        self.frame = 0 
        self.tk = tk
        self.nombre = nombre
        self.show = False # empieza a false para que solo se pueda cambiar una vez
    
    def __mul__(self, other):
        return Mult(self, other)
    
    def __truediv__(self, other):
        return Div(self, other)
    
    def __add__(self, other):
        return Add(self, other)
    
    def __sub__(self, other):
        return Sub(self, other)
    
    def __neg__(self):
        return Neg(self)
    
    def __pow__(self, other):
        return Exp(self)

    def next(self, tiempo = None):
        _tiempo = tiempo
        if tiempo is None: 
            _tiempo = np.arange(self.frame, self.frame + CHUNK)
            self.frame += CHUNK
        return self.fun(_tiempo) # devuelve vacío
    
    def fun(self, tiempo):
        '''esto es lo que se modiica en cada implementacion de Function'''
        return np.zeros(CHUNK)
    
    def doShow(self):
        if self.show is False and self.tk is not None: # si es None o True no entra
            self.show = True
            self.tk = LabelFrame(self.tk, text=self.nombre)
            self.tk.pack(side=LEFT)
            
    def addNombre(self, n): # no se si se va a usar pero weno
        if n != "" and self.nombre != "":
            n = n + ":"
        self.nombre = n + self.nombre
    
    
# TODO: hacer el show de las operaciones
class Add(Function): # f(x) = g(x) + h(x)
    def __init__(self, g, h):
        super().__init__()
        self.g = g
        self.h = h
        
    def fun(self, tiempo):
        _g = self.g.next(tiempo)
        _h = self.h.next(tiempo)
        return _g + _h
    
class Sub(Function): # f(x) = g(x) - h(x)
    def __init__(self, g, h):
        super().__init__()
        self.g = g
        self.h = h
        
    def fun(self, tiempo):
        _g = self.g.next(tiempo)
        _h = self.h.next(tiempo)
        return _g - _h  
    
class Mult(Function): # f(x) = g(x) * h(x)
    def __init__(self, g, h):
        super().__init__()
        self.g = g
        self.h = h
        
    def fun(self, tiempo):
        _g = self.g.next(tiempo)
        _h = self.h.next(tiempo)
        return _g * _h
    
class Div(Function): # f(x) = g(x) / h(x)
    def __init__(self, g, h):
        super().__init__()
        self.g = g
        self.h = h
        
    def fun(self, tiempo):
        _g = self.g.next(tiempo)
        _h = self.h.next(tiempo)
        return _g / _h  

class Neg(Function):
    def __init__(self, g):
        super().__init__()
        self.g = g
        
    def fun(self, tiempo):
        _g = self.g.next(tiempo)
        return -_g
    
# TODO añadir el otro valor del log
#f(x)=log(10,x .9+.1)+1 <-
class Log(Function):
    def __init__(self, g):
        super().__init__()
        self.g = g
        
    def fun(self, tiempo):
        _g = self.g.next(tiempo)
        return np.log(_g)

class Exp(Function):
    def __init__(self, g, e):
        super().__init__()
        self.g = g
        self.e = e
        
    def fun(self, tiempo):
        _g = self.g.next(tiempo)
        _e = self.e.next(tiempo)
        return _g ** _e
    
class Const(Function): # f(t) = valor
    def __init__(self, valor, tk:Tk=None, nombre="C", show=False, fr=None, to=None, step=None):
        super().__init__(tk, nombre)
        self.valor = valor
        
        self.fr = fr
        self.to = to
        self.step = step
        
        if step is None:
            self.step = valor / 100
        if fr is None:
            self.fr = valor - 10 * self.step
        if to is None:
            self.to = valor + 10 * self.step

        if show:
            self.doShow()
        
    def fun(self, tiempo):
        return self.valor # más rápido
        # return np.full(CHUNK, self.valor)
        
    def setVal(self, val):
        self.valor = val
        
    def doShow(self):
        super().doShow()
        if self.show is False and self.tk is not None: # si es None o True no entra
            slider=Scale(self.tk, from_=self.fr, to=self.to, resolution=self.step, orient=HORIZONTAL, label=self.nombre, command=self.setVal)
            slider.set(self.valor)
            slider.pack

class C(Const): # misma que const pero mas corta
    def __init__(self, valor, tk:Tk=None, nombre="C", show=False, fr=None, to=None, step=None):
        super().__init__(valor, tk, nombre, show, fr, to, step)
        
class X(Function): # f(t) = valor*t
    def __init__(self, valor=C(1), tk:Tk=None, avoid0 = False, nombre="X", show=False):
        super().__init__(tk, nombre, show)
        self.valor = valor
        self.avoid0 = avoid0
        if self.show:
            self.doShow()
    
    def fun(self, tiempo):
        z = 0
        _valor = self.valor / C(SRATE)
        if self.avoid0:
            z = 0.000001
        return tiempo * _valor.next(tiempo) + z
    
    def doShow(self):
        super().doShow()
        self.valor.addNombre(self.nombre)
        self.valor.doShow()
    
class XP(Function):
    def __init__(self, valor=C(1), exp=C(1), tk:Tk=None, avoid0 = False, nombre="X^exp", show=False):
        super().__init__(tk, nombre)
        self.exp = exp
        self.avoid0 = avoid0
        self.val = X(valor, tk, False, "X", False)
        if self.show:
            self.doShow()
    
    def fun(self, tiempo):
        z = 0
        if self.avoid0:
            z = 0.000001
        return (tiempo * self.val.next(tiempo)) ** self.exp.next(tiempo) + z

    def doShow(self):
        super().doShow() # crea el tk.frame
        self.val.addNombre(self.nombre) 
        self.val.doShow() # añade el valor al frame
        self.exp.addNombre("exp") # creo
        self.exp.addNombre(self.nombre)
        self.exp.doShow() # añade el exponente al frame




