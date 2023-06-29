# ----------------------------------------------------------------------- IMPORTACIÓN DE LIBRERÍAS ------------------------------------------------------------------------
import streamlit as st
from PIL import Image

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
def init_pages():
    show_pages(
        [
            Page("DC.py", "Home", "🏠"),
            # Artículos
            Page("Artículos/Artículos.py","Artículos", icon="📎"),
            Page("Artículos/Refracción/Refracción.py","Los fantasmas de la carretera", icon="🛣️"),
            Page("Artículos/Doppler/Doppler.py","Cómo escuchar la velocidad", icon="🚑"),
            # Simulaciones
            Page('Simulaciones/Simulaciones.py', 'Simulaciones', icon="👻"),
            Page("Simulaciones/Snell/Snell.py", "Ley de Snell", icon="〽️"),
            Page("Simulaciones/Doppler/Doppler.py", "Efecto Doppler", icon="🎯"),
        ]
    )

    publicaciones = pd.read_csv('publicaciones.csv', delimiter=';')
    for index, publicacion in publicaciones.iterrows():
        hide_pages(publicacion.nombre_publico)

init_pages()



# ---------------------------------------------------------------------- CONTENIDO PROPIO DE LA PÁGINA ----------------------------------------------------------------------

from streamlit.components.v1 import html, declare_component
# Wrapt the javascript as html code
my_html = open('./Slideshow/slideshow_html.html').read()

# Execute your app
html(my_html, height=700)
#st.markdown(open('./Slideshow/chat.html').read(), unsafe_allow_html=True)
#st.markdown('<script>' + open('./Slideshow/slideshow_js.js').read() + '</script>', unsafe_allow_html=True)
#st.markdown('<style>' + open('./Slideshow/slideshow_styles.css').read() + '</style>', unsafe_allow_html=True)


def manejarEvento(datos):
    st.write("Datos recibidos desde el componente:", datos)
    # Realiza acciones adicionales con los datos recibidos

# Declara el componente personalizado
componente_personalizado = declare_component(
    "nombre_del_componente",
    url="./Slideshow",
)


def st_custom_slider(label: str, min_value: int, max_value: int, key=None):
    component_value = componente_personalizado(label=label, minValue=min_value, maxValue=max_value, key=key)
    print(component_value)
    return component_value



# Ejecuta tu aplicación de Streamlit

#column = st.columns(2)
#
#column[0].header('**Artículos recientes**')
#column[1].header('**Últimas Simulaciones**')
#
#
#
#
#
#
## -- IMAGEN CLICKEABLE (WIP)
#last_coordinates=None
##with column[0]:
##    last_coordinates = streamlit_image_coordinates(img,)
#
#
## ---- COLUMNA ARTÍCULOS ----
#publicaciones = pd.read_csv('publicaciones.csv', delimiter=';')
#n_articulos = 0
#n_simulaciones = 0
#for index, publicacion in publicaciones.iterrows():
#
#    if publicacion.Tipo == 'Artículo':
#        columna=0; n_articulos+=1
#        if n_articulos >3: continue
#    if publicacion.Tipo == 'Simulación':
#        columna=1; n_simulaciones+=1
#        if n_simulaciones >3: continue
#
#    # Imagen asociada al artículo
#    img = Image.open("Galería/Imágenes/" + publicacion.ruta_imagen)
#    img = img.resize((600,300))
#    column[columna].image(img, use_column_width=True )
#
#    # Botón de acceso al artículo
#    if column[columna].button(publicacion.nombre_publico, use_container_width=True) or last_coordinates!=None:
#        switch_page(publicacion.nombre_publico)




    
    



# ---- MEJORAS PENDIENTES -----
# La lógica para que se pueda clickear en las imágenes para ir al enlace está incorporada, falta que el tamaño de las imágenes se adapte al del contenedor (use_container_width manual)
# Tamibén sería deseable un feedback que la haga lucir "clickeable" al pasar el raton por encima (On_hover). Tal vez baste con el aplicar el comportamiento normal del botón on hover