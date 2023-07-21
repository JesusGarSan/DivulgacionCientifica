# ----------------------------------------------------------------------- IMPORTACIÓN DE LIBRERÍAS ------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colormaps
import copy


import streamlit as st
import streamlit.components.v1 as com

import os
# ----------------------------------------------------------------- CONFIGURACIÓN INICIAL DE LA PÁGINA -----------------------------------------------------------------

import setup_page
setup_page.setup_page()


#------------------------------------------------------------------------- DEFINICIÓN DE FUNCIONES ------------------------------------------------------------------------

import sys
sys.path.insert(0, 'Simulaciones/Snell/')
from Snell_functions import *

# ---------------------------------------------------------------------- CONTENIDO PROPIO DE LA PÁGINA ----------------------------------------------------------------------
st.title('Ley de Snell multimedio')
st.divider()
column = st.columns(2)
with column[0]: 
    n, O_1,  plot_reflexiones, plot_refracciones, max_reflexiones = parameter_dashboard()

with column[1]:
    mostrar_simulacion(n, O_1,  plot_reflexiones, plot_refracciones, max_reflexiones)


# ----------------------------------------------------------------------------- FOOTER ----------------------------------------------------------------------------------


