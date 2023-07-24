import streamlit as st
from st_pages import Page, Section, show_pages, show_pages_from_config, add_page_title, hide_pages


def setup_page(width='wide', local_css = None):

    st.set_page_config('El Quid', '🔍', width, initial_sidebar_state='expanded')
    load_css()
    if local_css!=None: load_css(local_css)
    hide_streamlits()
    show_header()
    init_pages()

# ----------------------------------------------------------------------------------------------

def show_header():
    st.markdown('<style>' + open('./Header/header_styles.css').read() + '</style>', unsafe_allow_html=True)
    st.markdown(open('./Header/header_html.html').read(), unsafe_allow_html=True)

def hide_streamlits():
    hide_st_style = """
                <style>
                mainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                [data-testid="collapsedControl"] {
                display: none
                }
                </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)

def load_css(sheet = 'styles.css'):
    st.markdown('<style>' + open('./'+sheet).read() + '</style>', unsafe_allow_html=True)

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
            Page("Simulaciones/Polarización/Polarización.py", "Polarización de la luz", icon=":bulb:"),
            # Hazlo en casa
            Page("DIY/DIY.py", "DIY"),
            # Galería
            Page("Galería/galería.py", "Galería"),
            # Sugerencias
            Page('Sugerencias/sugerencias.py', 'Sugerencias'),
            Page("Sugerencias/agradecimiento.py", 'Gracias'),
        ]
    )
