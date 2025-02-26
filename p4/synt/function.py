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
    
    def __neg__(self):
        return Neg(self)
    
    def __pow__(self, other):
        return Exp(self)

    def next(self, tiempo = None):
        '''esta función debería dejarse sin tocar (salvo en casos como const donde no sea necesario el tiempo)'''
        if tiempo is None: 
            tiempo = np.arange(0, CHUNK)
        return self.fun(tiempo) # devuelve la funcion
    
    
    def fun(self, tiempo):
        '''esto es lo que se modiica en cada implementacion de Function'''
        return np.zeros(CHUNK)
    
    
    
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
        
    def _fun(self, tiempo):
        _g = self.g.next(tiempo)
        return -_g
    
# TODO añadir el otro valor del log
class Log(Function):
    def __init__(self, g):
        super().__init__()
        self.g = g
        
    def _fun(self, tiempo):
        _g = self.g.next(tiempo)
        return np.log(_g)

class Exp(Function):
    def __init__(self, g, e):
        super().__init__()
        self.g = g
        self.e = e
        
    def _fun(self, tiempo):
        _g = self.g.next(tiempo)
        _e = self.e.next(tiempo)
        return _g ** _e
    
class Const(Function): # f(t) = valor
    def __init__(self, valor):
        super().__init__()
        self.valor = valor
        
    def next(self, tiempo):
        return self.valor # más rápido
        # return np.full(CHUNK, self.valor)

class C(Const): # misma que const pero mas corta
    def __init__(self, valor):
        super().__init__(valor)
        
class X(Function): # f(t) = valor*t
    def __init__(self, valor=C(1), avoid0 = False):
        super().__init__()
        self.valor = valor / C(SRATE)
        self.avoid0 = avoid0
    
    def next(self, tiempo):
        z = 0
        if self.avoid0:
            z = 0.000001
        return tiempo * self.valor.next(tiempo) + z
    
class XP(Function):
    def __init__(self, valor, pow, avoid0 = False):
        super().__init__()
        self.valor = valor / C(SRATE)
        self.pow = pow
        self.avoid0 = avoid0
    
    def next(self, tiempo):
        z = 0
        if self.avoid0:
            z = 0.000001
        return tiempo * self.valor.next(tiempo) ** self.pow.next(tiempo) + z

#f(x)=log(10,x .9+.1)+1 <-



