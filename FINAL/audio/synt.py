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
        self.mixer = Mixer(1, chnls=1, mul=1)  # mixer para mezclar las notas
        self._base_objs = self.mixer.getBaseObjects()

    def note_on(self, id, freq, velocity=1):
        ''' Crea una copia del oscilador y las pone a sonar añadiendolas al mixer'''
        print(f"note_on {id}")
        _id = id
        _osc = Osc(self.table, freq=freq, mul=self.amp)
        _osc.play()
        if id in self.playingNotes:
            self.mixer.delInput(id)
        self.playingNotes[_id] = _osc
        self.mixer.addInput(_id, _osc)
        self.mixer.setAmp(_id, 0, 1)

    def note_off(self, id):
        ''' Detiene el oscilador y lo elimina del mixer'''
        if id in self.playingNotes:
            print(f"note_off {id}")
            self.playingNotes[id].stop()
            self.mixer.delInput(id)
            del self.playingNotes[id]

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
        return super().report_controllables()

    def set_table(self, table):
        self.table = table

    def get_table(self):
        return self.table
