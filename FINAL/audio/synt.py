from pyo import *
from copy import copy
from copy import deepcopy
from controller.controllable import Controllable
import pickle

class Synt(PyoObject, Controllable):
    ''' Recibe un oscilador
        en note_on crea una copia del oscilador y la hace sonar
        en note_off detiene el oscilador y lo elimina del mixer
    '''

    def __init__(self, table, amp=1):
        ''' Reproduce notas'''
        super().__init__()
        self.table = table
        self.amp = Sig(amp)

        self.playingNotes = {}
        self.envmap = {}
        self.mixer = Mixer(1, chnls=1, mul=1)  # mixer para mezclar las notas
        self._base_objs = self.mixer.getBaseObjects()

    def note_on(self, id, freq, env, velocity=1):
        ''' Crea una copia del oscilador y las pone a sonar añadiendolas al mixer'''
        print(f"note_on {id}")
        _osc = Osc(self.table, freq=freq, mul=self.amp)
        _env = env.copy()
        self.envmap[id] = _env
        self.playingNotes[id] = _osc
        TrigFunc(_env["trig"], lambda: self.remove_decayed(id)) # elimina la nota cuando decaiga
        if id in self.playingNotes:
            self.mixer.delInput(id)
        self.playingNotes[id] = _osc
        _osc.play()
        _env.play()
        self.mixer.addInput(id, _osc * _env)
        self.mixer.setAmp(id, 0, 1)

    def note_off(self, id):
        ''' Dice a la envolvente que entre en modo decay'''
        self.envmap[id].stop()
        # if id in self.playingNotes:
        #     print(f"note_off {id}")
        #     self.playingNotes[id].stop()
        #     self.mixer.delInput(id)
        #     del self.playingNotes[id]

    def remove_decayed(self, id):
        ''' Elimina las notas que ya han acabado'''
        if id in self.playingNotes:
            print(f"remove note {id}")
            self.playingNotes[id].stop()
            self.mixer.delInput(id)
            del self.playingNotes[id]
            del self.envmap[id]

    def out(self):
        "Sends the synth's signal to the audio output and return the object itself."
        return PyoObject.out(self)

    def play(self):
        return PyoObject.play(self)

    def stop(self):
        for osc in self.playingNotes.values():
            osc.stop()
        self.playingNotes.clear()
        return PyoObject.stop(self)

    def sig(self):
        "Returns the synth's signal for future processing."
        return self.mixer

    def use_knob(self, value, action):
        ''' Reproduce un knob MIDI'''
        super().use_knob(value, action)
        if action == "amp":
            self.amp.value = value

    def report_actions(self):
        return ["amp"]

    def report_controllables(self):
        return Controllable.report_controllables(self)

    def set_table(self, table):
        self.table = table

    def get_table(self):
        return self.table
