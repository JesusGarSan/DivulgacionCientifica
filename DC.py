# ----------------------------------------------------------------------- IMPORTACIÓN DE LIBRERÍAS ------------------------------------------------------------------------
import streamlit as st

from st_pages import Page, Section, show_pages, show_pages_from_config, add_page_title


# ---------------------------------------------------------------------


# ----------------------------------------------------------------- CONFIGURACIÓN INICIAL DE LA PÁGINA -----------------------------------------------------------------

st.set_page_config('Divulgación Científica', '💭', 'wide', initial_sidebar_state='expanded')

#add_page_title()
#show_pages_from_config()

#hide_st_style = """
#                <style>
#                #mainMenu {visibility: hidden;}
#                footer {visibility: hidden;}
#                header {visibility: hidden;}
#                </style>
#"""
#st.markdown(hide_st_style, unsafe_allow_html=True)

import streamlit.components.v1 as com
with open('styles.css') as styles:
    design = styles.read()


show_pages(
    [
        Page("DC.py", "Home", "🏠"),
        Section("Artículos", icon="📎"),
        Page("Refracción/Refracción.py","Los fantasmas de la carretera", icon="🛣️"),
    ]
)



# ---------------------------------------------------------------------- CONTENIDO PROPIO DE LA PÁGINA ----------------------------------------------------------------------


COL1, COL2 = st.columns(2)

com.html(f"""
         <div>
         <style>
         {design}
         </style>
         <h2 class="column>
         Artículos recientes
         </h2>
         </div>
         """)

