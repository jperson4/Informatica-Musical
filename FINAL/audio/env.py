from pyo import * 

''' 
    Debido a que la función deepcopy no funciona con los objetos PyoObject, hemos tenido que implemantar
    estas clases que añaden la funcion copy
'''
class cAdsr(Adsr):
    def __init__(self, attack: float = 0.01, decay: float = 0.05, sustain: float = 0.707, release: float = 0.1, dur: int = 0, mul: int = 1, add: int = 0):
        super().__init__(attack, decay, sustain, release, dur, mul)
        
    def copy(self):
        return cAdsr(super().attack, super().decay, super().sustain, super().release, super().dur, super().mul)
    