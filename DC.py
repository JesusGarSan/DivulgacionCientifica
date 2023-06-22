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

#Cargamos lso estilos css en la página
st.markdown('<style>' + open('./styles.css').read() + '</style>', unsafe_allow_html=True)


show_pages(
    [
        Page("DC.py", "Home", "🏠"),
        Page("Artículos/Artículos.py","Artículos", icon="📎"),
        Page("Artículos/Refracción/Refracción.py","Los fantasmas de la carretera", icon="🛣️"),
        Page("Artículos/Doppler/Doppler.py","Cómo escuchar la velocidad", icon="🚑"),
        Page('Simulaciones/Simulaciones.py', 'Simulaciones', icon="👻"),
        Page("Simulaciones/Snell.py", "Ley de Snell", icon="〽️"),
        Page("Simulaciones/Doppler.py", "Efecto Doppler", icon="🎯"),
    ]
)



# ---------------------------------------------------------------------- CONTENIDO PROPIO DE LA PÁGINA ----------------------------------------------------------------------

st.markdown(f"""
            <h1>
            Divulgación Científica
            </h1>
            """, unsafe_allow_html=True)

column = st.columns(2)

column[0].header('**Artículos recientes**')
column[1].header('**Últimas Simulaciones**')


# ---- COLUMNA ARTÍCULOS ----


img = Image.open("Galería/charco.png")
img = img.resize((600,300))
column[0].image(img, use_column_width=True )

# -- IMAGEN CLICKEABLE (WIP)
last_coordinates=None
#with column[0]:
#    last_coordinates = streamlit_image_coordinates(img,)



if column[0].button('Los fantasmas de la carretera', use_container_width=True) or last_coordinates!=None:
    switch_page("Los fantasmas de la carretera")


# ---- COLUMNA SIMULACIONES ----


    # Efecto Doppler
img = Image.open("Galería/Doppler.png")
img = img.resize((500,250))
column[1].image(img, use_column_width=True )
if column[1].button('Efecto Doppler', use_container_width=True):
    switch_page("Efecto Doppler")
    
    
    
    # Ley de Snell
img = Image.open("Galería/Snell.png")
img = img.resize((500,250))
column[1].image(img, use_column_width=True )
if column[1].button('Ley de Snell', use_container_width=True):
    switch_page("Ley de Snell")
    
    

    
    
    



# ---- MEJORAS PENDIENTES -----
# La lógica para que se pueda clickear en las imágenes para ir al enlace está incorporada, falta que el tamaño de las imágenes se adapte al del contenedor (use_container_width manual)
# Tamibén sería deseable un feedback que la haga lucir "clickeable" al pasar el raton por encima (On_hover). Tal vez baste con el aplicar el comportamiento normal del botón on hover
