from audio import *
from pyo import *
import mido
from synt.nota import Nota
from midi.midi import Midi
from instrument.instrument import Instrument
import threading

# hilo listener del midi
def midi_listener():
    input_ports = mido.get_input_names()
    mpk_port = next((port for port in input_ports if "MPK Mini" in port), None)
    midi = Midi(ins)
    with mido.open_input(mpk_port) as inport:  
        for msg in inport:
            if msg.type == 'note_on':
                # midi = Midi(ins)
                midi.note_on(msg.note, msg.velocity)
            elif msg.type == 'note_off':
                ''' midi = Midi(ins) ''' 
                midi.note_off(msg.note, msg.velocity)
            elif msg.type == 'control_change':
                # midi = Midi(ins)
                midi.play_knob(msg.control, msg.value)

ins = None

if __name__ == "__main__":
    # Leer de los puertos MIDI disponibles y enontrar el MPK Mini
    # input_ports = mido.get_input_names()

    server = start_server()
    env = Adsr()
    ins = Instrument() # creamos un instrumento que vaya sonando
    ins.out()

    midi_thread = threading.Thread(target=midi_listener, daemon=True)
    midi_thread.start()
    

    
    # nota.play() # la activamos
    # pat2 = Pattern(nota.note_off, time=.5).stop()
    server.gui(locals())
    midi_thread.join()
