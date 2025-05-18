from tools import *
from pyo import *
import mido
from midi.midi import Midi
from audio.instrument import Instrument
from audio.synt import Synt
from controller.controller import Controller
from factory import Factory
from audio.env import cAdsr
import threading

# hilo listener del midi
def midi_listener():
    input_ports = mido.get_input_names()
    mpk_port = next((port for port in input_ports if "MPK Mini" in port), None)
    midi = Midi(controller)
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
controller = None

if __name__ == "__main__":
    # Leer de los puertos MIDI disponibles y encontrar el MPK Mini
    server = start_server()
    controller = Controller()
    factory = Factory(controller)
    
    """ esto se deberia hacer en la interfaz de factory"""
    env = cAdsr()
    synts = [Synt(HarmTable([1, 0, .7, 0, .5, 0, .3]))]
    ins = Instrument(env, synts, "ins1")  # creamos un instrumento que vaya sonando
    # controller.add_instrument(ins)  # lo añadimos al controlador BRUTO
    factory.add_instrument(ins)
    
    """ esto se deberia hacer en la interfaz de controller """
    # controller.add_knob_action()
    controller.add_knob_action(0, env, "atk")
    controller.add_knob_action(1, env, "dec")
    controller.add_knob_action(2, env, "sus")
    controller.add_knob_action(3, env, "rel")

    # ins.out()
    

    # Crear controlables para cada valor de ADSR y asignarlos al controlador

    """aqui habria que hacer un hilo para la gui del controller y otro para la factory"""

    midi_thread = threading.Thread(target=midi_listener, daemon=True)
    midi_thread.start()
    
    server.gui(locals())
    midi_thread.join()
