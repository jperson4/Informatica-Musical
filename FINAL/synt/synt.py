from pyo import *

class Synth(PyoObject):
    ''' Recibe un oscilador y una envolvente
        en note_on crea una copia del oscilador y la hace sonar
        en note_off dice a la envolvente que empiece a decaer, cuando decaiga, se eliminara la copia del oscilador aunque
        
        todos los osciladores suenan porque se meten en el mixer cuando los creamos
        (cuando se apagan, los sacamos del mixer)
    '''

    def __init__(self, osc, env, transpo=1, amp=1):
        ''' Reproduce notas'''
        super().__init__()
        self.transpo = Sig(transpo)
        self.osc = osc
        self.env = env
        self.amp = Sig(amp) # CHECK

        self.playingNotes = {}
        self.decayingNotes = {}
        
        self.mixer = Mixer(1, chnls=1, initsize=0, mul=0.5) # mixer para mezclar las notas
        # cuando toquemos una nota, la añadimos al mixer
        
    def note_on(self, id, velocity=1):
        ''' Crea una copia del oscilador y las pone a sonar añadiendolas al mixer'''
        freq = idToFreq[id] * self.transpo
        _id = id * self.transpo
        _osc = copy(self.osc)
        _env = copy(self.env)
        _osc.setFreq(freq) # de forma que puedas dejar el oscilador 
        _osc.setMul(_osc.mul * velocity * self.amp)
        TrigFunc(_env["trig"], lambda: self.remove_decaying(_id)) # cuando acabe la envolvente, elimina la nota
        self.playingNotes[_id] = (_osc, _env)
        self.mixer.addInput(_id, _osc)
        
    def note_off(self, id):
        ''' Saca la nota de playing u la añade a decaying, activa el decay de la envolvente'''
        _id = id * self.transpo
        if _id in self.playingNotes:
            self.decayingNotes[_id] = self.playingNotes[_id]
            self.decayingNotes[_id][1].stop() # activa el decay de la envolvente
            self.playingNotes.remove(_id)
            
    def remove_decaying(self, id):
        ''' Elimina las notas que ya han terminado de decaer y ya no estan sonando'''
        self.decayingNotes[id][0].stop() # para la nota del todo
        self.mixer.delInput(id)
        del self.decayingNotes[id]
                
    def out(self):
        "Sends the synth's signal to the audio output and return the object itself."
        # self.notch.out()
        return PyoObject.out(self)

    def sig(self): # puede que no sea necesario
        "Returns the synth's signal for future processing."
        return self.notch