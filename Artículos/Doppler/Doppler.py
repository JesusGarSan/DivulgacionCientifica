# ----------------------------------------------------------------------- IMPORTACIÓN DE LIBRERÍAS ------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colormaps



import streamlit as st
import streamlit.components.v1 as com

from PIL import Image

import os
from streamlit_extras.stoggle import stoggle
from streamlit_extras.add_vertical_space import add_vertical_space

# ----------------------------------------------------------------- CONFIGURACIÓN INICIAL DE LA PÁGINA -----------------------------------------------------------------
# Configuración ancha de la página
st.set_page_config(layout='wide')


# Escondemos las masrcas de agua y menú hamburguesa
#hide_st_style = """
#                <style>
#                #mainMenu {visibility: hidden;}
#                footer {visibility: hidden;}
#                header {visibility: hidden;}
#                </style>
#"""
#st.markdown(hide_st_style, unsafe_allow_html=True)


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

#column[0].image('Artículos/Refracción/charco.png')

column[0].markdown('''Nuestra experiencia en el mundo nos hace tener respuestas intuitivas incluso en cosas que no necesariamente entendemos.
                    Estas intuiciones tienen normalmente trasfondos interesantes. 
                    ''')           

column[0].markdown('''Un ejemplo de esto es nuestra capacidad de saber si un objeto se acerca o se aleja de nosotros según el sonido que escuchamos de él. En este artículo indagaremos en este fenómeno.
                    Entenderemos a qué se debe y, ya puestos, **aprenderemos cómo romper la barrera del sonido**.''')

column[0].markdown('''Pero antes de nada, veámos si cuentas con esta capacidad: ''')

img = Image.open("Galería/Imágenes/ambulancia.png")
img = img.resize((600,350))
column[1].image(img, use_column_width=True )

column[0].markdown('**¡Ponte a prueba!**: A continuación podrás escuchar la sirena de dos ambulancias. Una de ellas se grabó mientras la ambulancia se acercaba al micrófono, y la otra mientras se alejaba.')
column[0].markdown("¿Qué audio se corresponde con la ambulancia **:red[_acercándose_]** al micrófono?:")

column_0 = column[0].columns(2)

column_0[0].audio("Galería/Audio/sirena_acercandose.wav")
respuesta_correcta = column_0[0].button("Opción 1", use_container_width=True)
column_0[1].audio("Galería/Audio/sirena_alejandose.wav")
respuesta_incorrecta = column_0[1].button("Opción 2", use_container_width=True)

if respuesta_correcta: 
    column[0].markdown('**:green[¡Correcto!]** La pregunta entonces es: ¿Cómo podemos saber algo así sólo escuchando la sirena de la ambulancia?')
if respuesta_incorrecta: 
    column[0].markdown('**:red[Incorrecto]**. ¡Pero no te preocupes! Algo me dice que al siguiente intento acertarás... ')

st.divider()
#--------------------------------------------------------------------------------------------------------


st.header('El sonido como onda')
st.markdown('Tal vez hayas escuchado alguna vez que **el sonido es una onda**. Pero ¿qué es siquiera una onda?. Vamos a proponer la definición más general de "_Onda_". No te preocupes si no la entiendes, que vamos a ir explicándola poco a poco')
st.markdown('<h4 style="text-align: center">Una <u>onda</u> es una <i>propagación</i> de una <i>perturbación</i>  de una <i>propiedad del espacio</i> </body>', unsafe_allow_html=True)


st.header('El efecto Doppler')
column = st.columns(2)

with column[0].expander("**Efecto Doppler**"):
    st.markdown(r'''  ''')
    st.latex(r'''
    f_{r} = \frac{v - v_r}{v - v_e} \cdot f_e
    ''')


st.divider()
#--------------------------------------------------------------------------------------------------------

st.header('Rompiendo la barrera del Sonido')


st.divider()
#--------------------------------------------------------------------------------------------------------



st.markdown('')

st.markdown('')









# --------------------------------------------------------------------------- CUESTIONARIO -------------------------------------------------------------------------------
#st.divider()
import sys
sys.path.insert(0, 'Artículos/Cuestionario/')

import cuestionario
cuestionario.mostrar_cuestionario()

# ----------------------------------------------------------------------------- FOOTER ----------------------------------------------------------------------------------

