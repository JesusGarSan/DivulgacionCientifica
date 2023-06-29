# ----------------------------------------------------------------------- IMPORTACIÓN DE LIBRERÍAS ------------------------------------------------------------------------
from PIL import Image

import streamlit as st

from st_pages import Page, Section, show_pages, show_pages_from_config, add_page_title, hide_pages

from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.stoggle import stoggle
from streamlit_image_coordinates import streamlit_image_coordinates


# ---------------------------------------------------------------------


# ----------------------------------------------------------------- CONFIGURACIÓN INICIAL DE LA PÁGINA -----------------------------------------------------------------

import setup_page
setup_page.setup_page()

#Cargamos los estilos css en la página
st.markdown('<style>' + open('./styles.css').read() + '</style>', unsafe_allow_html=True)


import pandas as pd
publicaciones = pd.read_csv('publicaciones.csv', delimiter=';')
for index, publicacion in publicaciones.iterrows():
    hide_pages(publicacion.nombre_publico)
# ---------------------------------------------------------------------- CONTENIDO PROPIO DE LA PÁGINA ----------------------------------------------------------------------


column = st.columns(2)

last_coordinates = None


import pandas as pd
publicaciones = pd.read_csv('publicaciones.csv', delimiter=';')
for index, publicacion in publicaciones.iterrows():
    if publicacion.Tipo!='Artículo': continue

    # Imagen asociada al artículo
    img = Image.open("Galería/Imágenes/" + publicacion.ruta_imagen)
    img = img.resize((600,300))
    column[(index+1)%2].image(img, use_column_width=True )

    # Botón de acceso al artículo
    if column[(index+1)%2].button(publicacion.nombre_publico, use_container_width=True) or last_coordinates!=None:
        switch_page(publicacion.nombre_publico)