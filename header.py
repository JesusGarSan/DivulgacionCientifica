# ----------------------------------------------------------------------- IMPORTACIÓN DE LIBRERÍAS ------------------------------------------------------------------------
import streamlit as st


# ------------------------------------------------------------------------------- HEADER -------------------------------------------------------------------------
def show_header():
    st.markdown('<style>' + open('Header\header_styles.css').read() + '</style>', unsafe_allow_html=True)
    st.markdown(open('Header\header_html.html').read(), unsafe_allow_html=True)





# Botón de HTML para cambiar de página. 
# st.markdown('<a href="/Artículos" target="_self">Next page</a>', unsafe_allow_html=True)

