# ----------------------------------------------------------------------- IMPORTACIÓN DE LIBRERÍAS ------------------------------------------------------------------------
import streamlit as st
from PIL import Image
import pandas as pd

from st_pages import Page, Section, show_pages, show_pages_from_config, add_page_title, hide_pages

from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.stoggle import stoggle
from streamlit_image_coordinates import streamlit_image_coordinates




# ----------------------------------------------------------------- CONFIGURACIÓN INICIAL DE LA PÁGINA -----------------------------------------------------------------

import setup_page
setup_page.setup_page()

# ------------------------------------------------------------------------- DECLARACIÓN DE FUNCIONES -----------------------------------------------------------------------

def get_recent(publicaciones_file, n_publicaciones):
    
    publicaciones = pd.read_csv(publicaciones_file, delimiter=';')
    publicaciones = publicaciones.iloc[::-1][:n_publicaciones]
    hrefs, clases, nombres, srcs = [], [], [], []
    for index, row in publicaciones.iterrows():
        hrefs.append(f"'{row.nombre_publico}'")
        clases.append(normalize(row.Tipo).lower())
        nombres.append(row.Tipo+': '+row.nombre_publico)
        srcs.append(f"https://github.com/JesusGarSan/DivulgacionCientifica/blob/main/Galer%C3%ADa/Im%C3%A1genes/{row.ruta_imagen}?raw=true")
        

    return hrefs, clases, nombres, srcs

def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s

def carrusel_HTML(hrefs, clase, nombres, srcs, counter):
    carrusel=r"""
<!DOCTYPE html>
<html>
   <head>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <style>
         * {box-sizing: border-box;}
         body {font-family: Verdana, sans-serif;}
         /*.mySlides {display: none;}*/
         img {vertical-align: middle;}
         /* Slideshow container */
         .slideshow-container {
         max-width: 80%;
         height: 50%;
         position: relative;
         margin: auto;
         }
         .slideshow-image{
         width: 100%; /* Establece el ancho deseado */
         height: 500px; /* Mantiene la proporción de aspecto original */         
         }
         /* Caption text */
         .text {
         color: #f2f2f2;
         font-size: 15px;
         padding: 8px 12px;
         position: absolute;
         bottom: 8px;
         width: 100%;
         text-align: center;
         }
         /* Number text (1/3 etc) */
         .articulo {
         color: #f2f2f2;
         background-color: rgba(0, 0, 255, 0.5); /* Cambia el último valor (0.5) para ajustar la transparencia */
         font-size: 32px;
         padding: 8px 12px;
         position: absolute;
         top: 0;
         left: 0;
         right: 0;
         }
         .simulacion {
         color: #f2f2f2;
         background-color: rgba(255, 0, 0, 0.5); /* Cambia el último valor (0.5) para ajustar la transparencia */
         font-size: 32px;
         padding: 8px 12px;
         position: absolute;
         top: 0;
         left: 0;
         right: 0;
         }
         /* The dots/bullets/indicators */
         .dot {
         height: 15px;
         width: 15px;
         margin: 0 2px;
         background-color: #bbb;
         border-radius: 50%;
         display: inline-block;
         transition: background-color 0.6s ease;
         }
         .active {
         background-color: #717171;
         }
         /* Fading animation */
         .fade {
         animation-name: fade;
         animation-duration: 1.5s;
         }
         @keyframes fade {
         from {opacity: .4} 
         to {opacity: 1}
         }
         /* On smaller screens, decrease text size */
         @media only screen and (max-width: 300px) {
         .text {font-size: 11px}
         }
         /* Botones de navegación */
         .prev, .next {
         cursor: pointer;
         position: absolute;
         top: 50%;
         width: auto;
         padding: 16px;
         margin-top: -22px;
         color: white;
         font-weight: bold;
         font-size: 18px;
         transition: 0.6s ease;
         border-radius: 0 3px 3px 0;
         user-select: none;
         }
         /* Posición del botón de navegación izquierdo */
         .prev {
         left: 0;
         }
         /* Posición del botón de navegación derecho */
         .next {
         right: 0;
         }
         /* Cambio de color de los botones de navegación al pasar el mouse sobre ellos */
         .prev:hover, .next:hover {
         background-color: rgba(255, 0, 0, 0.8);
         }
      </style>
   </head>"""+f"""
   <body>
      <div class="slideshow-container">
         <div class="mySlides fade">
            <a href={hrefs[counter]} target="_self">
               <img src={srcs[counter]} class="slideshow-image">
               <div class="{clase[counter]}">{nombres[counter]}</div>
            </a>
         </div>
      </div>
      </div>
      <br>
   </body>
</html>
                """

    st.markdown(carrusel, unsafe_allow_html=True)

def carrusel(hrefs, clases, nombres, srcs):
    if 'counter' not in st.session_state:
        st.session_state.counter = 1
    if 'seleccion' not in st.session_state:
        st.session_state.seleccion = 1
    total = len(nombres)
    cols = st.columns([.05,.9,.05])
    with cols[1]:

        n = len(nombres)
        botones = [ButtonsItem(icon='chevron-left'),]
        for i in range(n): botones.append(ButtonsItem(str(i+1)))
        botones.append(ButtonsItem(icon='chevron-right'),)

        st.session_state.seleccion = buttons(botones, align='center', return_index=True, grow=False, index = None)


    selection = st.session_state.seleccion

    if selection == 0: st.session_state.counter-=1
    elif selection == total+1: st.session_state.counter+=1
    elif selection!=None: st.session_state.counter = selection
    if st.session_state.counter >= total: st.session_state.counter-=total
    if st.session_state.counter < 0: st.session_state.counter+=total



    counter = st.session_state.counter-1
    with cols[1]:
        carrusel_HTML(hrefs, clases, nombres, srcs, counter)

    # ---- Ciclado automático -----
    import time
    if selection == None: # Sólo si no se ha pinchado ya para moverse
        counter = st.session_state.counter
        time.sleep(6) # Tiempo entra cada cambio de imagen automático
        counter +=  1
        if counter >= total: counter-=total

        st.session_state.counter = counter
        st.experimental_rerun()

# ---------------------------------------------------------------------- CONTENIDO PROPIO DE LA PÁGINA ----------------------------------------------------------------------


from streamlit_antd_components import *

st.title('Publicaciones recientes')
hrefs, clases, nombres, srcs = get_recent('publicaciones.csv', 5)
carrusel(hrefs, clases, nombres, srcs)




#### Carrusel funcional con js pero con limitacione intrínsecas de funcionamiento
#from streamlit.components.v1 import html, declare_component
#slideshow = open('./Slideshow/slideshow_html.html').read()
#html(slideshow, height=700)


#st.markdown(open('./Slideshow/chat.html').read(), unsafe_allow_html=True)
#st.markdown('<script>' + open('./Slideshow/slideshow_js.js').read() + '</script>', unsafe_allow_html=True)
#st.markdown('<style>' + open('./Slideshow/slideshow_styles.css').read() + '</style>', unsafe_allow_html=True)



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
