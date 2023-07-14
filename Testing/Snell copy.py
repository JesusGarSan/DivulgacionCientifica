# ----------------------------------------------------------------------- IMPORTACIÓN DE LIBRERÍAS ------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colormaps



import streamlit as st
import streamlit.components.v1 as com

import os

# ----------------------------------------------------------------- CONFIGURACIÓN INICIAL DE LA PÁGINA -----------------------------------------------------------------
# Configuración ancha de la página
st.set_page_config(layout='wide')


# Escondemos las masrcas de agua y menú hamburguesa
#hide_st_style = """
#                <style>
#                #mainMenu {visibility: hidden;}
#                footer {visibility: hidden;}
#                header {visibility: hidden;}
#                </style>
#"""
#st.markdown(hide_st_style, unsafe_allow_html=True)


# Cargamos los estilos css
#with open('styles.css') as styles:
#    design = styles.read()




# ---------------------------------------------------------------------- CONTENIDO PROPIO DE LA PÁGINA ----------------------------------------------------------------------

#------------------------------------------------------------------------- DEFINICIÓN DE FUNCIONES ------------------------------------------------------------------------

# Coordenadas polares

def polares(centro, r, theta):
    extremo=[0,0]
    extremo[0] = centro[0]+ r*np.sin(theta)
    extremo[1] = centro[1]+ r*np.cos(theta)

    return extremo

# Ley de Snell
# n_1 * sin(O_1) = n_2 * sin(O_2)
def snell(n_1, n_2, O_1):
    if abs(n_1/n_2 * np.sin(O_1/180*np.pi) )>1: return None
    return np.arcsin( n_1/n_2 * np.sin(O_1/180*np.pi) ) * 180/np.pi


#Dibujado y ploteo del simulador
def simulador_snell(n_1, n_x, O_1, n_medios, plot_reflexiones):
    incremento_n = (n_x - n_1)/n_medios

    fig, ax = plt.subplots(figsize=(12,10))
    ax.axis('off')
    ax.set_xlim(-1,1)
    ax.set_ylim(-1,1)

    ax.text(-1,.85, 'Medio 1', fontsize=24)
    ax.text(-1,-.99, f'Medio {n_medios+1}', fontsize=24)
    ax.fill_between([-1,1], [1,1], color='white') # medio 1

    # Rayo incidente
    longitud_rayos = 1
    inc_x = [-longitud_rayos * np.sin(np.pi*O_1/180),0]
    inc_y = [longitud_rayos * np.cos(np.pi*O_1/180),0]

    color_incidente='blue'

    ax.fill_between([-1,1], [1,1], color='white') # medio 1
    ax.vlines(0, -1, 1, color='grey', linestyles='dashed') # vertical
    ax.plot(inc_x, inc_y, color=color_incidente, label='Rayo incidente')
    ax.arrow( (inc_x[0]+inc_x[1])/2, (inc_y[0]+inc_y[1])/2, 0.02*np.sin(np.pi*O_1/180), -0.02*np.cos(np.pi*O_1/180), width=.008, color=color_incidente, length_includes_head=True)

    # Rayo Reflejado

    longitud_rayos = .8
    reflejado_x = [longitud_rayos * np.sin(np.pi*O_1/180),0]
    reflejado_y = [longitud_rayos * np.cos(np.pi*O_1/180),0]

    color_reflexion = 'green'

    ax.vlines(0, -1, 1, color='grey', linestyles='dashed') # vertical
    ax.plot(reflejado_x, reflejado_y, color=color_reflexion, label='Rayo reflejado')
    ax.arrow( (reflejado_x[0]+reflejado_x[1])/2, (reflejado_y[0]+reflejado_y[1])/2, 0.02*np.sin(np.pi*O_1/180), 0.02*np.cos(np.pi*O_1/180),
            width=.008, color=color_reflexion, length_includes_head=True)


    # Medios
    colormap = colormaps.get_cmap('Wistia')
    step_1=0
    for i in range(n_medios):
        step_2=-(i+1)/n_medios
        ax.fill_between([-1, 1], [step_1, step_1], [step_2, step_2], color=colormap(i/n_medios)) # medio 2
        step_1=step_2


    # Rayos refractados
    O_2=O_1
    refrac_x=[0,0]
    refrac_y=[0,0]
    color_refrac = 'red'
    dibujar_flecha=True
    for i in range(n_medios):
        O_1 = O_2
        O_2 = snell(n_1, n_1+(i+1)*incremento_n, O_1)



        if O_2!=None:
            longitud_segmentos = 1/n_medios/np.cos(np.pi*O_2/180)

            refrac_x = [0 + refrac_x[1], refrac_x[1] + longitud_segmentos * np.sin(np.pi*O_2/180)]
            refrac_y = [0 + refrac_y[1], refrac_y[1] + -longitud_segmentos * np.cos(np.pi*O_2/180)]

            # Dibujamos la flecha de dirección correctamente si sólo hay 1 medio refractante
            if n_medios == 1:
                if refrac_x[1] > 0.5: divisor = refrac_x[1]*2
                ax.arrow( (refrac_x[0]+refrac_x[1])/divisor, (refrac_y[0]+refrac_y[1])/divisor, 0.02*np.sin(np.pi*O_2/180), -0.02*np.cos(np.pi*O_2/180), width=.008, color=color_refrac, length_includes_head=True)
                dibujar_flecha=False
            # Dibujamos la flecha de dirección
            if (refrac_x[0]>0.5 or refrac_y[0]<-0.5) and dibujar_flecha:
                ax.arrow( refrac_x[0], refrac_y[0], 0.02*np.sin(np.pi*O_2/180), -0.02*np.cos(np.pi*O_2/180), width=.008, color=color_refrac, length_includes_head=True)
                dibujar_flecha=False

            # Sólo añadimos a la leyenda el primer rayo refractado
            if i==0: plt.plot(refrac_x, refrac_y, color=color_refrac, label='Rayo refractado')
            else: plt.plot(refrac_x, refrac_y, color=color_refrac)
        else:   
            if dibujar_flecha==True and i>0:
                ax.arrow( refrac_x[0], refrac_y[0], 0.02*np.sin(np.pi*O_1/180), -0.02*np.cos(np.pi*O_1/180), width=.008, color=color_refrac, length_includes_head=True)
            #break

        # Rayos reflejados de los refractados
        O_1=O_2
        if i>0:
            longitud_rayos = (longitud_segmentos - refrac_y[1]) / np.sin(np.pi*O_1/180)
            reflejado_x = [longitud_rayos * np.sin(np.pi*O_1/180) + refrac_x[1], refrac_x[0]]
            reflejado_y = [longitud_rayos * np.cos(np.pi*O_1/180) + refrac_y[1], refrac_y[0]]
            
            ax.vlines(refrac_x[0], -longitud_segmentos/2 + refrac_y[0], longitud_segmentos/2 + refrac_y[0], color='grey', linestyles='dashed') # vertical

            ax.plot(reflejado_x, reflejado_y, color=color_reflexion)
            #ax.arrow( (reflejado_x[0]+reflejado_x[1])/2, (reflejado_y[0]+reflejado_y[1])/2, 0.02*np.sin(np.pi*O_1/180), 0.02*np.cos(np.pi*O_1/180),
            #        width=.008, color=color_reflexion, length_includes_head=True)

    ax.legend(fontsize=16, loc=1)
    
    return fig



# ----------------------------------------------------------------------------------- SIMULACIÓN --------------------------------------------------------------------------

# Parámetros iniciales
COL1, COL2 = st.columns(2)
col1, col2 = COL1.columns(2) 
n_1 = col1.number_input('Índice de refracción del medio SUPERIOR', 1.,5., value = 1.,format='%.3f')
n_x = col1.number_input('Índice de refracción del medio INFERIOR', 1.,5., value = 1.2, format='%.3f')

O_1 = col2.slider('Ángulo de incidencia (º)', 0, 90, value=60)
n_medios = col2.slider('Número de medios', 2,100)
n_medios-=1
COL2.pyplot(simulador_snell(n_1, n_x, O_1, n_medios, False))

# --------------------------------------------------------------------------- CUESTIONARIO -------------------------------------------------------------------------------
#st.divider()
#import sys
#sys.path.insert(0, 'Artículos/Cuestionario/')
#
#import cuestionario
#cuestionario.mostrar_cuestionario()

# ----------------------------------------------------------------------------- FOOTER ----------------------------------------------------------------------------------




