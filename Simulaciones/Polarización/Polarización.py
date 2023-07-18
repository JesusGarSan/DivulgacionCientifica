# ----------------------------------------------------------------------- IMPORTACIÓN DE LIBRERÍAS ------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colormaps
from matplotlib.animation import FuncAnimation

import copy


import streamlit as st
import streamlit.components.v1 as com

import os
# ----------------------------------------------------------------- CONFIGURACIÓN INICIAL DE LA PÁGINA -----------------------------------------------------------------
import setup_page
setup_page.setup_page()

# ------------------------------------------------------------------- CONTENIDO PROPIO DE LA PÁGINA --------------------------------------------------------------------
def parameter_dashboard():
    n_inicial_ondas = st.number_input('Número de ondas', min_value=1, max_value=20, value=5)
    amplitud = st.number_input('Amplitud de las ondas', min_value=0.0, value=0.6)
    polarizar = st.checkbox('Aplicar polarizador', value=False)
    rango_desfase = st.number_input('Rango de desfase entre ondas incidentes', min_value=0.0, max_value=2*np.pi, value = 2*np.pi /5)
    if rango_desfase == 0: desfasar = False
    else: desfasar= True
    desfases = np.random.rand(n_inicial_ondas) * rango_desfase

    return amplitud, n_inicial_ondas, polarizar,  desfasar, desfases

def animation_dashboard():
    frames = st.number_input('Nº de fotogramas', min_value=1, max_value=200, value=100)
    fps = st.number_input('Fotogramas por segundo', min_value=10, max_value=60, value=30)
    pos_camara=[0,0]
    vel_camara=[0,0]
    col1, col2 = st.columns(2)
    pos_camara[0] = col1.number_input('Posición inicial de la cámara', value=-160.0)
    pos_camara[1] = col2.number_input('Y coord',label_visibility='hidden', value=60.0)
    vel_camara[0] = col1.number_input('Velocidad cámara', value= 0.0)
    vel_camara[1] = col2.number_input('Y coord',label_visibility='hidden', value= -0.16)

    return frames, fps, pos_camara, vel_camara

@st.cache_data(show_spinner=False)
def crear_animación(params):
    # Figura sobre la que se mostrará la animación
    fig = plt.figure(figsize=(7, 5))
    ax = plt.axes(projection = '3d')
    np.random.seed(1)


    # Función para actualizar frmaes
    def animate(frame, fig, ax, amplitud, incremento_ondas, polarizar , desfasar, rotar, pos_camara=[-160,60], vel_camara=[0,-0.16]):

        line = np.linspace(0,6*np.pi, 1000)
        #amplitud = 0.6
        x = line
        y = line * 0
        z = np.sin(x + frame/np.pi)*amplitud
        ax.cla()
        
        plt.grid(True)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])

        #global n_ondas
        #if incremento_ondas!=0:
        #    desfasar=False
        #    if frame % incremento_ondas == 0 :
        #        n_ondas+=1




        # Dibujar ondas
        for i in range(n_ondas)[::-1]:
            if desfasar: z = np.sin(x + frame/np.pi+desfases[i])*amplitud

            angle = np.radians(360 / n_ondas * i + rotar*frame)  # Actualizar el ángulo con respecto al frame
            rotation_matrix = np.array([[1, 0, 0],
                                        [0, np.cos(angle), -np.sin(angle)],
                                        [0, np.sin(angle), np.cos(angle)]])
            rotated_points = np.dot(rotation_matrix, np.array([x, y, z]))

            rotated_x, rotated_y, rotated_z = rotated_points

            if polarizar: lines.append(ax.plot3D(rotated_x[500:], rotated_y[500:], rotated_z[500:], 'orange'))
            else: lines.append(ax.plot3D(rotated_x[:], rotated_y[:], rotated_z[:], 'orange'))
            

        # Dirección de propagación
        ax.plot3D(line, line * 0, line * 0, 'blue')

        ax.set_xlim(0, np.max(rotated_x))
        ax.set_ylim(-3, 3)
        ax.set_zlim(-3, 3)

        # Polarizador 
        if polarizar:
            lineas_poralizador = 20
            for i in range(lineas_poralizador)[::-1]:
                ax.plot3D([np.max(x)/2, np.max(x)/2], [-3 + 6*i/lineas_poralizador, -3+ 6*i/lineas_poralizador], [-3, 3]
                        , 'grey')
                if i == lineas_poralizador//2:
                    lines.append(ax.plot3D(rotated_x[:500], rotated_y[:500], rotated_z[:500], 'orange'))

        ax.view_init(pos_camara[0] + frame * vel_camara[0], pos_camara[1] + frame * vel_camara[1])

        return



    # Crea la animación
    ani = FuncAnimation(fig, animate, fargs=(fig, ax, amplitud, 0, polarizar, desfasar, 0, pos_camara, vel_camara), frames=frames, interval=50)
    # Muestra la animación
    import streamlit.components.v1 as components 
    components.html(ani.to_jshtml(fps= fps, default_mode='Once'), height=1000, width=1000)
    


column = st.columns(2)

with column[0]:
    st.header('Parámetros físicos')
    amplitud, n_inicial_ondas, polarizar,  desfasar, desfases = parameter_dashboard()
    st.header('Configuración animación')
    frames, fps, pos_camara, vel_camara = animation_dashboard()

n_ondas = n_inicial_ondas
lines = []

with column[1]:
    params = [n_inicial_ondas, amplitud, 0, polarizar , desfasar, 0, pos_camara, vel_camara ] 
    with st.spinner('Creando animación...'): crear_animación(params)
