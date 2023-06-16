# ----------------------------------------------------------------------- IMPORTACIÓN DE LIBRERÍAS ------------------------------------------------------------------------
import streamlit as st

from st_pages import Page, Section, show_pages, show_pages_from_config, add_page_title



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
        Section('Simulaciones', icon="👻"),
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

COL1, COL2 = st.columns(2)




