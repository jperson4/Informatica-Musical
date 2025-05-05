from pyo import *
from audio import *

pa_list_devices() # muestra los dispositivos de audio disponibles
# pa_get_default_devices_from_host("alsa")
# print(pa_get_input_max_channels(DEVICE_OUT))


s = start_server() # inicia el servidor de audio
freq = Sig(440)
a = Sine(freq).out() # crea un oscilador de seno a 440 Hz
s.gui(locals()) # abre la interfaz gráfica del servidor
