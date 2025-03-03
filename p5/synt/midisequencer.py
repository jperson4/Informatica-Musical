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
import mido


class MidiSequencerTk:
    # análogo a lo anterior
    def __init__(self,tk,instruments=None):
        if instruments == None:
            env = EnvInstrumento(.1, .1, .7, .3)
            synt = Synt(C(1), Sine(C(1)))
            self.instruments = [Instrumento(tk, synt, env)]            
        else:
            self.instruments = instruments

        frame = LabelFrame(tk, text="Midi Sequencer", bg="#908060")
        frame.pack(side=TOP)

        frameFile = Frame(frame, highlightbackground="blue", highlightthickness=6)
        frameFile.pack(side=TOP)
        Label(frameFile,text='Archivo MIDI: ').pack(side=LEFT)
 
        self.file = Entry(frameFile) #.pack(side=RIGHT)
        self.file.insert(14,"pirates.mid")
        self.file.pack(side=LEFT)

        self.transport = 0
        
        for i in self.instruments:
            i.doShow(frame)
        
        self.text = Text(frame,height=6,width=23)
        self.text.pack(side=RIGHT)
        playBut = Button(frame,text="Play", command=self.play)
        playBut.pack(side=TOP)
        stopBut = Button(frame,text="Stop", command=self.stop)
        stopBut.pack(side=BOTTOM)

        self.tick = 1
        self.state = 'off'
        
    # obtención de la secuencia midi (noteOn/Off) con tiempos relativos al inicio
    def getSeq(self,midiEvents):
        seq = []
        accTime = 0
        for m in midiEvents:
            accTime += m.time
            if m.type=='note_on':
                if m.velocity==0: seq.append((accTime,'noteOff',m.note+self.transport,m.channel))
                else: seq.append((accTime,'noteOn',m.note+self.transport,m.channel))    
            elif m.type=='note_off':
                seq.append((accTime,'noteOff',m.note+self.transport,m.channel))
        return seq

  
    def play(self):
        events = mido.MidiFile(self.file.get())
        seq = self.getSeq(events)
        print(seq)

        self.state = 'on'
        self.playLoop(seq)

    def playLoop(self,seq,item=0,accTime=0):   
        if item>=len(seq) or self.state =='off':
            return

        # ahora tenemos que procesar todos los ítems cuyo tiempo supere el crono accTime    
        while item<len(seq) and accTime>=seq[item][0]:
            (_,msg,midiNote,_chan) = seq[item]  # (time,'noteOff',midNote,channel)
            self.text.insert('6.0',  f'{msg} {midiNote} {_chan}\n') 
            if msg=='noteOn':  
                self.instruments[_chan % len(self.instruments)].noteOn(midiNote)                   
            else: # msg noteOff    
                self.instruments[_chan % len(self.instruments)].noteOff(midiNote)                   
            item += 1 # y avanzmos ítem

        # avanzammos crono 
        accTime += self.tick/1000

        self.text.after(self.tick,lambda: self.playLoop(seq,item,accTime)) 

         
    def stop(self):
        self.instruments.stop()
        self.state = 'off'   
