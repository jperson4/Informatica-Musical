from pyo import *

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
