import mido

class Midi:
    def __init__(self, controller):
        self.controller = controller
        self.func_notas = {i: self.note_on for i in range(48, 73)}

        #Asigna una funcion a cada knob
        self.func_knobs = {i: self.play_knob for i in range(0, 9)}

        #Junta los dos diccionarios en un diccionario principal
        self.midi_map = {**self.func_notas, **self.func_knobs}
    
    def play(self, note):
        """Reproduce una nota MIDI"""
        # print(f"Playing note: {note}")
        self.func_notas[note](note)

    def note_on(self, note, velocity):
        """Reproduce una nota del teclado MIDI"""
        print(f"Playing note: {note}")
        print(f"Velocity: {velocity}")
        self.controller.note_on(note, velocity)

    def note_off(self, note, velocity):
        """Detiene una nota del teclado MIDI"""
        print(f"Stopping note: {note}")
        print(f"Velocity: {velocity}")
        self.controller.note_off(note)

    def play_knob(self, knob, value):
        """Reproduce un knob MIDI"""
        print(f"Playing knob: {knob}")
        print(f"Value: {value}")
        self.controller.play_knob(knob, value)

