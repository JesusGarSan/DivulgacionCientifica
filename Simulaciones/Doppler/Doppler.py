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




#-----------------------------------------------------------------------------------
# Parámetros controlables
# Establecer límites de los ejes


escala_velocidad = 1/10
# Variables para almacenar las circunferencias creadas
circles = []

#Parámetros físicos
#velocidad_propagacion = 343.2 * escala * escala_velocidad # Velocidad de proagación de la onda. (m/s)
#-----------------------------------------------------------------------------------------------


parametros, dim_x, dim_y = dashboard_parametros()
crear_animación(parametros,  dim_x, dim_y, height = 550, width = 1500)

# Crear la figura y los ejes
fig = plt.figure(figsize=(10,3))
ax = fig.add_axes((0,0,1,1), frameon=False) #Frameon = False quita el are de afuera de los ejes.
#ax.axis('off')
ax.set_frame_on=False

# ------ ALTERADOR DE AUDIO VIA DOPPLER NO SE QUÉ -------
st.divider()
velocidad_emisor = parametros['velocidad_emisor']  /parametros['escala']
audio_to_Doppler(parametros['f_receptor'], parametros['f_emisor'], velocidad_emisor, parametros['velocidad_sonido'])