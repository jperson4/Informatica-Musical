from audio import *
from pyo import *
from synt.nota import Nota

if __name__ == "__main__":
    server = start_server()
    server.start()
    nota = Nota(440, Sine(440))
    nota.out()  
    # nota.play()
    # time.sleep(1)
    # nota.stop()
    # time.sleep(1)
    server.gui(locals())