from pyo import *
# # Constantes que tengan que ver con el audio

CHUNK = 1024  # Número de muestras por buffer
SRATE = 44100  # Frecuencia de muestreo
AMP = 0.1 # Amplitud general del sonido
DEVICE_OUT = 5  # Dispositivo de audio a utilizar (puede cambiar según el sistema)
DEVICE_IN = 5  # Dispositivo de audio a utilizar (puede cambiar según el sistema)

# input = None  # Variable para almacenar el objeto de entrada de audio

# '''REPRODUCTOR'''
# input = None

# def callback(outdata, frames, time, status):
#     global input
#     # print('entro')
#     if input is not None:
#         bloque = input.next()
#         # convertimos formato (CHUNK,) a (CHUNK,1) para que adecuarlo a sounddevice
#         outdata[:] = bloque.reshape(-1, 1)
#     else:
#         # si no hay datos, reproducimos silencio
#         outdata[:] = np.zeros((CHUNK, 1))

def start_server():
    """Inicia el servidor de audio y lo configura."""
    server = Server(nchnls=2)
    server.amp = AMP
    server.setSamplingRate(SRATE)
    server.setBufferSize(CHUNK)
    server.setInputDevice(DEVICE_IN)
    server.setOutputDevice(DEVICE_OUT)
    server.setNchnls(2)  # Número de canales de salida (2 para estéreo)
    server.boot()
    return server