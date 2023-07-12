
import streamlit as st
import numpy as np
from PIL import Image

import setup_page
setup_page.setup_page()


st.header('¡Envíanos tus preguntas!')
st.markdown('¿Hay algo de tu día a día que te llame la atención pero no entiendas?')
st.markdown('¿Te gustaría una explicación de algún fenómeno en concreto?')
st.markdown('¿Tienes alguna idea o sugerencia?')
st.markdown('¡Escríbenos!')



if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'images' not in st.session_state:
    st.session_state.images = []


image = st.file_uploader('Adjunta imagen ilustrativa', )
if image != None:
    st.session_state.messages.append(image)
    image= None



input = st.chat_input('Escribe tu pregunta aquí')
if input != None:
    st.session_state.messages.append(input)
    messages = st.session_state.messages
    with st.chat_message(name='user', avatar='❓'):
        for message in messages:
            if type(message) == str: st.markdown(message)


messages = st.session_state.messages
import os
if len(messages)> 0:
    try: os.mkdir('Sugerencias/user')
    except: pass
    f = open('Sugerencias/user/sugerencias.txt', 'w')
    for message in messages:
        if type(message) == str: f.write(message + '\n')
        else: 
            img = Image.open(message)
            img.save(f'Sugerencias/user/{message.name}')
    
    f.close()

