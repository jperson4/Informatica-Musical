
class Controllable:
    ''' Interfaz para los objetos que son controlables por un knob'''
    def __init__(self):
        pass
    
    def use_knob(self, value, action):
        '''Recibe el valor midi normalizado y la acción a realizar y la realiza'''
        pass
    
    def report_actions(self):
        '''Devuelve todos las acciones posibles de este objeto'''
        return []
    
    def report_controllables(self):
        '''Devuelve la lista de todos sus objetos que implementan esta interfaz'''
        return self