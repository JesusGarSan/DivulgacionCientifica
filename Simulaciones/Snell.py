# ----------------------------------------------------------------------- IMPORTACIÓN DE LIBRERÍAS ------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colormaps
import copy


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

class rayo:
    def __init__(self, origen, longitud ,theta, sentido):
        self.origen = np.array(origen)
        self.longitud = longitud
        self.theta = theta
        self.extremo = np.array(polares(self.origen, longitud, theta)) + np.array(self.origen)

        self.sentido = sentido

    def stats(self):
        print(f"""
              origen: {self.origen}
              extremo: {self.extremo}
              ángulo respecto a la vertical: {self.theta}
              sentido: {self.sentido}
              """)

    def recortar(self, fronteras, plot_colision):

        recortado = False
        fronteras = np.array(fronteras)
        # Localizamos las fronteras que se encuentran entre el origen y el extremo actual
        if self.sentido== +1:
            fronteras_intermedias = np.where((self.origen[1]<fronteras) & (self.extremo[1]>fronteras))[0]
        if self.sentido== -1:
            fronteras_intermedias = np.where((self.origen[1]>fronteras) & (self.extremo[1]<fronteras))[0]
        # Reasiganmos el nuevo valor de extremo (si se han encontrado fronteras intermedias)
        if  len(fronteras_intermedias) > 0:
            print(fronteras[fronteras_intermedias])
            if self.sentido== +1: indice_nuevo_extremo = fronteras_intermedias[len(fronteras_intermedias)-1]
            if self.sentido== -1: indice_nuevo_extremo = fronteras_intermedias[0]
            nuevo_extremo = fronteras[indice_nuevo_extremo]
           
            self.extremo[0] = nuevo_extremo / self.extremo[1] * self.extremo[0]
            self.extremo[1] = nuevo_extremo

            

            recortado = True


        if plot_colision == True:
            longitud_segmentos = (fronteras[1] - fronteras[0])*1.5
            plt.vlines(self.extremo[0], -longitud_segmentos/2 + self.extremo[1], longitud_segmentos/2 + self.extremo[1], color='grey', linestyles='dashed') # vertical

        return recortado


            
    def plot_rayo(self, color, arrow):
        x=[self.origen[0], self.extremo[0]]
        y=[self.origen[1], self.extremo[1]]
        plt.plot(x, y, color=color, label='Rayo incidente')
        if arrow==True:
            if self.sentido == -1: plt.arrow( (x[0]+x[1])/2, (y[0]+y[1])/2, 0.02*np.sin(np.pi*self.theta/180), -0.02*np.cos(np.pi*self.theta/180), width=.008, color=color, length_includes_head=True)
            if self.sentido == +1: plt.arrow( (x[0]+x[1])/2, (y[0]+y[1])/2, 0.02*np.sin(np.pi*self.theta/180), +0.02*np.cos(np.pi*self.theta/180), width=.008, color=color, length_includes_head=True)


    def reflejar(self):
        rayo_reflejado = rayo(origen= self.extremo, longitud=3 ,theta= self.theta, sentido=-self.sentido)
        return rayo_reflejado

    def refractar(self, n_1, n_2):
        theta = snell(n_1, n_2, self.theta)
        if theta!=None:
            rayo_refractado = rayo(origen= self.extremo, longitud=3 ,theta= theta, sentido=self.sentido)
            rayo_refractado.extremo[1] = np.abs(rayo_refractado.extremo[1]) * rayo_refractado.sentido

            rayo_refractado.extremo[1]+=self.extremo[1]
            rayo_refractado.extremo[0]+=self.extremo[0]

            return rayo_refractado
        else: return None

# Coordenadas polares

def polares(centro, r, theta):
    #theta-=90
    extremo=[0,0]
    extremo[0] =  r*np.sin(np.pi*theta/180) #+ centro[0]
    extremo[1] =  r*np.cos(np.pi*theta/180) #+ centro[1]

    return extremo

# Ley de Snell
# n_1 * sin(O_1) = n_2 * sin(O_2)
def snell(n_1, n_2, O_1):
    if abs(n_1/n_2 * np.sin(O_1/180*np.pi) )>1: return None
    return np.arcsin( n_1/n_2 * np.sin(O_1/180*np.pi) ) * 180/np.pi


#Dibujado y ploteo del simulador
def simulador_snell(n_1, n_x, O_1, n_medios, plot_reflexiones):


    print('------------------------------------------------')

    fig, ax = plt.subplots(figsize=(12,10))
    ax.axis('off')
    ax.set_xlim(-1,1)
    ax.set_ylim(-1,1)

    ax.text(-1,.85, 'Medio 1', fontsize=24)
    ax.text(-1,-.99, f'Medio {n_medios+1}', fontsize=24)
    ax.fill_between([-1,1], [1,1], color='white') # medio 1

    # Medios
    colormap = colormaps.get_cmap('Wistia')
    step_1=0
    fronteras = [step_1]
    n = [n_1]
    incremento_n = (n_x - n_1)/n_medios
    for i in range(n_medios):
        step_2=-(i+1)/n_medios
        ax.fill_between([-1, 1], [step_1, step_1], [step_2, step_2], color=colormap(i/n_medios)) # medio 2
        step_1=step_2
        fronteras.append(step_1)
        n.append(n[len(n)-1] + incremento_n)

    # Rayo incidente (Primer rayo)
    longitud_rayos = 1 # Longitud máxima

    x = -np.sin(np.pi*O_1/180)
    y = +np.cos(np.pi*O_1/180)

    rayo_incidente = rayo(origen = [x,y], longitud = longitud_rayos, theta = O_1, sentido=-1) #Creamos el rayo como objeto
    rayo_incidente.extremo =[0,0]    
    rayo_incidente.recortar(fronteras, True)
    rayo_incidente.plot_rayo('blue', arrow= True)


    # Primer rayo reflejado
    rayo_reflejado = rayo_incidente.reflejar()
    rayo_reflejado.recortar(fronteras, plot_colision=False)
    rayo_reflejado.plot_rayo('green', arrow=True)


    # Primer rayo refractado
    rayo_refractado = rayo_incidente.refractar(n[0], n[1])
    rayo_refractado.recortar(fronteras, True)
    rayo_refractado.plot_rayo('red', arrow=True)

    rayo_reflejado = rayo_refractado.reflejar()
    rayo_reflejado.recortar(fronteras, plot_colision=False)
    rayo_reflejado.plot_rayo('green', arrow=True)

    # Primer rayo refractado
    rayo_refractado_2 = rayo_refractado.refractar(n[1], n[2])
    rayo_refractado_2.recortar(fronteras, True)
    rayo_refractado_2.plot_rayo('red', arrow=True)
    print(f"refractado angulo: {rayo_refractado_2.theta}")

    rayo_reflejado_2 = rayo_refractado_2.reflejar()
    rayo_reflejado_2.recortar(fronteras, plot_colision=False)
    rayo_reflejado_2.plot_rayo('green', arrow=True)
    print(f"refractado angulo: {rayo_reflejado_2.theta}")
    rayo_reflejado_2.stats()

    #aux_rayo_incidente = copy.deepcopy(rayo_incidente)
    #for i in range (n_medios):


    #    # Refracciones
    #    rayo_refractado = aux_rayo_incidente.refractar(n[i], n[i+1] )
    #    if rayo_refractado!=None:
    #        rayo_refractado.recortar(fronteras, True)
    #        rayo_refractado.plot_rayo('red', arrow= False)
    #    
    #        aux_rayo_incidente = copy.deepcopy(rayo_refractado)

    #    # Reflexiones
    #    rayo_reflejado = aux_rayo_incidente.reflejar()
    #    #rayo_reflejado.recortar(fronteras, plot_colision=True)
    #    rayo_reflejado = aux_rayo_incidente.reflejar()
    #    rayo_reflejado.plot_rayo('green', arrow=True)





    centro = [0, -0.5]
    print(polares(centro, 1 ,90))
    rayo_test = rayo(origen=centro, longitud=0.2, theta=120, sentido = 1)
    rayo_test.plot_rayo('purple', True)


    return fig

    
    inc_x = [extremos[0], 1]
    inc_y = [extremos[1], -1]

    #inc_x = [-longitud_rayos * np.sin(np.pi*O_1/180),0]
    #inc_y = [longitud_rayos * np.cos(np.pi*O_1/180),0]

    color_incidente='blue'

    ax.fill_between([-1,1], [1,1], color='white') # medio 1
    ax.vlines(0, -1, 1, color='grey', linestyles='dashed') # vertical
    ax.plot(inc_x, inc_y, color=color_incidente, label='Rayo incidente')
    ax.arrow( (inc_x[0]+inc_x[1])/2, (inc_y[0]+inc_y[1])/2, 0.02*np.sin(np.pi*O_1/180), -0.02*np.cos(np.pi*O_1/180), width=.008, color=color_incidente, length_includes_head=True)
    return fig
    # Rayo Reflejado

    longitud_rayos = .8
    reflejado_x = [longitud_rayos * np.sin(np.pi*O_1/180),0]
    reflejado_y = [longitud_rayos * np.cos(np.pi*O_1/180),0]

    color_reflexion = 'green'

    ax.vlines(0, -1, 1, color='grey', linestyles='dashed') # vertical
    ax.plot(reflejado_x, reflejado_y, color=color_reflexion, label='Rayo reflejado')
    ax.arrow( (reflejado_x[0]+reflejado_x[1])/2, (reflejado_y[0]+reflejado_y[1])/2, 0.02*np.sin(np.pi*O_1/180), 0.02*np.cos(np.pi*O_1/180),
            width=.008, color=color_reflexion, length_includes_head=True)





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




