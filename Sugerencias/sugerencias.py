import streamlit as st
from pathlib import Path

st.header('Contacto')


contact_form="""
<form action="https://formsubmit.co/the.quid.es@gmail.com" method="POST">
     <input type="hidden" name="_template" value="table">
     <input type="hidden" name="_autoresponse" value="¡Gracias por ponerte en contacto con nosotros! A continuación puedes encontrar una copia de tu mensaje:">
     <input type="hidden" name="_captcha" value="false">
     <input type="text" name="name" placeholder="Tu nombre" required>
     <input type="email" name="email" placeholder="Tu e-mail" required>
     <textarea name="message" placeholder="Indícanos tu Sugerencia o Pregunta"></textarea>
     <button type="submit">Enviar</button>
</form>
"""

st.markdown(contact_form, unsafe_allow_html=True)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("./Sugerencias/styles/styles.css")