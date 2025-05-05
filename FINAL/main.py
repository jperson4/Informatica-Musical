from audio import *
import sounddevice as sd
from pyo import *

if __name__ == "__main__":
    pa_list_devices()
    server = Server()
    server.amp = AMP
    server.setSamplingRate(SRATE)
    server.setBufferSize(CHUNK)
    server.setInputDevice(DEVICE_IN)
    server.setOutputDevice(DEVICE_OUT)
    server.boot()

    # seno
    a = Sine(440).out()
    # b = Sine(540).out()
    
    server.gui(locals())
    # server.start()