from pyo import *
import numpy as np

s = Server().boot()

# Get the length of an audio block.
bs = s.getBufferSize()

# Create a table of length `buffer size` and read it in loop.
t = DataTable(size=bs)
osc = TableRead(t, freq=t.getRate(), loop=True, mul=0.1).out()

# Share the table's memory with a numpy array. 
arr = np.asarray(t.getBuffer()) # esto puede ser la clave para poder usar sounddevice
# la vaina es q puede que sea mega lento


def process():
    "Fill the array (so the table) with white noise."
    arr[:] = np.random.normal(0.0, 0.5, size=bs)


# Register the `process` function to be called at the beginning
# of every processing loop.
s.setCallback(process) 

s.gui(locals())