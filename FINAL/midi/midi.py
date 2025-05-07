import mido

class Midi:
    def __init__(self, instrument):
        self.func_notas = {i: self.play_note for i in range(48, 73)}

        #Asigna una funcion a cada knob
        self.func_knobs = {i: self.play_knob for i in range(0, 9)}

        #Junta los dos diccionarios en un diccionario principal
        self.midi_map = {**self.func_notas, **self.func_knobs}
    
    def play(self, note):
        """Reproduce una nota MIDI"""
        # print(f"Playing note: {note}")
        self.func_notas[note](note)

    def play_note(self, note, velocity):
        """Reproduce una nota del teclado MIDI"""
        print(f"Playing note: {note}")
        print(f"Velocity: {velocity}")
        # self.instrument.play(note)

    def play_knob(self, knob, value):
        """Reproduce un knob MIDI"""
        print(f"Playing knob: {knob}")
        print(f"Value: {value}")
        # self.instrument.play(knob)


