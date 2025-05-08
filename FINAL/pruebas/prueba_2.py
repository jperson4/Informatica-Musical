from pyo import *

CHUNK = 1024  # Número de muestras por buffer
SRATE = 44100  # Frecuencia de muestreo
AMP = 0.1 # Amplitud general del sonido
DEVICE_OUT = 6  # Dispositivo de audio a utilizar (puede cambiar según el sistema)
DEVICE_IN = 6  # Dispositivo de audio a utilizar (puede cambiar según el sistema)

def start_server():
    """Inicia el servidor de audio y lo configura."""
    server = Server(audio='alsa', nchnls=1)
    server.amp = AMP
    server.setSamplingRate(SRATE)
    server.setBufferSize(CHUNK)
    server.setInputDevice(DEVICE_IN) # & = default
    server.setOutputDevice(DEVICE_OUT) # & = default
    server.setNchnls(1)  # Número de canales de salida aparentemente solo vale 1
    server.boot()
    return server


s = start_server()
s.start()
a = Sine(440)
b = FM(carrier=200, ratio=[.5013,.4998], index=6, mul=.2)
mm = Mixer(outs=3, chnls=2, time=.025)
fx1 = Disto(mm[0], drive=.9, slope=.9, mul=.1).out()
fx2 = Freeverb(mm[1], size=.8, damp=.8, mul=.5).out()
fx3 = Harmonizer(mm[2], transpo=1, feedback=.75, mul=.5).out()
mm.addInput(0, a)
mm.addInput(1, b)
# mm.setAmp(0,0,.5)
# mm.setAmp(0,1,.5)
# mm.setAmp(1,2,.5)
# mm.setAmp(1,1,.5)

s.gui(locals())