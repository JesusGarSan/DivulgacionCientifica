# ----------------------------------------------------------------------- IMPORTACIÓN DE LIBRERÍAS ------------------------------------------------------------------------

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import HTML
import numpy as np


import streamlit as st
import streamlit.components.v1 as com

import os

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


# Cargamos los estilos css
#with open('styles.css') as styles:
#    design = styles.read()

from st_pages import Page, Section, show_pages, show_pages_from_config, add_page_title

#show_pages(
#    [
#        Page("DC.py", "Home", "🏠"),
#        Page("Artículos/Artículos.py","Artículos", icon="📎"),
#        Page("Artículos/Refracción/Refracción.py","Los fantasmas de la carretera", icon="🛣️"),
#        Page("Simulaciones/Snell.py", "Simulaciones", icon="👻"),
#    ]
#)


# ---------------------------------------------------------------------- CONTENIDO PROPIO DE LA PÁGINA ----------------------------------------------------------------------


# Función para actualizar la animación en cada cuadro
def update_anim(frame):
    # Calcular la posición x del círculo en función del tiempo (frame)
    x_emisor = posicion_inicial_emisor_x + frame * velocidad_emisor
    x_receptor = posicion_inicial_receptor_x + frame * velocidad_receptor

    # Coordenadas cartesianas del círculo
    theta = np.linspace(0, 2 * np.pi, 100)
    y = np.sin(theta)

    # Actualizar la posición del punto
    circle_emisor.set_center((x_emisor, posicion_inicial_emisor_y))
    circle_emisor_border.set_center((x_emisor, posicion_inicial_emisor_y))

    circle_receptor.set_center((x_receptor, posicion_inicial_receptor_y))
    circle_receptor_border.set_center((x_receptor, posicion_inicial_receptor_y))

    # Actualizar los radios de las circunferencias anteriores con una velocidad de crecimiento ajustada
    #velocidad_propagacion = 0.01  # Velocidad de crecimiento de los círculos
    for c in circles:
        c.set_radius(c.get_radius() + velocidad_propagacion)  # Incremento del radio

    # Crear y dibujar una nueva circunferencia en intervalos regulares
    if frame % intervalo_emision == 0 and frame!=0:
        linewidth = 1  # Grosor de la línea de las circunferencias azules
        new_circle = plt.Circle((x_emisor, posicion_inicial_emisor_y), circle_emisor.radius, color='blue', fill=False, linewidth=linewidth)
        ax.add_artist(new_circle)
        circles.append(new_circle)

    return circle_emisor, circle_emisor_border, *circles


# Crear la figura y los ejes
fig = plt.figure(figsize=(10,3))
ax = fig.add_axes((0,0,1,1), frameon=False) #Frameon = Flase quita el are de afuera de los ejes.
#ax.axis('off')
ax.set_frame_on=False



#-----------------------------------------------------------------------------------
# Parámetros controlables
escala = 1/40
escala_velocidad = 1/10
# Establecer límites de los ejes
dim_x = 2000 * escala
dim_y = 600 * escala
ax.set_xlim(-dim_x/2, dim_x/2)
ax.set_ylim(-dim_y/2, dim_y/2)

# Variables para almacenar las circunferencias creadas
circles = []

    #Parámetros físicos
posicion_inicial_emisor_x = -dim_x/3 # Posición inicial en el eje x del emisor
posicion_inicial_emisor_y = 0  # Posición inicial en el eje y del emisor
velocidad_emisor = 10 * escala  # Velocidad del emisor. (m/s)
posicion_inicial_receptor_x = dim_x/3  # Posición inicial en el eje x del receptor
posicion_inicial_receptor_y = 0  # Posición inicial en el eje y del receptor
velocidad_receptor = 1 * escala  # Velocidad del receptor. (m/s)
velocidad_propagacion = 343.2 * escala * escala_velocidad # Velocidad de proagación de la onda. (m/s)

    # Parámetros de la animación
radio_inicial = (dim_x/2) * escala  # Radio inicial de los círculos de las emisiones.
intervalo_emision = 4  # Intervalo entre emisiones. Propósitos gráficos
#-----------------------------------------------------------------------------------------------


col1, col2, col3, col4 = st.columns(4)

col1.markdown('**EMISOR (Punto naranja):**')
posicion_inicial_emisor_x = col1.slider('Horizontal', -dim_x/2, dim_x/2, -dim_x/3 )
posicion_inicial_emisor_y = col1.slider('Vertical', -dim_y/2, dim_y/2, 0.0 )
velocidad_emisor = col1.number_input('Velocidad (m/s)', value= 10.0, min_value=-30.0, max_value=+30.0, step= 1.0, )
velocidad_emisor*=escala

col2.markdown('**RECEPTOR (Punto rojo):**')
posicion_inicial_receptor_x = col2.slider('Horizontal', -dim_x/2, dim_x/2, +dim_x/3, key='x_receptor' )
posicion_inicial_receptor_y = col2.slider('Vertical', -dim_y/2, dim_y/2, 0.0, key='y_receptor' )
velocidad_receptor = col2.number_input('Velocidad (m/s)', value= 0.0, min_value=-30.0, max_value=+30.0, step= 1.0, key='velocidad_receptor' )
velocidad_receptor*=escala


col3.markdown('**Parámetros físicos**')

romper_fisica = col3.checkbox('Romper la física:', False)
velocidad_sonido = col3.number_input('Velocidad del sonido (m/s)', value = 343.2, min_value=1.0, max_value=2000.0, disabled=not(romper_fisica), help='')
escala_velocidad = col3.number_input('Escala de velocidad (1/...?)', value = 10.0, min_value=1.0, max_value=1000.0, disabled=not(romper_fisica), help='Reducción artificial de la velocidad para que sea observable en la animación (No se considera esta reducción el los cálculos físicos)')


col4.markdown('**ANIMACIÓN**')
intervalo_emision = col4.number_input('Intervalo de emisión', value=4, min_value=1, max_value=20, help='Número de frames entre una emisión y la siguiente')
n_frames = col4.number_input('Nº de fotogramas', value=30, min_value=1, max_value=100, help='Número de imágenes que constituyen la animación')
velocidad_animacion = col4.number_input('Velocidad animación', value=50, min_value=30, max_value=100)


# Dibujar el punto original en la posición inicial como un círculo naranja
circle_emisor = plt.Circle((posicion_inicial_emisor_x, posicion_inicial_emisor_y), radio_inicial, color='orange', fill=True)
ax.add_artist(circle_emisor)
# Dibujar el borde del punto original en la posición inicial como una circunferencia negra
circle_emisor_border = plt.Circle((posicion_inicial_emisor_x, posicion_inicial_emisor_y), radio_inicial, color='black', fill=False, linewidth=2)
ax.add_artist(circle_emisor_border)

# Dibujar el punto original en la posición inicial como un círculo rojo
circle_receptor = plt.Circle((posicion_inicial_receptor_x, posicion_inicial_receptor_y), radio_inicial, color='red', fill=True)
ax.add_artist(circle_receptor)
# Dibujar el borde del punto original en la posición inicial como una circunferencia negra
circle_receptor_border = plt.Circle((posicion_inicial_receptor_x, posicion_inicial_receptor_y), radio_inicial, color='black', fill=False, linewidth=2)
ax.add_artist(circle_receptor_border)


# Crear la animación
anim = animation.FuncAnimation(fig, update_anim, frames=n_frames, interval=velocidad_animacion, blit=True)

# Mostrar la animación
animacion = HTML(anim.to_jshtml())

import streamlit.components.v1 as components
components.html(anim.to_jshtml(), height=1000)

st.write(animacion)
