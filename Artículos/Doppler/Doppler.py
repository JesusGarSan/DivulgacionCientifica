# ----------------------------------------------------------------------- IMPORTACIÓN DE LIBRERÍAS ------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colormaps



import streamlit as st
import streamlit.components.v1 as com

from PIL import Image

import os

from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.stoggle import stoggle
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_antd_components import *
# ----------------------------------------------------------------- CONFIGURACIÓN INICIAL DE LA PÁGINA -----------------------------------------------------------------

import setup_page
setup_page.setup_page()

#Cargamos los estilos css en la página
st.markdown('<style>' + open('./styles.css').read() + '</style>', unsafe_allow_html=True)





# ---------------------------------------------------------------------- CONTENIDO PROPIO DE LA PÁGINA ----------------------------------------------------------------------

#------------------------------------------------------------------------- DEFINICIÓN DE FUNCIONES ------------------------------------------------------------------------



# ----------------------------------------------------------------------------------- ARTÍCULO --------------------------------------------------------------------------


st.markdown(f"""
         <div>
         <style>
         </style>
         <h1>
         Cómo escuchar la velocidad
         </h1>
         </div>
         """, unsafe_allow_html=True)




column = st.columns(2)

column[0].markdown(r'''
_Estás a punto de cruzar la calle cuando escuchas una sirena acercándose. Te giras y ves que se trata de una ambulancia. Te detienes para dejarla pasar.
Entonces te asalta una pregunta: **¿qué le ha pasado a la sirena?**. Podrías jurar que se escuchaba distinta cuando la ambulancia se acercaba..._.
''')

column[0].markdown(r'''
Gracias a nuestro oído no es difícil saber cuando un coche se nos acerca. Lo escuchamos cada vez más intensamente cuando se nos acerca, y cada vez más levemente cuando se aleja.
Pero **el volumen no es la única forma de saber si algo se acerca o se aleja**.
Aun si crees no saber otra forma, es muy probable que incoscientemente la conozcas. ¿Lo comprobamos?

''')

img = Image.open("Galería/Imágenes/ambulancia.png")
img = img.resize((600,250))
column[1].image(img, use_column_width=True )





column[0].markdown('''**¡Ponte a prueba!**: A continuación podrás escuchar dos fragmentos de audio: uno de una ambulacia acercándose a la grabadora y otro alejándose de ella.
Hemos arreglado estos audios para que el volumen no cambie, así que tendrás que adivinarlo de otra manera:''')
column[0].markdown("¿Qué audio se corresponde con la ambulancia **:blue[_acercándose_]** al micrófono?:")

column_0 = column[0].columns(2)
column_1 = column[1].columns(2)

column_1[0].audio("Galería/Audio/sirena_acercandose.wav")
respuesta_correcta = column_1[0].button("Opción 1", use_container_width=True)
column_1[1].audio("Galería/Audio/sirena_alejandose.wav")
respuesta_incorrecta = column_1[1].button("Opción 2", use_container_width=True)

#from playsound import playsound
if respuesta_correcta: 
    column[0].markdown('**:green[¡Correcto!]** La pregunta entonces es: ¿Cómo lo has sabido?')
#    playsound('Artículos\Doppler\sound_1.mp3')     
if respuesta_incorrecta: 
    column[0].markdown('**:red[Incorrecto]**. ¡Pero no te preocupes! Algo me dice que al siguiente intento acertarás... ')
#    playsound("Artículos\Doppler\sound_2.mp3")     


st.divider()
#--------------------------------------------------------------------------------------------------------

#st.header('El efecto Doppler')

st.markdown(r'''
Al escuchar los audios te habrás dado cuenta de que una sirena sonaba más **aguda** y la otra más **grave**. Y esto es precisamente lo que nos permite distinguir entre una ambulancia acercándose y otra alejándose.
Resulta que:

''')
column = st.columns([.6, .4])
#column[1].image('Galería\GIFs\Doppler_1.gif')
column[0].markdown(r'''
- Cuando un **emisor** de sonido se nos :blue[**acerca**]  oímos el sonido que emite más :blue[**agudo**] que si estuviese quieto.
- Cuando un **emisor** de sonido se nos :red[**aleja**] oímos el sonido que emite más :red[**grave**] que si estuviese quieto.

Además:

- Cuanto mayor sea la **velocidad** a la que se acerque/aleje el emisor más agudo/grave se escuchará el sonido.
''')




st.markdown(r'''
Esto se debe a un fenómeno conocido como **"Efecto Doppler"**, y no solo lo podemos encontrar en sirenas de ambulancia.
El efecto Doppler es la base del funcionamiento de los radares de velocidad, el motivo por el que se producen **ondas de choque** y una de las formas que tenemos de saber cómo se mueven estrellas lejanas.
''')

st.markdown(r'''
¿Suena interesante? ¡Pues vamos a ver por qué de produce este efecto!
''')



st.divider()
# -----------------------------------------------------------

st.header('El sonido como vibración')
st.markdown(r'''
Para entender qué es el sonido es últil entender primero el medio por el que viaja. En este caso vamos a considerar el aire.
Podemos entender el **aire** como un **montón de partículas separadas** unas de otras sin ningún tipo de orden particular.

**El sonido se produce a partir de vibraciones**, aunque estas suelen ser demasiado pequeñas para verlas con nuestro ojo.
Cuando un objeto vibra se mueve de un lado a otro dentro de un rango de distancia.
Llamamos **oscilación** a cada uno de los movimientos de ida y vuelta de las vibraciones.

En cada oscilación, el objeto vibrante alterna "abalanzarse" contra las partículas de aire y "alejarse" de ellas.
Al abalanzarse empuja las partículas de aire, haciendo que se **compriman**, mientras que al alejarse hace que se separen entre sí.
Esta intermitencia de "empujones" provoca que las partículas de aire que toca el objeto empiecen también a oscilar.
Las partículas de aire oscilantes empujan su vez a las partículas de aire cercanas a ellas, **comprimiéndolas intermitentemente y haciendo que la oscilación se transmita a lo largo del aire**.
''')

column = st.columns(3)
column[0].image('Galería/GIFs/Partículas Libres.gif')
column[0].markdown('*Particulas de aire viajando libremente*')
column[1].image('Galería/GIFs/Lámina en vacío.gif')
column[1].markdown('*Lámina vibrando en el vacío*')
column[2].markdown('*Lámina vibrando en el aire y propagando la vibración*')

with st.expander('Un detalle clave: **oscilar** _vs._ **desplazar**'):
    column = st.columns(2)
    column[0].markdown("""
    Un detalle a tener en cuenta es que **lo que se propaga con la vibración de un objeto  NO es el aire**.
    Lo que se propaga son las propias oscilaciones. Cada una de las partículas de aire involucradas oscilan entorno a un mismo punto, no viajan del objeto a nuestro oído
    Fíjate en las partículas resaltadas de :red[rojo] en la siguiente animación:
    """)
    column[1].image('./Galería/GIFs/animacion_onda.gif')

    column[0].markdown("""Dicho de otra manera: Cuando una escuchamos a una persona hablar *el aire que sale de su boca NO está llegando a nuestro oído.""")



st.markdown(r'''
Nuestro oído es capaz de detectar las compresiones de aire que llegan hasta él, dándonos la habilidad de oir.
''')


column = st.columns([.65, .35])


column[0].markdown(r'''
Entender el sonido como compresiones de aire que viajan por el aire nos permite introducir el concepto de **frecuencia** del sonido. 
La frecuencia responde a la pregunta: _¿Cuántas compresiones llegan a mi oído cada segundo?_

- Si las compresiones están muy cerca unas de otras nos llegarán **muchas compresiones en un segundo**: **:blue[alta frecuencia]**.
Los sonidos de alta frecuencia son **:blue[agudos]**.

- Si las compresiones están muy alejadas unas de otras nos llegarán **pocas compresiones en un segundo**: **:red[baja frecuencia]**.
Los sonidos de baja frecuencia son **:red[graves]**.



''')

column[1].write('*ejemplo frecuencia alta*')
column[1].write('*ejemplo frecuencia baja*')

st.divider()



st.header('El efecto Doppler')


import sys
sys.path.insert(0, 'Simulaciones/Doppler/')
from Doppler_functions import *
dim_x = 2000 /40 
dim_y = 600 /40 

escala = 1/40
escala_velocidad = 10

parametros = {
    "velocidad_emisor": 0,
    "velocidad_receptor": 0,
    "posicion_inicial_emisor_x": -15,
    "posicion_inicial_emisor_y": 0,
    "posicion_inicial_receptor_x": 15,
    "posicion_inicial_receptor_y": 0,
    "intervalo_emision": 5,
    "n_frames": 40,
    "velocidad_animacion": 50,
    "velocidad_sonido": 340,
    "velocidad_propagacion": 340/escala_velocidad * escala,
    "escala_velocidad": escala_velocidad,
    'escala': escala,
    "radio_inicial": (dim_x/2) * escala,
    "f_emisor": 100,
    "f_receptor": None,
}


escala_figura =  .13


column = st.columns([0.55, 0.45])
with column[1]:
    index = buttons(['Emisor inmóvil', 'Emisor en movimiento', 'Emisor en movimiento (rápido)'], return_index=True, grow=True)
    if index == 0:
        parametros['velocidad_emisor'] = 0.0
        parametros['posicion_inicial_emisor_x'] = 0.0
    if index == 1:
        parametros['velocidad_emisor'] = 15.0
        parametros['posicion_inicial_emisor_x'] = -10.0
        parametros['posicion_inicial_receptor_x'] = 0.0
    if index == 2:
        parametros['velocidad_emisor'] = 25.0
        parametros['posicion_inicial_emisor_x'] = -15.0
        parametros['posicion_inicial_receptor_x'] = 0.0

    parametros['velocidad_emisor'] = st.number_input('Velocidad emisor (m/s)', value= float(parametros['velocidad_emisor']), min_value=-100.0, max_value=+100.0, step= 1.0,
                                    help='Para ayudar a la visualización esta simulación considera una velocidad del sonido de 34 m/s (reducción de factor 10 respecto al valor real).')
    parametros['velocidad_emisor'] *= escala
column[0].markdown(r'''
Ahora que comprendemos mejor la naturaleza del sonido y qué es la frecuencia tenemos todas las piezas para comprender el Efecto Doppler.
Al aprender sobre la frecuencia hemos visto los sonidos en los que las compresiones del aire están cerca entre sí son agudos, y los que tienen las compresiones (más) separadas son (más) graves.
''')
column[0].markdown('En la animación **[Emisor inmóvil]** de la derecha podemos ver una fuente emisora emitiendo sonido. Las circunferencias azules representan las compresiones de aire')

    

#column[1].subheader('Emisor inmóvil')
#column[1].image('Artículos/Doppler/emisión estática.gif')

column[0].markdown(r'''
Si en lugar de mantener la fuente emisora quieta la hacemos moverse **[Emisor en movimiento]** sucede algo curioso:
- La separación entre compresiones se reduce en las regiones hacia las que se **:blue[acerca]** el emisor. $\rightarrow$ **:blue[Aumenta la frecuencia]**

- La separación entre compresiones aumenta en las regiones de las que se **:red[aleja]** el emisor. $\rightarrow$ **:red[Disminuye la frecuencia]**

Por tanto: escuchamos el sonido emitido de forma más aguda cuando el emisor se nos acerca y de forma más grave cuando se aleja de nosotros.
''')
#column[1].subheader('Emisor en movimiento')
#column[1].image('Artículos\Doppler\emisión dinámica.gif')

# ---------- ANIMACIÓN INTERACTIVA DE DOPPLER ---------------

with column[1]:
    with st.spinner('Creando animación...'):
        crear_animación(parametros, dim_x, dim_y, escala_figura, height=300, width = 1100)


st.markdown(r'''
Este  efecto se hace más grande cuanto mayor es la velocidad del emisor **[Emisor en movimiento (rápido)]** .
Por eso es fácil que hayas experimentado este efecto con sirenas de ambulancia, pero no con gente que te habla mientras se acerca o aleja de ti.
''')


#column = st.columns(2)
#column[0].subheader('Emisión a alta velocidad')
#column[0].image('Artículos\Doppler\emisión rápida.gif')
#column[1].subheader('Emisión a baja velocidad')
#column[1].image('Artículos\Doppler\emisión lenta.gif')

st.divider()
#--------------------------------------------------------------------------------------------------------

st.header('Para saber más')

column = st.columns(2)
with column[0].expander('**¿Y si es el receptor el que se mueve?**'):
    st.markdown(r'''
    El **efecto Doppler** no sólo sucede cuando el emisor de sonido se mueve. También **se manifiesta cuando el receptor se mueve**.
    - Si el receptor se **:blue[acerca]** al emisor, se encontrará con más compresiones cada segundo, **:blue[aumentando la frecuencia]**.
    - Si el receptor se **:red[aleja]** del emisor, se encontrará con menos compresiones cada segundo, **:red[reduciendo la frecuencia]**.

    Si tanto el receptor como el emisor se mueven, **ambos movimientos contribuyen al efecto**.
    
    ''')

with column[0].expander('**Cómo calcular el efecto Doppler**'):
    st.markdown(r'''
    Podemos calcular la frecuencia a la que "se oye" un sonido afectado por el efecto Doppler mediante la siguiente ecuación:
    ''')
    st.latex(r'''
    f_{r} = \frac{v - v_r}{v - v_e}  f_e
    ''')

    st.markdown(r'''
    Donde:                                      
    $f_{r}$ es la frecuencia del sonido recibido            
    $f_{e}$ es la frecuencia del sonido emitido             
    $v$ es la velocidad del sonido              
    $v_r$ es la velocidad del receptor (>0 si se aleja del emisor)   
    $v_e$ es la velocidad del emisor (>0 si se acerca al receptor)
    ''')


with column[1].expander('**Las ondas de choque**'):
    st.markdown(r'''
    Si la fuente emisora es igual de rápida que el propio sonido se produce el fenómeno de las ondas de choque.
    Cuando esto sucede, cada una de las nuevas emisiones de la fuente se suma a las anteriores, haciendo que todas las emisiones viajen juntas como una enorme compresión del aire.
    ''')
    parametros['velocidad_emisor'] = parametros['velocidad_sonido']
    parametros['posicion_inicial_emisor_x'] = -20.0
    parametros['posicion_inicial_receptor_x'] = 50.0
    st.image('Galería/GIFs/onda choque.gif')
    st.markdown(r'''
    Es difícill mantener _exactamente_ la misma velocidad que el sonido, por lo que este fenómeno suele observarse en aviones capaces de **superar** la velocidad del sonido en el instante en el que la igualan.
    Esto es lo que comunmente se llama **"Romper la barrera del sonido"**.
                
    Cuando la velocidad del emisor es **superior** a la del sonido, las compresiones del aire se suman formando un cono. La compresión en este cono (suma de compresiones de cada vibración) puede hacerse muy grande.
                ¡Tanto como para **provocar la condensación del vapor de agua** que se encuentra!, creando así nubes con forma de cono:
    
                ''')
    columns = st.columns([0.66, 0.34])
    columns[0].image('Galería/GIFs/onda supersónica.gif')
    columns[1].image('Galería/Imágenes/avión match.jpg', use_column_width=True)

#--------------------------------------------------------------------------------------------------------

st.header('Juega con el Efecto Doppler')

column = st.columns(2)
column[0].markdown(r'''
Entre los simuladores de la web podrás encontrar uno dedicado al Efecto Doppler.
Además de poder crear tus propias animaciones **podrás subir tus propios audios para simular cómo se escucharían al someterse al efecto Doppler**.
Pásate a jugar con él: 
''')

#img = Image.open("Galería/Imágenes/" + 'Doppler.png')
#img = img.resize((600,300))
#column[1].image(img, use_column_width=True )
#
#with column[1]:
#    add_vertical_space(2)
if column[1].button('Simulador: Efecto Doppler', use_container_width=True):
    switch_page('Efecto Doppler')



# --------------------------------------------------------------------------- CUESTIONARIO -------------------------------------------------------------------------------
#st.divider()
import sys
sys.path.insert(0, 'Artículos/Cuestionario/')

import cuestionario
cuestionario.mostrar_cuestionario()

# ----------------------------------------------------------------------------- FOOTER ----------------------------------------------------------------------------------

