from audio import *
from pyo import *
import mido
from synt.nota import Nota
from midi.midi import Midi

if __name__ == "__main__":
    # Leer de los puertos MIDI disponibles y enontrar el MPK Mini
    input_ports = mido.get_input_names()
    mpk_port = next((port for port in input_ports if "MPK Mini" in port), None)

    server = start_server()
    server.start()
    env = Adsr(attack=1, decay=1, sustain=.4, release=2)
    # env = Sig(1)
    nota = Nota(440, Sine(440), env) # creamos una nota que vaya sonando
    nota.out() # la enviamos a la salida de audio
    # nota.play() # la activamos
    # pat1 = Pattern(nota.play, time=0.5).play()
    time.sleep(2)
    nota.note_off() # la desactivamos
    

    with mido.open_input(mpk_port) as inport:
        for msg in inport:
            if msg.type == 'note_on' or msg.type == 'note_off':
                midi = Midi(nota)
                midi.play_note(msg.note, msg.velocity)
            elif msg.type == 'control_change':
                midi = Midi(nota)
                midi.play_knob(msg.control, msg.value)

    
    # nota.play() # la activamos
    # pat2 = Pattern(nota.note_off, time=.5).stop()
    server.gui(locals())