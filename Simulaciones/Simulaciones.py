# ----------------------------------------------------------------------- IMPORTACIÓN DE LIBRERÍAS ------------------------------------------------------------------------
import streamlit as st
from PIL import Image

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

#Cargamos los estilos css en la página
st.markdown('<style>' + open('./styles.css').read() + '</style>', unsafe_allow_html=True)


#show_pages(
#    [
#        Page("DC.py", "Home", "🏠"),
#        Page("Artículos/Artículos.py","Artículos", icon="📎"),
#        Page("Artículos/Refracción/Refracción.py","Los fantasmas de la carretera", icon="🛣️"),
#        Page('Simulaciones/Simulaciones.py', 'Simulaciones', icon="👻"),
#        Page("Simulaciones/Snell.py", "Ley de Snell", icon="〽️"),
#        Page("Simulaciones/Doppler.py", "Efecto Doppler", icon="🎯"),
#    ]
#)





# ---------------------------------------------------------------------- CONTENIDO PROPIO DE LA PÁGINA ----------------------------------------------------------------------

column = st.columns(2)


last_coordinates = None


import pandas as pd
publicaciones = pd.read_csv('publicaciones.csv', delimiter=';')
for index, publicacion in publicaciones.iterrows():
    if publicacion.Tipo!='Simulación': continue

    # Imagen asociada al artículo
    img = Image.open("Galería/Imágenes/" + publicacion.ruta_imagen)
    img = img.resize((600,300))
    column[(index+1)%2].image(img, use_column_width=True )

    # Botón de acceso al artículo
    if column[(index+1)%2].button(publicacion.nombre_publico, use_container_width=True) or last_coordinates!=None:
        switch_page(publicacion.nombre_publico)
    