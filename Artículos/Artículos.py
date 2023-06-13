# ----------------------------------------------------------------------- IMPORTACIÓN DE LIBRERÍAS ------------------------------------------------------------------------
import streamlit as st

from st_pages import Page, Section, show_pages, show_pages_from_config, add_page_title
import webbrowser


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


COL1, COL2 = st.columns(2)


COL1.image("Artículos/Refracción/charco.png")
if COL1.button('Los fantasmas de las carreteras', use_container_width=True):
    webbrowser.open_new("https://jesusgarsan-divulgacioncientifica-dc-1cv9hy.streamlit.app/Los%20fantasmas%20de%20la%20carretera")

