from audio import *
import sounddevice as sd

if __name__ == "__main__":
    # Iniciar hilo de sonido
    input = None
    stream = sd.OutputStream(samplerate=SRATE, channels=2, callback=callback, blocksize=CHUNK)
    stream.start()
    
    