import numpy as np
from tkinter import *

from copy import deepcopy
import math

from synt.const import *
from synt.synt import *
from synt.osc import *
from synt.function import *
from synt.envolv import *
from synt.effects import *
from synt.instrumento import *
from synt.mixer import *

class Instrumento(Function):
    def __init__(self, synt, env, show=True, nombre='Instrumento'):
        super().__init__(show, nombre)
        # Creación de los osciladores
        # self.mixer = Mixer()
        self.synt = synt
        self.env = env
        # canales indexados por la nota de lanzamiento -> solo una nota del mismo valor
        self.channels = dict()        
        self.tails = dict()
        # self.afinacion = notasAJ

        self.octava = 4
        
        
    
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
        print(freq)
        synt = deepcopy(self.synt)
        # arreglar esta vaina
        self.env.reset()
        env = deepcopy(self.env)
        synt.setFreq(C(freq))
        synt.setEnv(env)
        self.channels[midiNote] = synt
        # self.channels[midiNote] = self.synt(midiNote, ondas = [osc.Sine()], env=EnvInstrumento(.01, .1, .7, .3)) #megasimple  
        
    def noteOff(self, midiNote):
        if midiNote in self.channels: # está el dict, release
            self.channels[midiNote].getEnv().noteOff()
            
    def change_octava(self, val):
        self.octava = int(val) - 2

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
            
    def doShow(self, tk, bg="#808090", side=LEFT):
        _tk = super().doShow(tk)
        if _tk is None:
            return None        
        # _tk = LabelFrame(_frame, text=self.nombre, bg="#808090")        
        slider_octava =Scale(_tk, from_=-1, to=10, resolution=1, orient=HORIZONTAL, label="Octava", command=self.change_octava, length=310)
        slider_octava.set(self.octava)
        slider_octava.pack()
        
        # una ventana de texto interactiva para poder lanzar notas con el teclado del ordenador
        text = Text(_tk,height=4,width=40)

        text.pack(side=TOP)
        text.bind('<KeyPress>', self.down)
        text.bind('<KeyRelease>', self.up) 
              
        self.synt.doShow(_tk, bg, side)
        self.env.doShow(_tk, bg, side)  
            
    # siguiente chunck del generador: sumamos señal de canales y hacemos limpia de silenciados
    def next(self, tiempo=None):
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
            fact = 1/math.sqrt(len(self.channels))
            out = out * fact
            # out = out /len(self.channels)
        return out