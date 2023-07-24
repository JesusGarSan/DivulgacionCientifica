# ----------------------------------------------------------------------- IMPORTACIÓN DE LIBRERÍAS ------------------------------------------------------------------------

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import HTML
import numpy as np
import librosa
import soundfile as sf



import streamlit as st
import streamlit.components.v1 as com


from streamlit_toggle import st_toggle_switch



# ----------------------------------------------------------------- CONFIGURACIÓN INICIAL DE LA PÁGINA -----------------------------------------------------------------
import setup_page
setup_page.setup_page()

import sys
sys.path.insert(0, 'Simulaciones/Doppler/')
from Doppler_functions import *

#------------------------------------------------------------------------- DEFINICIÓN DE FUNCIONES ------------------------------------------------------------------------

# ---------------------------------------------------------------------- CONTENIDO PROPIO DE LA PÁGINA ----------------------------------------------------------------------

st.title('Efecto Doppler')
st.divider()
st.header('Crea tu propia animación')


# Parámetros controlables
escala_velocidad = 1/10
# Variables para almacenar las circunferencias creadas
circles = []
#-----------------------------------------------------------------------------------------------
parametros, dim_x, dim_y = dashboard_parametros()

if st.button('Crear animación'):
    with st.spinner('Creando animación...'):
        crear_animación(parametros,  dim_x, dim_y, height = 550, width = 1500)

# Crear la figura y los ejes
fig = plt.figure(figsize=(10,3))
ax = fig.add_axes((0,0,1,1), frameon=False) #Frameon = False quita el are de afuera de los ejes.
ax.set_frame_on=False



# ------ ALTERADOR DE AUDIO VIA DOPPLER NO SE QUÉ -------
st.header('Modifica tu propio audio según el efecto Doppler')
column= st.columns(2)
st.markdown(f"""
                   Aplica el efecto Doppler a los audios que tu quieras.
                   Los parámetros que se usan para la alteración son los específicados arriba en la animación.
                   """)
#velocidad_emisor = parametros['velocidad_emisor']  /parametros['escala']


#v_e, v_r, c, input_file, output_file = Doppler_audio_dashboard()
Doppler_audio_dashboard(parametros)
