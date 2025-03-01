
from synt.const import *
import numpy as np
from tkinter import *



'''Envolvente: Recibe una serie de puntos y crea una funcion que los recorre'''
class Env:
    def __init__(self, fun, nombre="Env", show=True):
        self.fun = fun
        self.frame = 0
        self.nombre = nombre
        self.show = show
    
    def next(self, tiempo=None):
        _tiempo = []
        if tiempo is None: # guarda su propio frame si no le dan uno
            _tiempo = np.arange(self.frame, self.frame + CHUNK)
            self.frame += CHUNK
        else:
            _tiempo = tiempo
            self.frame = tiempo[0]
        part = self.fun(_tiempo)
        if (len(part) < CHUNK):
            part = np.concatenate((part, np.zeros(CHUNK-len(part))))
        return part
    
    def doShow(self, tk:Tk, bg="#808090", side=LEFT):
        '''crea un frame con su nombre para meter dentro sus elementos de forma recursiva'''
        if self.show is False:
            return None # para que acabe la recursion
        _tk = LabelFrame(tk, text=self.nombre, bg=bg)
        _tk.pack(side=side)
        return _tk    
    
    def addNombre(self, nombre):
        self.nombre = nombre
        
    def reset(self):
        self.frame = 0
        
    
class NoEnv(Env):
    def __init__(self, nombre="Env", show=True):
        super().__init__(self.fun)
        
    def fun(self, tiempo=None):
        return np.full(CHUNK, 1)
    
class EnvPP(Env):
    def __init__(self, points, nombre="Env", show=True):
        super().__init__(self.fun, nombre, show)
        env = np.zeros(0)
        # generamos la envolvente
        x0, y0 = points[0]
        
        _points = points[1:]
        if x0 != 0: # si el primero es 0, usamos el valor de y0, si no, empezamos en 0,0
            x0, y0 == 0, 0
            _points =np.concatenate(([(0,0)], points))
            
            
        for x, y in _points:
            x = round(x*SRATE) # traducir a segundos
            if x < 0: 
                x = 0
            env = np.concatenate((env, np.linspace(y0,y,x+1)[:-1])) # he quitado el [:-1] y no parece cambiar
            x0, y0, = x, y
        self.lastY = 0
        
        self.env = env
        
    def fun(self, tiempo=None):
        part = np.zeros(0)
        if (self.frame > len(self.env)):
            part = np.full(CHUNK, self.lastY)
            # print(self.lastY)
        else:
            part = self.env[self.frame:self.frame+CHUNK]
            rest = CHUNK - len(part)
            self.lastY = part[-1]
            if (len(part) < CHUNK):
                part = np.concatenate((part, np.full(rest, self.lastY)))
                
        self.lastY = part[-1]
        return part

# Esta envolvente tiene la duracion fija, no vale para el instrumento
class EnvADSR(EnvPP):
    '''
    atk, rel y sus van en segundos
    atk = segundos que tarda en crecer
    dec = segundos que tarda en alcanzar el sustain
    sus = valor que coge al decaer
    rel = segundos que tarda en decrecer
    dur = duracion total de la señal
    '''
    def __init__(self, atk, dec, sus, rel, dur, nombre="Env", show=True):
        _atk = (atk, 1)
        _dec = (dec, sus)
        _sus = (dur - rel, sus)
        _rel = (rel, 0)
        super().__init__([_atk, _dec, _sus, _rel], nombre, show)

# Esta envolvente tiene tres estados, atk, rel y off
class EnvInstrumento:
    '''
    atk, rel y sus van en segundos
    atk = segundos que tarda en alcanzar el maximo
    dec = segundos que tarda en alcanzar el sustain
    sus = valor que coge al decaer
    rel = segundos que tarda en decrecer
    '''
    def __init__(self, atk, dec, sus, rel, nombre="Env", show=True):
        _atk = (atk, 1)
        _dec = (dec, sus)
        # _sus = (dur - rel, sus)
        _rel = (rel, 0)
        self._rel = _rel
        self.sus = sus
        
        self.envAtk = EnvPP([_atk, _dec], nombre, show) # empieza en 0, sube a 1 y luego decae a sus
        self.envRel = EnvPP([(0,sus), _rel], nombre, show) # empieza en sus y baja hasta 0 en rel segundos
        self.state = 'atk'
        
    
    def next(self, tiempo=None):
        ret = 0
        # print(self.state)
        if self.state == 'atk':
            ret = self.envAtk.next()
        elif self.state == 'rel':           
            ret = self.envRel.next()
            if self.envRel.frame > self._rel[0] * SRATE:
                # print(self.rel.frame)
                # print(self._rel[0])
                print('off')
                self.state = 'off'
        elif self.state == 'off':
            # return 0
            return np.zeros(CHUNK)
        return ret 
        
    '''TODO: podria hacer una funcion noteOn para que si se vuelve a activar una nota que ya estaba sonando
        en vez de acabarse de golpe y empezar de 0, que empieze self.rel.lastY para que no sea tan brusco el cambio 
    '''    
    def noteOff(self):
        self.state = 'rel'#TODO: INFO era que tenia puesto == 
        self.rel = EnvPP([(0, self.envAtk.lastY), self._rel]) # empieza en el ultimo y baja hasta 0 en rel segundos        
        
    def getLast(self):
        if self.state == 'atk':
            return self.envAtk.lastY
        if self.state == 'rel':
            return self.envRel.lastY
        if self.state == 'off':
            return 0

    def doShow(self, tk:Tk, bg="#808090", side=LEFT):
        return tk #TODO
    
    def reset(self):
        self.envAtk.reset()
        self.envRel.reset()
        self.state = 'atk'