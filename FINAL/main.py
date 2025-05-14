from tools import *
from pyo import *
import mido
from midi.midi import Midi
from audio.instrument import Instrument
from controller.controller import Controller
from audio.env import cAdsr
import threading

# hilo listener del midi
def midi_listener():
    input_ports = mido.get_input_names()
    mpk_port = next((port for port in input_ports if "MPK Mini" in port), None)
    midi = Midi(c)
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
c = None

if __name__ == "__main__":
    # Leer de los puertos MIDI disponibles y encontrar el MPK Mini
    server = start_server()
    c = Controller()
    env = cAdsr()
    ins = Instrument(env, "ins1")  # creamos un instrumento que vaya sonando
    c.add_instrument(ins)  # lo añadimos al controlador BRUTO
    """Meter los 4 elementos de adsr en el controlador FUERZA BRUTA grr"""
    c.add_controllable((env, "atk"))
    c.add_controllable((env, "dec"))
    c.add_controllable((env, "sus"))
    c.add_controllable((env, "rel"))

    ins.out()

    # Crear controlables para cada valor de ADSR y asignarlos al controlador


    midi_thread = threading.Thread(target=midi_listener, daemon=True)
    midi_thread.start()
    
    server.gui(locals())
    midi_thread.join()
