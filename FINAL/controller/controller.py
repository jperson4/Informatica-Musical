class Controller:
    def __init__(self):
        self.controllables = []
        self.ins = []
    
    def add_controllable(self, controllable):
        ''' Añade un objeto controlable a la lista'''
        self.controllables.append(controllable)
        return len(self.controllables) - 1
    
    def remove_controllable(self, controllable):
        ''' Elimina un objeto controlable de la lista'''
        self.controllables.remove(controllable)

    def add_instrument(self, instrument):
        ''' Añade un instrumento a la lista'''
        self.ins.append(instrument)
        return len(self.ins) - 1
    
    def remove_instrument(self, instrument):
        ''' Elimina un instrumento de la lista'''
        self.ins.remove(instrument)

    def note_on(self, note, velocity=1, id=0):
        ''' Reproduce una nota MIDI'''
        self.ins[id].note_on(note, velocity)
    
    def note_off(self, note, id=0):
        ''' Detiene una nota MIDI'''
        self.ins[id].note_off(note)

    def play_knob(self, knob, value):
        ''' Reproduce un knob MIDI'''
        self.controllables[knob - 1][0].use_knob(value, self.controllables[knob - 1][1])

    