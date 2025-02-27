import numpy as np
from tkinter import *

from copy import copy


from synt.const import *
from synt.synt import *
from synt.osc import *
from synt.function import *
from synt.envolv import *
from synt.effects import *
from synt.instrumento import *

class Instrumento:
    def __init__(self, tk:Tk, synt, env):
        # Creación de los osciladores

        self.synt = synt
        self.env = env
        # canales indexados por la nota de lanzamiento -> solo una nota del mismo valor
        self.channels = dict()        
        self.tails = dict()
        # self.afinacion = notasAJ

        self.octava = 4
        
        # interfaz
        frame = LabelFrame(tk, text="Sintetizador FM armónico", bg="#808090")
        frame.pack(side=LEFT)
        
        slider_octava =Scale(frame, from_=-1, to=10, resolution=1, orient=HORIZONTAL, label="Octava", command=self.change_octava, length=400)
        slider_octava.set(self.octava)
        slider_octava.pack()

        
        # una ventana de texto interactiva para poder lanzar notas con el teclado del ordenador
        text = Text(frame,height=4,width=40)

        text.pack(side=BOTTOM)
        text.bind('<KeyPress>', self.down)
        text.bind('<KeyRelease>', self.up)


    
    def noteOn(self,midiNote):
        # si está el dict de canales apagamos nota actual con envolvente de fadeout
        # y guardamos en tails. El next devolverá este tail y luego comenzará la nota
        if midiNote in self.channels:                   
            lastAmp = self.channels[midiNote].getEnv().getLast() # ultimo valor de la envolvente: inicio del fadeOut
            # signal = self.channels[midiNote].next()     # señal          
            # self.tails[midiNote] = signal           # diccionario de tails (notas apagadas) 

        # generamos un nuevo synth en un canal indexado con notaMidi
        # con los parámetros actuales del synth
        # if self.afinacion_box.get() == 'Ajustada' and self.afinacion != notasAJ:
        #     self.afinacion = notasAJ
        #     print('AJ')
        # elif (self.afinacion_box.get() == 'Atemperada' and self.afinacion != notasAT):
        #     print('AT')
        #     self.afinacion = notasAT
        
        freq= freqsMidi[midiNote] * 2 ** self.octava
        synt = copy(self.synt)
        env = copy(self.env)
        synt.setFreq(C(freq))
        synt.setEnv(env)
        self.channels[midiNote] = synt
        # self.channels[midiNote] = self.synt(midiNote, ondas = [osc.Sine()], env=EnvInstrumento(.01, .1, .7, .3)) #megasimple
        
        
    def noteOff(self, midiNote):
        if midiNote in self.channels: # está el dict, release
            self.channels[midiNote].getEnv().noteOff()
            
    def change_octava(self, val):
        self.octava = int(val) - 1


    # identificar y mandar reproducir la nota
    def down(self, event):
        c = event.keysym
        if c in teclas:
            midiNote = teclas.index(c) + 48
            print(f'noteOn {midiNote}')
            self.noteOn(midiNote)

    def up(self, event):
        c = event.keysym
        if c in teclas:
            midiNote = teclas.index(c) + 48# buscamos indice y hacemos el noteOff
            print(f'noteOff {midiNote}')
            self.noteOff(midiNote)
    # siguiente chunck del generador: sumamos señal de canales y hacemos limpia de silenciados
    def next(self):
        out = np.zeros(CHUNK)          
        for c in list(self.channels):            # convertimos las keys a lista para mantener la lista de claves original
            # print(self.channels[c].getEnv().state)
            if self.channels[c].getEnv().state == 'off':  # si no, modificamos diccionario en el bucle de recorrido de claves -> error 
                del self.channels[c]
            else: # si la nota está el diccionario de tails devolvemos el fadeout generado en noteOn y elminamos tail
                if c in self.tails:                  
                    out += self.tails[c]
                    del self.tails[c]
                else:
                    out += self.channels[c].next()
        # if out is list:       
            # out = out / np.max(out)
        if len(self.channels) > 0:
            # print(len(self.channels))
            out = out /len(self.channels)
        return out