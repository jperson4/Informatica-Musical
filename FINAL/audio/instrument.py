from pyo import *
from tools import *
from audio.synt import *
from audio.env import *
from audio.effectschain import *
from audio.effect import *
from controller.controllable import Controllable

class Instrument(PyoObject, Controllable):
    def __init__(self):
        super().__init__()
        ''' Instrumento que reproduce notas con un oscilador y una envolvente'''
        # PyoObject.__init__(self)
        self.synts = [] # lista de synts
        self.synts.append(Synt(HarmTable([1, .75]), cAdsr(attack=.5)))
        self.mixer = Mixer(1, chnls=1, mul=1) # mixer para mezclar las notas
        self.mixer.addInput(0, self.synts[0])
        self.mixer.setAmp(0, 0, 1)
        self.mixer.play()
        self.effects = EffectsChain([STRev(self.mixer)], self.mixer)
        self._base_objs = self.effects.getBaseObjects()
        

    def note_on(self, note, velocity=1):
        ''' Envia la nota traducida a hz a un synt'''
        freq = note_to_Hz(note)
        for s in self.synts:
            s.note_on(note, freq, velocity)
            
    def note_off(self, note):
        for s in self.synts:
            s.note_off(note)
            
    def out(self):
        return self.effects.out(self)
    
    def play(self):
        # for s in self.synts:
        #     s.play()
        return self.effects.play(self)
    
    def stop(self):
        # for s in self.synts:
        #     s.stop()
        return self.effects.stop(self)
    
    def sig(self):
        return self.effects.sig(self)

    def use_knob(self, value, action):
        ''' Reproduce un knob MIDI'''
        # sube o baja el volumen de cada synt
        super().use_knob(value, action)
        if action == "amp":
            self.setMul(value)
        
    def report_actions(self):
        return ["amp"]