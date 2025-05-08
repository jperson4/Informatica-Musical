from pyo import *
from tools import *
from audio.synt import *
from audio.env import *

class Instrument(PyoObject):
    def __init__(self):
        super().__init__(self)
        ''' Instrumento que reproduce notas con un oscilador y una envolvente'''
        # PyoObject.__init__(self)
        self.synts = [] # lista de synts
        self.synts.append(Synt(Sine(1), cAdsr(attack=.5)))
        self.mixer = Mixer(1, chnls=1, mul=1) # mixer para mezclar las notas
        self.mixer.addInput(0, self.synts[0])
        self.mixer.setAmp(0, 0, 1)
        self.effects = [] # lista de efectos
        self._base_objs = self.mixer.getBaseObjects()
        

    def note_on(self, note, velocity=1):
        ''' Envia la nota traducida a hz a un synt'''
        freq = note_to_Hz(note)
        for s in self.synts:
            s.note_on(note, freq, velocity)
            
    def note_off(self, note):
        for s in self.synts:
            s.note_off(note)
            
    def out(self):
        self.mixer.out()
        return PyoObject.out(self)
    
    def play(self):
        return PyoObject.play(self)
    
    def stop(self):
        return PyoObject.play(self)

    def play_knob(self, knob):
        ''' Reproduce un knob MIDI'''
        print(f"Playing knob: {knob}")
        # Aqui se puede añadir la funcionalidad de los knobs