import mido

#Asigna el puerto de entrada MIDI para el teclado
func_notas = {i: play_note for i in range(48, 73)}

#Asigna una funcion a cada knob
func_knobs = {
    1: knob_one,
    2: knob_two,
    3: knob_three,
    4: knob_four,
    5: knob_five,
    6: knob_six,
    7: knob_seven,
    8: knob_eight,
}

midi_map = {**func_notas, **func_knobs}

