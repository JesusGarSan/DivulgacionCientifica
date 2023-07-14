import streamlit as st
from pathlib import Path

import setup_page
setup_page.setup_page('centered', local_css="./Sugerencias/styles/styles.css")

st.title(':mailbox_with_mail: Buzón de sugerencias')

st.write("""
Puedes usar este formulario para ponerte en contacto con nosotros. Estamos abiertos a **sugerencias para la página**, **dudas** que tengas y te gustaría que tratásemos o cualquier otra cuestión.
         
¡Estaremos encantados de leer lo que nos escribas!
         """)

contact_form="""
<form action="https://formsubmit.co/the.quid.es@gmail.com" method="POST">
     <input type="hidden" name="_template" value="table">
     <input type="hidden" name="_autoresponse" value="¡Gracias por ponerte en contacto con nosotros! A continuación puedes encontrar una copia de tu mensaje:">
     <input type="hidden" name="_captcha" value="false">
     <input type="text" name="name" placeholder="Tu nombre" required>
     <input type="email" name="email" placeholder="Tu e-mail" required>
     <textarea name="message" placeholder="Indícanos tu Sugerencia o Pregunta" required></textarea>
     <button type="submit">Enviar</button>
</form>
"""

st.markdown(contact_form, unsafe_allow_html=True)
