import numpy as np   
from osc import *
from const import *

class OscFM(Osc):
    def __init__(self,freq=110.0,amp=1.0,fm=6.0, beta=1.0, shapeMod=Sine, chunk=CHUNK, samplerate=SRATE):
        super().__init__(freq, self.oscfm, amp, 0, chunk, samplerate)
        # self.fm = fm     
        # self.beta = beta 
        # moduladora = βsin(2πfm)
        self.mod = shapeMod(freq=fm,amp=beta, chunk=chunk, samplerate=samplerate)
    
    def setBeta(self, beta):
        self.mod.setAmp(beta)
        
    def setFM(self, fm):
        self.mod.setFreq(fm)
        
    def getFM(self):
        return self.mod.getFreq()
    
    def getBeta(self):
        return self.mod.getAmp()
    
    def oscfm(self):  
        # sin(2πfc+mod)  
        # sacamos el siguiente chunk de la moduladora
        mod = self.mod.next()

        # soporte para el chunk de salida
        sample = np.arange(self.frame,self.frame+self.chunk)        
        # aplicamos formula
        out =  self.amp*np.sin(2*np.pi*self.freq*sample/self.samplerate + mod)
        # self.frame += self.chunk
        return out 
