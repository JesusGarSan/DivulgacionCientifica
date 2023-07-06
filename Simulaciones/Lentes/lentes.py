
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


def snell(n_1, n_2, O_1):
    if abs(n_1/n_2 * np.sin(O_1/180*np.pi) )>1: return None
    return np.arcsin( n_1/n_2 * np.sin(O_1/180*np.pi) ) * 180/np.pi

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



class lente:
    def __init__(self, focal, posicion, radio):
        self.focal = focal # if focal < 0: divergente ; if focal > 0: convergente
        self.posicion = posicion
        self.radio = radio


    






