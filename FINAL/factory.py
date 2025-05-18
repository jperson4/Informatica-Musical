from audio.instrument import *
from controller.controller import *
from audio.synt import *
from pyo import *


class Factory:
    ''' Esta clase se encarga de crear los objetos Instrument de añadirles synts y efectos
        además, su funcion setup devuelve la onda base a la que se van a añadir las siguientes
    '''
    def __init__(self, controller:Controller):
        self.controller = controller
        self.out = Sig(0, 0)
        # self.out.out() # no suena
        # self.inst_set = set()
        self.inst_set = []
        
    def add_instrument(self, instrument:Instrument):
        self.controller.add_instrument(instrument)
        self.out = self.out + instrument
        instrument.out() # apaño?
        # self.inst_set.add(instrument)
        self.inst_set.append(instrument)
        
    def remove_instrument(self, instrument:Instrument):
        self.controller.remove_instrument(instrument)
        instrument.stop()
        self.inst_set.remove(instrument)
        
    def add_synt_to_inst(self, synt:Synt, instrument:Instrument):
        instrument.add_synt(synt)
        # self.controller.add_controllable(synt)
        self.controller.refresh()
        
    def remove_synt_from_inst(self, synt:Synt, instrument:Instrument):
        instrument.remove_synt(synt)
        self.controller.refresh()

    # def play(self):
    #     # self.out.out()
        
    # def pause(self):
    #     # self.out.stop()
        
    