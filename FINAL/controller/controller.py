class Controller:
    def __init__(self):
        self.controllables = [] # lista de todos los objetos controlables
        # self.knob_actions = [set(), set(), set(), set(), set(), set(), set(), set()] # un set de pares por cada valor
        self.knob_actions = [[],[],[],[],[],[],[],[]]
        self.ins = []
    
    def add_controllable(self, controllable):
        ''' Añade un objeto controlable a la lista'''
        self.controllables.append(controllable)
        # return len(self.controllables) - 1
    
    def remove_controllable(self, controllable):
        ''' Elimina un objeto controlable de la lista'''
        self.controllables.remove(controllable)
        
    def refresh(self):
        self.controllables.clear()
        _ins = self.ins.copy()
        self.ins.clear()
        for i in _ins:
            self.add_instrument(i)

    def add_instrument(self, instrument):
        ''' Añade un instrumento a la lista'''
        self.ins.append(instrument)
        cont = instrument.report_controllables()
        for c in cont:
            self.add_controllable(c)
        # TODO refresh gui
        # return len(self.ins) - 1
    
    def remove_instrument(self, instrument):
        ''' Elimina un instrumento de la lista'''
        self.ins.remove(instrument)
        cont = instrument.report_controllables()
        for c in cont:
            self.remove_controllable(c)
            # TODO eliminarlo de la accion?
        # TODO refresh gui 
            
    def add_knob_action(self, knob, controllable, action):
        ''' Añade una funcion a un knob'''
        # self.knob_actions[knob].add((controllable, action)) # ej: (env, "atk")
        self.knob_actions[knob].append((controllable, action)) # ej: (env, "atk")
        
    def remove_knob_action(self, knob, controllable, action):
        ''' Elimina una funcion de un knob'''
        self.knob_actions[knob].remove((controllable, action)) # ej: (env, "atk")

    def note_on(self, note, velocity=1):
        ''' Reproduce una nota MIDI'''
        for i in self.ins:
            i.note_on(note, velocity)
    
    def note_off(self, note):
        ''' Detiene una nota MIDI'''
        for i in self.ins:
            i.note_off(note)

    def play_knob(self, knob, value):
        ''' Reproduce un knob MIDI'''
        knob_act = self.knob_actions[knob]
        for c in knob_act:
            c[0].use_knob(value, c[1])
        # self.controllables[knob - 1][0].use_knob(value, self.controllables[knob - 1][1])

    