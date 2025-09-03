Práticas de python de la asignatura Informátrica Musical
Se trataba de hacer un sintetizador.

Nosotros desarrollamos esta arquitectura inspirandonos en la programacion funcional. De esta forma conseguíamos un sintetizador en el cual todo se podía modular ininitamente y se podían sumar y restar ondas con toral libertad.
Por ejemplo, se puede crear una onda a 440Hz
```
o = Sine(freq = 440)
```
y acontinuación modularla en amplitud con otra onda a 60Hz
``` 
o = o * Sine(freq = 60)

# tambien valdría 
o = Sine(freq = 440, amp = Sine(freq = 60))
```
de esta forma podríamos estar sumando, restando, modulando en amplitud y en frecuencia de forma indefinida. 

El rendimiento es bastante bueno ya que no usamos bucles en python si no que empleamos los arrays de numpy.

Más adelante añadimos envolventes, filtros y control por MIDI.

Para la práctica final de la asignatura, conectamos un sintetizador (parecido al nuestro pero hecho usando la librería pyo) a un teclado MIDI 
