# ----------------------------------------------------------------------- IMPORTACIÓN DE LIBRERÍAS ------------------------------------------------------------------------
import streamlit as st

from st_pages import Page, Section, show_pages, show_pages_from_config, add_page_title

from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.stoggle import stoggle
from streamlit_image_coordinates import streamlit_image_coordinates


# ---------------------------------------------------------------------


# ----------------------------------------------------------------- CONFIGURACIÓN INICIAL DE LA PÁGINA -----------------------------------------------------------------

st.set_page_config('Divulgación Científica', '💭', 'wide', initial_sidebar_state='expanded')

#add_page_title()
#show_pages_from_config()

hide_st_style = """
                <style>
                #mainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

import streamlit.components.v1 as com
with open('styles.css') as styles:
    design = styles.read()


# ---------------------------------------------------------------------- CONTENIDO PROPIO DE LA PÁGINA ----------------------------------------------------------------------


column = st.columns(2)

last_coordinates=None
#last_coordinates = streamlit_image_coordinates("Artículos/Refracción/charco.png")
column[0].image("Artículos/Refracción/charco.png")
if column[0].button('Los fantasmas de la carretera', use_container_width=True) or last_coordinates!=None:
    switch_page("Los fantasmas de la carretera")

