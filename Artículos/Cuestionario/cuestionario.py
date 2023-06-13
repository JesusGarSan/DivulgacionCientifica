import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm



import streamlit as st
import streamlit.components.v1 as com
with open('styles.css') as styles:
    design = styles.read()

def pregunta_tema():

    #st.markdown('¿Era difícil el tema del artículo?')
    com.html(f"""
         <style>
         {design}
         </style>
         <h4>
         ¿Era difícil el tema del artículo?
         </h4>
         """, height=25)
    
    if st.session_state.respuesta_1 != False:
        com.html(f"""
            <style>
            {design}
            </style>
            <h4 style="background-color: #E3B505">
            😊 ¡Gracias por tu respuesta! 😊
            </h4>
            """, height=30)
    
    else:

        col1, col2, col3,  col4,  col5, = st.columns(5)
        if col1.button('Muy difícil', key='tema 1', use_container_width=True) == True: st.session_state.respuesta_1 = 1; return True
        if col2.button('Difícil', key='tema 2', use_container_width=True)     == True: st.session_state.respuesta_1 = 2; return True
        if col3.button('Regular', key='tema 3', use_container_width=True)     == True: st.session_state.respuesta_1 = 3; return True
        if col4.button('Fácil', key='tema 4', use_container_width=True)       == True: st.session_state.respuesta_1 = 4; return True
        if col5.button('Muy fácil', key='tema 5', use_container_width=True)   == True: st.session_state.respuesta_1 = 5; return True

    return False


def pregunta_explicacion():

    com.html(f"""
         <style>
         {design}
         </style>
         <h4>
         ¿Ha sido fácil de entender la explicación?
         </h4>
         """, height=25)
    
    if st.session_state.respuesta_2 != False:
        com.html(f"""
            <style>
            {design}
            </style>
            <h4 style="background-color: #2ec4b6">
            👐 ¡Gracias por tu respuesta! 👐
            </h4>
            """, height=30)
    
    else:

        col1, col2, col3,  col4,  col5, = st.columns(5)
        if col1.button('Muy difícil', key='explicación 1', use_container_width=True) == True: st.session_state.respuesta_2 = 1; return True
        if col2.button('Difícil', key='explicación 2', use_container_width=True)     == True: st.session_state.respuesta_2 = 2; return True
        if col3.button('Regular', key='explicación 3', use_container_width=True)     == True: st.session_state.respuesta_2 = 3; return True
        if col4.button('Fácil', key='explicación 4', use_container_width=True)       == True: st.session_state.respuesta_2 = 4; return True
        if col5.button('Muy fácil', key='explicación 5', use_container_width=True)   == True: st.session_state.respuesta_2 = 5; return True

    return False



def pregunta_simulacion():

    com.html(f"""
         <style>
         {design}
         </style>
         <h4>
         ¿Han sido útiles las simulaciones?
         </h4>
         """, height=25)
    
    if st.session_state.respuesta_3 != False:
        com.html(f"""
            <style>
            {design}
            </style>
            <h4 style="background-color: #FF6F33">
            🌟 ¡Gracias por tu respuesta! 🌟
            </h4>
            """, height=30)
    
    else:

        col1, col2, col3,  col4,  col5, = st.columns(5)
        if col1.button('Nada útiles', key='simulaciones 1', use_container_width=True)    == True: st.session_state.respuesta_3 = 1; return True
        if col2.button('Poco útiles', key='simulaciones 2', use_container_width=True)    == True: st.session_state.respuesta_3 = 2; return True
        if col3.button('Algo útiles', key='simulaciones 3', use_container_width=True)    == True: st.session_state.respuesta_3 = 3; return True
        if col4.button('Bastante útiles', key='simulaciones 4', use_container_width=True)== True: st.session_state.respuesta_3 = 4; return True
        if col5.button('Muy útiles', key='simulaciones 5', use_container_width=True)     == True: st.session_state.respuesta_3 = 5; return True

    return False


#                       -------------------------    FIN PREGUNTAS   --------------------------


def mostrar_cuestionario():

        if 'respuesta_1' not in st.session_state:
            st.session_state.respuesta_1 = False

        if 'respuesta_2' not in st.session_state:
            st.session_state.respuesta_2 = False

        if 'respuesta_3' not in st.session_state:
            st.session_state.respuesta_3 = False

        com.html(f"""
            <style>
            {design}
            </style>
            <h1>
            ¡Gracias por leer!
            </h1>
            """, height=100)


        if pregunta_tema() == True: st.experimental_rerun()
        if pregunta_explicacion() == True: st.experimental_rerun()
        if pregunta_simulacion() == True: st.experimental_rerun()



#                        ------------------- TESTS DE DESARROLLO --------------------
#mostrar_cuestionario()


