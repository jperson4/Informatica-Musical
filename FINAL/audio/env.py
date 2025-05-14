from pyo import * 
from controller.controllable import *

''' 
    Debido a que la función deepcopy no funciona con los objetos PyoObject, hemos tenido que implemantar
    estas clases que añaden la funcion copy
'''
class cAdsr(Adsr, Controllable):
    def __init__(self, attack: float = 0.01, decay: float = 0.05, sustain: float = 0.707, release: float = 0.1, dur: int = 0, mul: int = 1, add: int = 0):
        super().__init__(attack, decay, sustain, release, dur, mul)
        self.attack_mod = 2 # maximo ataque?
        self.decay_mod = 2
        self.sustain_mod = 2
        self.release_mod = 3
        
    def copy(self):
        return cAdsr(super().attack, super().decay, super().sustain, super().release, super().dur, super().mul)
    
    def use_knob(self, value, action):
        if action == "atk":
            self.setAttack(value * self.attack_mod)
        if action == "dec":
            self.setDecay(value * self.decay_mod)
        if action == "sus":
            self.setSustain(value * self.sustain_mod)
        if action == "rel":
            self.setRelease(value * self.release_mod)
            
    def report_actions(self):
        return ["atk", "dec", "sus", "rel"]
    
    