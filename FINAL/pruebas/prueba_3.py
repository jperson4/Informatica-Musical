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
    server.setMidiInputDevice(99)  # Open all input devices.
    server.setNchnls(1)  # Número de canales de salida aparentemente solo vale 1
    server.boot()
    return server


s = start_server()
s.start()

# Automatically converts MIDI pitches to frequencies in Hz.
notes = Notein(scale=1)
# notes.keyboard()

# MIDI-triggered ADSR envelope.
env1 = MidiAdsr(notes["velocity"], attack=0.005, decay=0.1, sustain=0.7, release=0.5, mul=0.1)

# MIDI-triggered DADSR envelope (a classic ADSR with an adjustable pre-delay).
env2 = MidiDelAdsr(notes["velocity"], delay=0.5, attack=1, decay=0.5, sustain=0.5, release=0.5, mul=0.1)

# Root frequency appears instantly.
sig1 = Sine(freq=notes["pitch"], mul=env1).out()

# Small frequency deviations appear smoothly after a half-second delay.
# sig2 = RCOsc(freq=notes["pitch"] * 0.992, sharp=0.8, mul=env2).mix()
# sig3 = RCOsc(freq=notes["pitch"] * 1.008, sharp=0.8, mul=env2).mix()


# Create a stereo signal from the frequency deviations.
# stereo = Mix([sig2, sig3], voices=2)

# Sum the signals and apply a global reverberation.
# rev = WGVerb(sig1, feedback=0.8, cutoff=5000, bal=0.3).out()

s.gui(locals())