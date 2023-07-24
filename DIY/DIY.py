# ----------------------------------------------------------------------- IMPORTACIÓN DE LIBRERÍAS ------------------------------------------------------------------------


# ----------------------------------------------------------------- CONFIGURACIÓN INICIAL DE LA PÁGINA -----------------------------------------------------------------
import setup_page
setup_page.setup_page()

# ---------------------------------------------------------------------- CONTENIDO PROPIO DE LA PÁGINA ----------------------------------------------------------------------
from functions import *

st.write('') # Para dar algo de margen superior
column = st.columns([0.3, 0.7])
with column[0]:
    category_selector()
with column[1]:
    search_bar('DIY')
    mostrar_publicaciones('DIY')

