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
    def __init__(self, show, nombre=""):
        self.frame = 0 
        self.nombre = nombre
        self.show = show # empieza a false para que solo se pueda cambiar una vez
    
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
    
    def doShow(self, tk:Tk, bg="#808090"):
        '''crea un frame con su nombre para meter dentro sus elementos de forma recursiva'''
        if self.show is False:
            return None # para que acabe la recursion
        
        _tk = LabelFrame(tk, text=self.nombre, bg=bg)
        
        _tk.pack(side=LEFT)
        return _tk             
    
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
    def __init__(self, valor, nombre="C", show=False, fr=None, to=None, step=None):
        super().__init__(show, nombre)
        self.valor = valor
        self.fr = fr
        self.to = to
        self.step = step
        
        _valor = valor
        if valor == 0: # cuando es 0 se lia
            _valor = 1
        
        if step is None:
            self.step = _valor / 1000
        if fr is None:
            # self.fr = valor - 1000 * self.step
            self.fr = 0
        if to is None:
            self.to = _valor + 1500 * self.step
        

        # if show:
            # self.doShow()
        
    def fun(self, tiempo):
        return self.valor # más rápido
        # return np.full(CHUNK, self.valor)
        
    def setVal(self, val):
        self.valor = float(val)
        
    def doShow(self, tk:Tk):
        '''crea un frame con su nombre para meter dentro sus elementos de forma recursiva'''
        '''Const es un caso especial porque es un caso base'''
        
        if self.show is False:
            return None # para que acabe la recursion
        
        # hacemos un slider y lo metemos en root
        slider=Scale(tk, from_=self.fr, to=self.to, resolution=self.step, orient=HORIZONTAL, label=self.nombre, command=self.setVal)
        slider.set(self.valor)
        slider.pack(side=LEFT)
        
        # _tk = super().doShow(tk)
        # self.fr.doShow(_tk)
        # self.to.doShow(_tk)
        # self.step.doShow(_tk)
        
        return tk # diria que no hace falta pero bueno

class C(Const): # misma que const pero mas corta
    def __init__(self, valor, nombre="", show=False, fr=None, to=None, step=None):
        super().__init__(valor, nombre, show, fr, to, step)
        
class X(Function): # f(t) = valor*t
    def __init__(self, valor=C(1), avoid0 = False, nombre="X", show=False):
        super().__init__(nombre, show)
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
    
    def doShow(self,  tk:Tk):
        _tk = super().doShow(tk)
        
        self.valor.addNombre(self.nombre)
        self.valor.doShow(_tk)
    
class XP(Function):
    def __init__(self, valor=C(1), exp=C(1), avoid0 = False, nombre="X^exp", show=False):
        super().__init__(nombre, show)
        self.exp = exp
        self.avoid0 = avoid0
        self.val = X(valor, False, "X", show)
        if self.show:
            self.doShow()
    
    def fun(self, tiempo):
        z = 0
        if self.avoid0:
            z = 0.000001
        return (tiempo * self.val.next(tiempo)) ** self.exp.next(tiempo) + z
    
    def doShow(self,  tk:Tk):
        _tk = super().doShow(tk)
        
        # if _tk is None:
        #     print("No has introducido un Tk")
        #     return None # para que acabe la recursion
        # print("Has introducido un Tk")
        
        self.val.addNombre(self.nombre) 
        self.val.doShow(_tk) # añade el valor al frame
        self.exp.addNombre("exp") # creo
        self.exp.addNombre(self.nombre)
        self.exp.doShow(_tk) # añade el exponente al frame





