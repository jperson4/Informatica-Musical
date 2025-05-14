from pyo import *
from tools import *
from audio.synt import *
from audio.env import *
from audio.effectschain import *
from audio.effect import *
from controller.controllable import Controllable

class Instrument(PyoObject, Controllable):
    def __init__(self, env):
        super().__init__()
        ''' Instrumento que reproduce notas con un oscilador y una envolvente'''
        self.synts = []  # lista de synts
        self.synts.append(Synt(HarmTable([1, .75])))
        self.mixer = Mixer(1, chnls=1, mul=1)  # mixer para mezclar las notas
        self.mixer.addInput(0, self.synts[0])
        self.mixer.setAmp(0, 0, 1)
        
        # Create an ADSR envelope
        self.adsr = Adsr(attack=0.01, decay=0.2, sustain=0.7, release=0.5, mul=1)
        self.env = env
        self.mixer.setMul(self.adsr)  # Apply the ADSR envelope to the mixer
        self.mixer.play()
        self.env.play()
        # self.effects = EffectsChain([STRev(Sine(1))], self.mixer)
        self._base_objs = self.effects.getBaseObjects()

    def note_on(self, note, velocity=1):
        ''' Envia la nota traducida a hz a un synt'''
        freq = note_to_Hz(note)
        for s in self.synts:
            s.note_on(note, freq, velocity)
        self.adsr.play()  # Trigger the ADSR envelope
            
    def note_off(self, note):
        for s in self.synts:
            s.note_off(note)
        self.adsr.stop()  # Release the ADSR envelope
            
    def out(self):
        return self.effects.out()
    
    def play(self):
        return self.effects.play()
    
    def stop(self):
        return self.effects.stop()
    
    def sig(self):
        return self.effects.sig()

    def use_knob(self, value, action):
        ''' Reproduce un knob MIDI'''
        if action == "amp":
            self.setMul(value)
        
    def report_actions(self):
        return ["amp"]
    
    def report_controllables(self):
        ret = super().report_controllables()
        for s in self.synts:
            ret += s.report_controllables() 
        return ret 
