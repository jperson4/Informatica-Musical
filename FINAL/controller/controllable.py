
class Controllable:
    ''' Interfaz para los objetos que son controlables por un knob'''
    def __init__(self):
        pass
    
    def use_knob(self, value, action):
        pass
    
    def report_actions(self):
        return []