from pyo import *

# constantes del sonido
CHUNK = 1024  # Número de muestras por buffer
SRATE = 44100  # Frecuencia de muestreo
AMP = 0.1 # Amplitud general del sonido
DEVICE_OUT = 20  # Dispositivo de audio a utilizar (puede cambiar según el sistema)
DEVICE_IN = 20 # Dispositivo de audio a utilizar (puede cambiar según el sistema)

def start_server():
    server = Server(nchnls=1)
    server.amp = AMP
    server.setSamplingRate(SRATE)
    server.setBufferSize(CHUNK)
    server.setInputDevice(DEVICE_IN) # & = default
    server.setOutputDevice(DEVICE_OUT) # & = default
    server.setNchnls(1)  # Número de canales de salida aparentemente solo vale 1
    server.boot()
    # server.start()
    return server

# Start audio server
s = Server().boot()
s.start()

# Simple MIDI note to frequency conversion
def midi_to_freq(note):
    return 440 * (2 ** ((note - 69) / 12.0))

# Create MIDI input
midi = Notein(poly=8, scale=1)

# Get pitch and velocity
pitch = midi['pitch']
velocity = midi['velocity']

# Convert pitch to frequency
freq = MToF(pitch)

# Map velocity (0–127) to amplitude (0–1)
amp = Sig(velocity / 127)

# Generate sine wave from MIDI input
sine = Sine(freq=freq, mul=amp * 0.3).out()

# Keep script running
print("Listening to MIDI input... Press Ctrl+C to stop.")

s.gui(locals())
