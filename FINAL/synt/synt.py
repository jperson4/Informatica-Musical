from pyo import *

class Synth(PyoObject):
    def __init__(self, osc, env, transpo=1, amp=1):
        ''' Reproduce notas'''
        super().__init__()
        self.transpo = Sig(transpo)
        self.osc = osc
        self.env = env
        self.amp = amp

        self.playingNotes = {}
        self.decayingNotes = {}
        
        self.mixer = Mixer(1, chnls=1, initsize=0, mul=0.5) # mixer para mezclar las notas
        # cuando toquemos una nota, la añadimos al mixer


    def out(self):
        "Sends the synth's signal to the audio output and return the object itself."
        # self.notch.out()
        return PyoObject.out(self)



    def sig(self): # puede que no sea necesario
        "Returns the synth's signal for future processing."
        return self.notch