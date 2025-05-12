from pyo import *

s = Server().boot()

tritab = TriangleTable(order=50).normalize()
lookup = Osc(table=tritab, interp=2, freq=500, mul=.2)

sawtab = SawTable(order=50).normalize()
saw_osc = Osc(table=sawtab, interp=2, freq=500, mul=.2)

# Mix the two oscillators together into a single signal
mixed_signal = lookup + saw_osc

# Output the mixed signal
mix = Mix(mixed_signal, voices=2).out()

sc = Scope(mixed_signal, gain=1)

s.gui(locals())