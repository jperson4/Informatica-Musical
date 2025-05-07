from audio import *
from pyo import *
from synt.nota import Nota

if __name__ == "__main__":
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
    
    
    # nota.play() # la activamos
    # pat2 = Pattern(nota.note_off, time=.5).stop()
    server.gui(locals())