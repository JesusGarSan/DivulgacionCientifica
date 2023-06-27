import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle

import numpy as np


#------------------------------------- DEFINICIÓN DE FUNCIONES ------------------------------------

def sin(theta):
    return np.sin(theta*np.pi/180)

def cos(theta):
    return np.cos(theta*np.pi/180)

def plot_frame(posiciones, lamina):
    posiciones_ = np.array(posiciones)
    ax.clear()
    ax.set_xlim(0, dim_x - 10)
    ax.set_ylim(0, dim_y)
    ax.scatter(posiciones_[:,0], posiciones_[:,1], s=2)
    ax.add_patch(Rectangle((lamina.posicion-lamina.anchura/2, 0), lamina.anchura, lamina.altura, facecolor='gray'))
    plt.show()

def animate(frame):
    lamina.mover()
    posiciones = []
    for particula in particulas:
        particula.mover(lamina)
        posiciones.append(particula.posicion)
    
    plot_frame(posiciones, lamina)



#------------------------------------- DEFINICIÓN DE CLASES ------------------------------------

# Clase lámina 
class lámina:
    def __init__(self, posicion, anchura, altura, rango, velocidad):
        self.posicion = posicion
        self.anchura = anchura
        self.altura = altura
        self.rango = rango
        self.velocidad = velocidad

    def mover(self):
        if self.posicion <= self.rango and self.posicion >= -self.rango:    
            self.posicion += self.velocidad
        else:
            self.velocidad *=-1
            self.posicion += self.velocidad

# Clase partícula 
class particle:
    def __init__(self, posicion, angulo, velocidad):
        self.posicion = np.array(posicion)*1.0
        self.angulo = angulo
        self.direccion = np.array([cos(angulo), sin(angulo)])#.T[0]
        self.velocidad = velocidad
        self.libre = True

    def mover(self, lamina):
        nueva_posicion = self.posicion + self.direccion*self.velocidad#.T[0]
        extremo_lamina = lamina.posicion + lamina.anchura/2

        # Choque contra la lámina vibrante
        if nueva_posicion[0] <= extremo_lamina and lamina.velocidad >= 0 and self.libre==True:
            
            # Método de "empujar las partículas"
            #self.velocidad = lamina.velocidad
            #self.angulo = 0
            #self.direccion = np.array([1, 0]).T 
            #self.posicion += self.direccion*self.velocidad
            
            # Método de "clonar las partículas". Usamos este para evitar que la lámina se quede sin nada que empujar
            self.libre = False
            nueva_particula = particle(self.posicion, 0, lamina.velocidad)
            nueva_particula.libre = False

            particulas.append(nueva_particula)
        # Desplazamiento normal
        elif nueva_posicion[0] < dim_x and nueva_posicion[0]>0 and nueva_posicion[1] < dim_y and nueva_posicion[1] > 0:
            self.posicion[0]+= self.direccion[0]*self.velocidad
            self.posicion[1]+= self.direccion[1]*self.velocidad

        # Choque contra las paredes
        else: self.rebotar()

        if lamina.velocidad < 0: self.libre = True

    def rebotar(self):
        if self.posicion[0]<=0 :#or self.posicion[0]>=dim_x: # Rebote con la vertical
            self.angulo = + 180 - self.angulo
        elif self.posicion[1]<=0 or self.posicion[1]>=dim_y:
            self.angulo = - self.angulo

        self.direccion = np.array([cos(self.angulo), sin(self.angulo)])#.T[0]
        self.posicion += self.direccion*self.velocidad#.T[0]

        self.posicion[0] = np.clip(self.posicion[0], 0.0, dim_x)
        self.posicion[1] = np.clip(self.posicion[1], 0.0, dim_y)
        




#-------------------------------------

np.random.seed(1)

global dim_x, dim_y

dim_x = 300
dim_y = 50
densidad = 50.0
rango = 10
particulas = []
posiciones = []

for x in range(dim_x)[:]:
    for y in range(dim_y):
        if np.random.rand(1)*100 <= densidad:
            angulo = np.random.rand(1)[0]*360
            velocidad = np.random.rand(1)[0]*0.1+0.1
            particulas.append(particle([x,y], angulo, velocidad))

            posiciones.append([x,y])

#particulas = [particle([50.0,30.0], 160.0, 1.0)]
lamina = lámina(posicion=-5.0, anchura=22.0, altura=dim_y, rango=rango, velocidad=2.0)

# Crea la figura y el objeto de ejes
fig, ax = plt.subplots()

# Crea la animación con dos frames
ani = animation.FuncAnimation(fig, animate, frames=250, interval=50, repeat=False)
# Muestra la animación
plt.show()

# Guarda la animación
ani.save('animacion.gif', writer='pillow')

# Mostrar en streamlit #
#import streamlit as st
#import streamlit.components.v1 as components
#components.html(ani.to_jshtml(), height=1000, width=1000)
########################