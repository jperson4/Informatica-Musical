from pyo import *
from synt.nota import Nota

class Instrument(PyoObject):
    def __init__(self, osc, env, amp=1):
        ''' Instrumento que reproduce notas con un oscilador y una envolvente'''
        PyoObject.__init__(self)
        self.osc = osc
        self.env = env
        self.amp = amp
        self._base_objs = self.osc.getBaseObjects()

    def play_note(self, note):
        ''' Reproduce una nota MIDI'''
        nota = Nota(440.0 * (2 ** ((note - 69) / 12.0)), Sine(440.0 * (2 ** ((note - 69) / 12.0))), self.env) # creamos una nota que vaya sonando
        nota.out() # la enviamos a la salida de audio
        time.sleep(2)
        nota.note_off() # la desactivamos

    def play_knob(self, knob):
        ''' Reproduce un knob MIDI'''
        print(f"Playing knob: {knob}")
        # Aqui se puede añadir la funcionalidad de los knobs