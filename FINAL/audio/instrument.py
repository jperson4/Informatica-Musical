from pyo import *
from tools import *
from audio.synt import *
from audio.env import *
from audio.effectschain import *
from audio.effect import *
from view.gui import *
from controller.controllable import Controllable

class Instrument(PyoObject, Controllable):
    def __init__(self, env, synts:list[Synt] = [], name="ins"):
        Controllable.__init__(self, name)
        ''' Instrumento que reproduce notas con un oscilador y una envolvente'''
        self.synts = synts
        if len(synts) == 0:
            self.synts.append(Synt(HarmTable([1])))
            
        self.mixer = Mixer(1, chnls=1, mul=1)  # mixer para mezclar las notas
        
        for i, synt in enumerate(self.synts):
            self.mixer.addInput(i, synt)
            self.mixer.setAmp(i, 0, 1)
            
        """  gui = SynthGUI(self)
        gui.show_gui() """
    
        # Create an ADSR envelope
        #self.adsr = cAdsr(attack=0.01, decay=0.2, sustain=0.7, release=0.5, mul=1)
        self.env = env
        self.mixer.setMul(self.env)  # Apply the ADSR envelope to the mixer
        self.mixer.play()
        self.env.play()
        #self.effects = EffectsChain([STRev(Sine(1))], self.mixer)
        self._base_objs = self.mixer.getBaseObjects()
        #self._base_objs = self.effects.getBaseObjects()

    def note_on(self, note, velocity=1):
        ''' Envia la nota traducida a hz a un synt'''
        freq = note_to_Hz(note)
        for s in self.synts:
            s.note_on(note, freq, velocity)
        self.env.play()  # Trigger the ADSR envelope
            
    def note_off(self, note):
        for s in self.synts:
            s.note_off(note)
        self.env.stop()  # Release the ADSR envelope
            
    def out(self):
        return self.mixer.out()
    
    def play(self):
        return self.effects.play()
    
    def stop(self):
        return self.effects.stop()
    
    def sig(self):
        return self.effects.sig()
    
    def set_waveform(self, waveform, index=0):
        ''' Cambia la forma de onda del synt'''
        if index < len(self.synts):
            self.synts[index].table.setWaveform(waveform)
        else:
            print(f"Error: Index {index} out of range for synts list.")
            
    def add_synt(self, synt):
        self.synts.append(synt)
    
    def remove_synt(self, synt):
        self.synts.remove(synt)

    def use_knob(self, value, action):
        ''' Reproduce un knob MIDI'''
        if action == "amp":
            self.setMul(value)
        
    def report_actions(self):
        return ["amp"]
    
    def report_controllables(self):
        ret = Controllable.report_controllables(self)
        for s in self.synts:
            ret += s.report_controllables() 
        ret += self.env.report_controllables() 
        return ret 
