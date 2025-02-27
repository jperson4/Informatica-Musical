
CHUNK = 1024
SRATE = 48000
TIME = SRATE
TEST_TIME = SRATE*3

# notas = {
#     'C': 523.251,   # do
#     'D': 587.33,    # re
#     'E': 659.255,   # mi
#     'F': 698.456,   # fa
#     'G': 783.991,   # sol
#     'A': 880,       # la
#     'B': 987.767,   # si
#     'c': 1046.502,  # do
#     'd': 1174.659,  # re
#     'e': 1318.51,   # mi
#     'f': 1396.913,  # fa
#     'g': 1567.982,  # sol
#     'a': 1760,      # la
#     'b': 1975.533,  # si
# }

# mapeo de teclas del ordenador a notas en el piano
# utilizamos '.' para los sostenidos
teclas = "zsxdcvgbhnjmq2w3er5t6y7u"  # 2 de teclas filas 
notas =  "C.D.EF.G.A.Bc.d.ef.g.a.b"  # mapeadas a 2 octavas
# notas =  ""
#         octava baja||octava alta


# frecuencias de las notas asocidas a las teclas del teclado
# partimos del la=220Hz y generamos frecuencias de escala temperada
pitchs = [ 220*2.0**(i/12.0) for i in range(len(teclas))] 

# frecuencias asociadas a las notas midi de 0 a 127
# El LA central es la nota midi 70 y su frecuencia es 440
# contruimos hacia abajo y hacia arriba el resto de notas
freqsMidi = [ 440*2.0**(i/12.0) for i in range(-69,59)]


notasAJ = [440, 495,      550,    586.67, 660,    733.33, 825]
notasAT = [440, 493.88,   554.36, 587.33, 659.26, 739.99, 830.61]
# notasAJ = [440, 466.16, 495, 523.25, 550, 586.67, 622.25, 660, 698.46, 733.33, 825] #las negras estan inventadas
# notasAT = [440, 466.16, 493.88, 523.25, 554.36, 587.33, 622.25, 659.26, 698.46, 739.99, 830.61]

#array que guarda los tonos hasta la siguiente nota con nombre (sin #)
aqglthlsncn = [2, 0, 1, 2, 0, 2, 0, 1, 2, 0, 2, 0] # no se usa

def getdiatonic(n, notas=notasAJ): #TODO: va raro
    pos = n % 7
    oct = n // 7
    return notas[pos] * (2 ** oct)

def diatonicAcorde(n, notas=notasAJ):
    "Devuelve el acorde diatonico relacionado con la frecuencia dada"
    _n = n
    return [getdiatonic(n, notas), getdiatonic( n + 2, notas), getdiatonic(n + 4, notas)]

def timeToFrame(t): return round(t*SRATE)