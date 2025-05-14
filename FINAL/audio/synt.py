from pyo import *
from copy import copy
from copy import deepcopy
from controller.controllable import Controllable
import pickle

class Synt(PyoObject, Controllable):
    ''' Recibe un oscilador y una envolvente
        en note_on crea una copia del oscilador y la hace sonar
        en note_off dice a la envolvente que empiece a decaer, cuando decaiga, se eliminara la copia del oscilador aunque
        
        todos los osciladores suenan porque se meten en el mixer cuando los creamos
        (cuando se apagan, los sacamos del mixer)
    '''

    def __init__(self, table, env, amp=1):
        ''' Reproduce notas'''
        super().__init__()
        # self.transpo = Sig(transpo)
        self.table = table
        self.env = env
        self.amp = Sig(amp) # CHECK

        self.playingNotes = {}
        self.decayingNotes = {}
        
        self.mixer = Mixer(1, chnls=1, mul=1) # mixer para mezclar las notas
        # cuando toquemos una nota, la añadimos al mixer
        self._base_objs = self.mixer.getBaseObjects()

        
    def note_on(self, id, freq, velocity=1):
        ''' Crea una copia del oscilador y las pone a sonar añadiendolas al mixer'''
        # freq = idToFreq[id] * self.transpo

        print(f"note_on {id}")
        _id = id
        _osc = Osc(self.table, freq=freq, mul=self.amp)
        # _env = self.env.copy()
        # _osc.setFreq(freq) # de forma que puedas dejar el oscilador 
        # _osc.setMul(_osc.mul * self.amp)
        # _env =  pickle.loads(pickle.dumps(self.env))
        _env = self.env.copy()
        # _env = Adsr(**vars(self.env))
        # _env.stop() #? puede CHECK
        _osc.play()
        _env.play()
        TrigFunc(_env["trig"], lambda: self.remove_decaying(_id)) # cuando acabe la envolvente, elimina la nota
        if id in self.playingNotes or id in self.decayingNotes:
            self.mixer.delInput(id)
        self.playingNotes[_id] = (_osc, _env)
        self.mixer.addInput(_id, _osc * _env)
        self.mixer.setAmp(_id, 0, 1)

        
    def note_off(self, id):
        ''' Saca la nota de playing u la añade a decaying, activa el decay de la envolvente'''
        if id in self.playingNotes:
            print(f"note_off {id}")
            self.decayingNotes[id] = self.playingNotes[id]
            self.decayingNotes[id][1].stop() # activa el decay de la envolvente
            del self.playingNotes[id]
            
    def remove_decaying(self, id):
        print(f"nota {id} eliminada")
        ''' Elimina las notas que ya han terminado de decaer y ya no estan sonando'''
        self.decayingNotes[id][0].stop() # para la nota del todo
        self.mixer.delInput(id)
        del self.decayingNotes[id]
                
    def out(self):
        "Sends the synth's signal to the audio output and return the object itself."
        # self.notch.out()
        # self.mixer.out()
        return PyoObject.out(self)
    
    def play(self):
        return PyoObject.play(self)
    
    def stop(self):
        for n in self.playingNotes:
            n[1].stop()
        return PyoObject.play(self)

    def sig(self): # puede que no sea necesario
        "Returns the synth's signal for future processing."
        return self.notch
    
    def use_knob(self, value, action):
        ''' Reproduce un knob MIDI'''
        # sube o baja el volumen de cada synt
        super().use_knob(value, action)
        if action == "amp":
            self.setMul(value)
        # TODO ver si encontramos una manera de meter ondas dentro de otras (y poder controlarlo)
            
    def report_actions(self):
        return ["amp"]
    
    def report_controllables(self):
        ret = super().report_controllables()
        ret += [self.env]
        
        return ret 
    
    def set_table(self, table):
        self.table = table
    
    def get_table(self):
        return self.table