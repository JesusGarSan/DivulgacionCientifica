# ----------------------------------------------------------------------- IMPORTACIÓN DE LIBRERÍAS ------------------------------------------------------------------------
import streamlit as st
from PIL import Image

from st_pages import Page, Section, show_pages, show_pages_from_config, add_page_title

from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.stoggle import stoggle
from streamlit_image_coordinates import streamlit_image_coordinates
from streamlit_cropper import st_cropper

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

#Cargamos lso estilos css en la página
st.markdown('<style>' + open('./styles.css').read() + '</style>', unsafe_allow_html=True)


show_pages(
    [
        Page("DC.py", "Home", "🏠"),
        Page("Artículos/Artículos.py","Artículos", icon="📎"),
        Page("Artículos/Refracción/Refracción.py","Los fantasmas de la carretera", icon="🛣️"),
        Page('Simulaciones/Simulaciones.py', 'Simulaciones', icon="👻"),
        Page("Simulaciones/Snell.py", "Ley de Snell", icon="〽️"),
        Page("Simulaciones/Doppler.py", "Efecto Doppler", icon="🎯"),
    ]
)





# ---------------------------------------------------------------------- CONTENIDO PROPIO DE LA PÁGINA ----------------------------------------------------------------------

columns = st.columns(2)



    # Ley de Snell
img = Image.open("Galería/Snell.png")
img = img.resize((500,250))
columns[0].image(img, use_column_width=True )
if columns[0].button('Ley de Snell', use_container_width=True):
    switch_page("Ley de Snell")
    

    # Efecto Doppler
img = Image.open("Galería/Doppler.png")
img = img.resize((500,250))
columns[1].image(img, use_column_width=True )
if columns[1].button('Efecto Doppler', use_container_width=True):
    switch_page("Efecto Doppler")
    
    
    