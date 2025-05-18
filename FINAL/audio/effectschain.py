from pyo import *

class EffectsChain(PyoObject):
    def __init__(self, list, input:PyoObject):
        super().__init__()
        self.output = input
        # super().__init__()
        # self.list = list
        # self.input = input
        # self.input.stop()
        # self.output = None
        # self.setup()
        # self.input.play()
        # self._base_objs = self.output.getBaseObjects()
        
    def setup(self):
        
        if len(self.list) == 0:
            self.output = self.input
            return
        
        aux = self.list[0]
        aux.setInput(self.input, 0)
        for i in range(1, len(self.list)):
            f = self.list[i]
            f.setInput(aux, 0)
            aux = f
        self.output = aux

    def getOutput(self):
        return self.output

    def out(self):
        # for s in self.list:
        #     s.play()
        return self.output.out()
    
    def play(self):
        for s in self.list:
            s.play()
        return self.output.play()
    
    def stop(self):
        for s in self.list:
            s.stop()
        return self.output.stop()
    
    def sig(self):
        return self.output.sig()
    
    def getEffects(self):
        return self.list[1:]
        
