from pyo import *
from controller.controllable import Controllable


class Reverb(STRev, Controllable):
    def __init__(self, input, inpos=0.5, revtime=1, cutoff=5000, bal=0.5, roomSize=1, firstRefGain=-3, mul=1, add=0):
        super().__init__(input, inpos, revtime, cutoff, bal, roomSize, firstRefGain, mul, add)
        
    def use_knob(self, value, action):
        if action == "impos":
            self.setInpos(value)
        elif action == "revtime":
            self.setRevtime(value)
        elif action == "cutoff":
            self.setCutoff(value)
        elif action == "bal":
            self.setBal(value)
        elif action == "roomsize":
            self.setRoomsize(value)
        elif action == "firstrefgain":
            self.setFirstrefgain(value)

    def report_actions(self):
        return ["impos", "revtime", "cutoff", "bal", "roomsize", "firstrefgain"]