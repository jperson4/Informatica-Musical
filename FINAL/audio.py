# Constantes que tengan que ver con el audio

CHUNK = 1024  # Número de muestras por buffer
SRATE = 48000  # Frecuencia de muestreo

input = None  # Variable para almacenar el objeto de entrada de audio

'''REPRODUCTOR'''
input = None

def callback(outdata, frames, time, status):
    global input
    # print('entro')
    if input is not None:
        bloque = input.next()
        # convertimos formato (CHUNK,) a (CHUNK,1) para que adecuarlo a sounddevice
        outdata[:] = bloque.reshape(-1, 1)
    else:
        # si no hay datos, reproducimos silencio
        outdata[:] = np.zeros((CHUNK, 1))
