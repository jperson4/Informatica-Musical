from pyo import *
from copy import copy

@DeprecationWarning # DEPRECATED
class Nota(PyoObject):
    def __init__(self, freq, osc, env, amp=1):
        PyoObject.__init__(self)
        ''' Oscilador que oscila a una frecuencia dada con una envolvente y amplitud'''
        self.freq = freq
        self.osc = copy(osc)
        self.env = copy(env) # deberia hacer copy?
        self.osc.setFreq(self.freq)
        self.osc.setMul(amp * self.env) # multiplicamos la envolvente por la amplitud
        self.osc.stop() # lo mismo no deberia parar el oscilador base
        self._base_objs = self.osc.getBaseObjects()
           
    def play(self):
        ''' Funcionamiento: 
            al pulsar una tecla, se llama a esta funcion, que activa el oscilador (si estuviera parado) y tmb activa la envolvente.
            cuando se suelta la tecla, se llama a note_off, que manda la señal stop a la envolvente (para que vaya parando) 
            y posteriormene, en un bucle externo, se chekeara que la envolvente es 0 y si es asi, se manda la señal stop al oscilador.
        '''
        self.osc.play() # activamos que envie señal, lo mismo es mejor dejarlo en play continuamente y confiar en la envolvente?
        self.env.play() # activamos la envolvente
        return PyoObject.play(self)
        
    def note_off(self):
        ''' Desactiva el oscilador.'''
        # self.osc.stop() # desactivamos el oscilador
        self.env.stop()
        
    def out(self):
        ''' Envía la señal a la salida de audio.'''
        # self.osc.play() # en verdad mejor que de primeras ni suene y que suene cuando le demos al play
        self.env.play()
        return PyoObject.out(self)
    
    def getAmp(self):
        return self.osc.getMul()
    
    def stop(self):
        ''' Desactiva el oscilador.'''
        self.osc.stop()
        return PyoObject.stop(self)
        