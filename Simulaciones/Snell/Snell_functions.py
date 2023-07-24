# ----------------------------------------------------------------------- IMPORTACIÓN DE LIBRERÍAS ------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colormaps
import copy


import streamlit as st
import streamlit.components.v1 as com

import os


#------------------------------------------------------------------------- DEFINICIÓN DE FUNCIONES ------------------------------------------------------------------------

# Coordenadas polares
def polares(centro, r, theta):
    extremo=[0,0]
    extremo[0] =  r*np.sin(np.pi*theta/180)
    extremo[1] =  r*np.cos(np.pi*theta/180)

    return extremo

class rayo:
    def __init__(self, origen, longitud ,theta, sentido):


        self.origen = np.array(origen)
        self.longitud = longitud
        self.theta = theta
        self.sentido = +1
        if 90 < self.theta and self.theta < 270: self.sentido = -1        
        self.extremo = np.array(polares(self.origen, longitud, theta)) + np.array(self.origen)


    def stats(self):
        print(f"""
              origen: {self.origen}
              extremo: {self.extremo}
              ángulo respecto a la vertical: {self.theta}
              sentido: {self.sentido}
              """)

            
    def plot_rayo(self, color, arrow):
        x=[self.origen[0], self.extremo[0]]
        y=[self.origen[1], self.extremo[1]]
        plt.plot(x, y, color=color, label='Rayo incidente')
        if arrow==True:
            plt.arrow( (x[0]+x[1])/2, (y[0]+y[1])/2, 0.02*np.sin(np.pi*self.theta/180), +0.02*np.cos(np.pi*self.theta/180), width=.008, color=color, length_includes_head=True)


    def reflejar(self, longitud=10):
        if self.sentido == -1:rayo_reflejado = rayo(origen= self.extremo, longitud=longitud, theta= 180-self.theta, sentido=-self.sentido)
        if self.sentido == +1:
            rayo_reflejado = rayo(origen= self.extremo, longitud=longitud, theta=180-self.theta, sentido=-self.sentido)
            
            rayo_reflejado.extremo[0] += np.abs(rayo_reflejado.origen[0]-rayo_reflejado.extremo[0]) *2
        #rayo_reflejado = rayo(origen= self.extremo, longitud=longitud, theta=180-self.theta, sentido=self.sentido)
        rayo_reflejado.medio = self.medio
        rayo_reflejado.tipo = 'Reflejado' 
        
        return rayo_reflejado

    def refractar(self, n_1, n_2):
        theta = snell(n_1, n_2, self.theta)
        if theta!=None:
            if self.sentido==-1:rayo_refractado = rayo(origen= self.extremo, longitud=10 ,theta= 180-theta, sentido=self.sentido)
            if self.sentido==+1:rayo_refractado = rayo(origen= self.extremo, longitud=10 ,theta= theta, sentido=self.sentido)

            if self.sentido==-1: rayo_refractado.medio = self.medio+1
            if self.sentido==+1: rayo_refractado.medio = self.medio-1

            rayo_refractado.tipo = 'Refractado' 
            return rayo_refractado
        else: return None

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
            if self.sentido== +1: indice_nuevo_extremo = fronteras_intermedias[len(fronteras_intermedias)-1]
            if self.sentido== -1: indice_nuevo_extremo = fronteras_intermedias[0]
            nuevo_extremo = fronteras[indice_nuevo_extremo]

            if self.sentido ==-1:
                self.extremo[0] = np.tan((180-self.theta)*np.pi/180)*np.abs(self.origen[1]-nuevo_extremo)
                self.extremo[0]+=self.origen[0]
            if self.sentido ==+1:
                self.extremo[0] = np.tan(self.theta*np.pi/180)*np.abs(self.origen[1]-nuevo_extremo)
                self.extremo[0]+=self.origen[0]
            self.extremo[1] = nuevo_extremo
            recortado = True

        if plot_colision == True:
            longitud_segmentos = (fronteras[1] - fronteras[0])*1.5
            plt.vlines(self.extremo[0], -longitud_segmentos/2 + self.extremo[1], longitud_segmentos/2 + self.extremo[1], color='grey', linestyles='dashed') # vertical

        return recortado


# Ley de Snell
# n_1 * sin(O_1) = n_2 * sin(O_2)
def snell(n_1, n_2, O_1):
    if abs(n_1/n_2 * np.sin(O_1/180*np.pi) )>1: return None
    return np.arcsin( n_1/n_2 * np.sin(O_1/180*np.pi) ) * 180/np.pi


def incidencia(rayo_incidente, fronteras, n, n_reflexiones, plot_reflexiones, plot_refracciones, max_reflexiones):
    if rayo_incidente.extremo[0]>1: return # Esto hace que no se generen los rayos que se salen horizontalmente de la figura
    if rayo_incidente.extremo[1]==1: return # Esto hace que no se reflejen los rayos que llegan al "techo" del gráfico
    if n_reflexiones >=max_reflexiones: pass
    else:
        #Reflexión
        global primera_incidencia
        if plot_reflexiones or n_reflexiones==0 or primera_incidencia:
            primera_incidencia=False
            if n_reflexiones ==0: rayo_reflejado = rayo_incidente.reflejar(longitud=1.)
            else: rayo_reflejado = rayo_incidente.reflejar(longitud=1.5)
            recurrencia_reflexion = rayo_reflejado.recortar(fronteras, False)

            rayo_reflejado.plot_rayo('green', arrow=True)
            if recurrencia_reflexion:
                incidencia(rayo_reflejado, fronteras, n, n_reflexiones+1, plot_reflexiones, plot_refracciones, max_reflexiones)

    # Refracción
    if plot_refracciones==False and n_reflexiones>1: return
    i_medio = rayo_incidente.medio
    if rayo_incidente.sentido==-1:
        if len(n)<=i_medio+1: return
        rayo_refractado = rayo_incidente.refractar(n[i_medio], n[i_medio+1] )
    if rayo_incidente.sentido==+1:
        if len(n)<=i_medio: return
        rayo_refractado = rayo_incidente.refractar(n[i_medio], n[i_medio-1] )
    if rayo_refractado==None: return # Reflexión Interna Total

    recurrencia_refraccion = rayo_refractado.recortar(fronteras, False)
    rayo_refractado.plot_rayo('red', arrow=True)

    if recurrencia_refraccion:
        if rayo_incidente.tipo=='Refractado' or rayo_incidente.tipo=='Incidente':
            incidencia(rayo_refractado, fronteras, n, n_reflexiones, plot_reflexiones, plot_refracciones, max_reflexiones)
        else:
            incidencia(rayo_refractado, fronteras, n, n_reflexiones+1, plot_reflexiones, plot_refracciones, max_reflexiones)
        if rayo_incidente.tipo=='Reflejado' and rayo_incidente.sentido==+1:
            incidencia(rayo_refractado, fronteras, n, n_reflexiones+1, False, plot_refracciones, max_reflexiones)
    return


#Dibujado y ploteo del simulador
def simulador_snell(n, O_1,  plot_reflexiones, plot_refracciones, max_reflexiones):

    fig, ax = plt.subplots(figsize=(12,10))
    ax.axis('off')
    ax.set_xlim(-1,1)
    ax.set_ylim(-1,1)

    ax.text(-1,.85, 'Medio 1', fontsize=24)
    ax.text(-1,-.99, f'Medio {len(n)}', fontsize=24)
    ax.fill_between([-1,1], [1,1], color='white') # medio 1
    #fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)

    # Medios
    colormap = colormaps.get_cmap('Wistia')
    step_1=0
    fronteras = [1, step_1] # Contar con 1 como frontera permite cortar recortar los rayos salientes
    for i in range(len(n)-1):
        step_2=-(i+1)/(len(n)-1)
        ax.fill_between([-1, 1], [step_1, step_1], [step_2, step_2], color=colormap(i/(len(n)-1))) # medio 2
        step_1=step_2
        fronteras.append(step_1)

    # Rayo incidente (Primer rayo)
    longitud_rayos = 1 # Longitud máxima

    x = -np.sin(np.pi*O_1/180)
    y = +np.cos(np.pi*O_1/180)

    rayo_incidente = rayo(origen = [0,0], longitud = longitud_rayos, theta = 180-O_1, sentido=-1) #Creamos el rayo como objeto
    rayo_incidente.medio = 0   
    rayo_incidente.tipo = 'Incidente' 
    aux = rayo_incidente.extremo
    rayo_incidente.extremo = rayo_incidente.origen
    rayo_incidente.origen = -aux

    rayo_incidente.recortar(fronteras, True)
    rayo_incidente.plot_rayo('blue', arrow= True)


    incidencia(rayo_incidente, fronteras, n, 1, plot_reflexiones, plot_refracciones, max_reflexiones)

    return fig



# ----------------------------------------------------------------------------------- SIMULACIÓN --------------------------------------------------------------------------

# ---------------------------------------------------------------------- CONTENIDO PROPIO DE LA PÁGINA ----------------------------------------------------------------------
def parameter_dashboard(): 
    global primera_incidencia   
    primera_incidencia = True

    column = st.columns(2) 
    # Parámetros iniciales

    n_1 = column[0].number_input('Índice de refracción del medio SUPERIOR', 1.,5., value = 1.,format='%.3f')
    n_x = column[0].number_input('Índice de refracción del medio INFERIOR', 1.,5., value = 1.2, format='%.3f')



    O_1 = column[1].slider('Ángulo de incidencia (º)', 0, 90, value=60)
    n_medios = column[1].slider('Número de medios', 2,40)
    n_medios-=1
    plot_reflexiones=False
    plot_refracciones=False
    if n_medios+1<=4 and n_medios+1>=2:
        plot_reflexiones = column[0].checkbox('Dibujar Reflexiones Internas', help='Esta opción sólo es eligible para 2, 3 o 4 medios')
        if plot_reflexiones:
            plot_refracciones = column[0].checkbox('Dibujar Refracciones Internas')
        if plot_reflexiones==False: plot_refracciones=False
    max_reflexiones=1
    if plot_reflexiones==True:
        max_reflexiones = column[1].number_input('Número de reflexiones internas', min_value=1, max_value=n_medios+1, value=1)
    max_reflexiones+=1

    incremento_n = (n_x - n_1)/n_medios
    n = [n_1]
    for i in range(n_medios):
        n.append(n[len(n)-1] + incremento_n)

    import pandas as pd
    medios = range(len(n)+1)[1:]
    df_n = pd.DataFrame({'Medio': medios, 'Índice de refracción': n})

    with st.expander('Opciones avanzadas:'):
        st.write('Puedes cambiar los valores de los índices de refracción de cada medio manualmente.')
        df_n = st.data_editor(df_n, use_container_width=True, hide_index=True)
        n = df_n['Índice de refracción'].tolist()


    return n, O_1,  plot_reflexiones, plot_refracciones, max_reflexiones

def mostrar_simulacion(n, O_1,  plot_reflexiones, plot_refracciones, max_reflexiones):
    #max_reflexiones = n_medios
    st.pyplot(simulador_snell(n, O_1,  plot_reflexiones, plot_refracciones, max_reflexiones))







# ----------------------------------------------------------------------------- FOOTER ----------------------------------------------------------------------------------



