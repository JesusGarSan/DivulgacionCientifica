import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle

import numpy as np


#------------------------------------- DEFINICIÓN DE FUNCIONES ------------------------------------

def sin(theta):
    return np.sin(theta*np.pi/180)

def cos(theta):
    return np.cos(theta*np.pi/180)

def plot_frame(posiciones, lamina, concentraciones):
    posiciones_ = np.array(posiciones)
    ax.clear()
    #ax.axis('off')
    #ax.set_xticks([])
    #ax.set_yticks([])
    ax.set_xlim(-dim_x/2, dim_x/2)
    ax.set_ylim(0, dim_y)
    ax.scatter(posiciones_[:,0], posiciones_[:,1], s=4)
    ax.add_patch(Rectangle((lamina.posicion-lamina.anchura, 0), lamina.anchura*2, lamina.altura, facecolor='gray'))
    ax.vlines(lamina.posicion, 0,100, colors='black')

    #ax[1].clear()
    #ax[1].set_xlim(0, dim_x)
    #ax[1].set_ylim(0, dim_y)
    #ax[1].plot(concentraciones)


    plt.show()

def animate(frame):
    liberar = lamina.mover()

    posiciones = []
    concentraciones = [0]*300
    for particula in particulas:
        particula.mover(lamina)
        posiciones.append(particula.posicion)
        if liberar: particula.libre = True
        
        
        index = int(particula.posicion[0])
        if index >=150: index = 150 -1
        if index <= -150: index = 0
        index+=150
        concentraciones[index] +=1
    
    import copy
    temp_lamina = copy.deepcopy(lamina)
    temp_lamina.mover()

    plot_frame(posiciones, temp_lamina, concentraciones)



#------------------------------------- DEFINICIÓN DE CLASES ------------------------------------

# Clase lámina 
class lámina:
    def __init__(self, posicion, anchura, altura, rango, velocidad_oscilacion, velocidad_desplazamiento = 0):
        self.posicion = posicion
        self.anchura = anchura
        self.altura = altura
        self.extremos = [posicion - anchura/2, posicion + anchura/2]
        self.rango = rango
        self.velocidad_oscilacion = velocidad_oscilacion
        self.velocidad_desplazamiento = velocidad_desplazamiento

        self.last_max = rango/2

    def mover(self):
        liberar = False
        if self.posicion <= self.last_max and self.posicion >= self.last_max-self.rango*2:      
            self.posicion += self.velocidad_oscilacion + self.velocidad_desplazamiento
        else:
            if self.velocidad_oscilacion > 0: self.last_max = self.posicion + self.velocidad_desplazamiento

            self.velocidad_oscilacion *=-1
            self.posicion += self.velocidad_oscilacion + self.velocidad_desplazamiento
            liberar = True

        self.extremos = [self.posicion - self.anchura/2, self.posicion + self.anchura/2]
        
        return liberar


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
        extremos_lamina = lamina.extremos

        # Choque contra la lámina vibrante
        if (nueva_posicion[0] >= extremos_lamina[0] and nueva_posicion[0] <= extremos_lamina[1]) and self.libre==True:
            
            # Método de "empujar las partículas"
            #self.velocidad = lamina.velocidad
            #self.angulo = 0
            #self.direccion = np.array([1, 0]).T 
            #self.posicion += self.direccion*self.velocidad
            
            # Método de "clonar las partículas". Usamos este para evitar que la lámina se quede sin nada que empujar
            self.libre = False
            nueva_particula = particle(self.posicion, 0, lamina.velocidad_oscilacion)
            

            if lamina.velocidad_oscilacion > 0: nueva_particula.posicion[0] = np.clip(nueva_particula.posicion[0], lamina.extremos[1], dim_x/2)
            if lamina.velocidad_oscilacion < 0: nueva_particula.posicion[0] = np.clip(nueva_particula.posicion[0], -dim_x/2, lamina.extremos[0])

            #nueva_particula.posicion[0] = lamina.posicion

            nueva_particula.libre = False

            particulas.append(nueva_particula)
        # Desplazamiento normal
        elif nueva_posicion[0] < dim_x and nueva_posicion[0]>0 and nueva_posicion[1] < dim_y and nueva_posicion[1] > 0:
            self.posicion[0] += self.direccion[0]*self.velocidad
            self.posicion[1] += self.direccion[1]*self.velocidad

        # Choque contra las paredes
        else: self.rebotar()

        #if lamina.velocidad < 0: self.libre = True

    def rebotar(self):
        #if self.posicion[0]<=-dim_x/2 :#or self.posicion[0]>=dim_x/2: # Rebote con la vertical
        #    self.angulo = + 180 - self.angulo
        if self.posicion[1]<=0 or self.posicion[1] >= dim_y:
            self.angulo = - self.angulo

        self.direccion = np.array([cos(self.angulo), sin(self.angulo)])#.T[0]
        self.posicion += self.direccion*self.velocidad#.T[0]

        # self.posicion[0] = np.clip(self.posicion[0], -dim_x/2, dim_x/2)
        self.posicion[1] = np.clip(self.posicion[1], 0.0, dim_y)
        




#-------------------------------------

np.random.seed(1)

global dim_x, dim_y

dim_x = 300
dim_y = 50
densidad = 1.0
rango = 10
anchura = 4.0
particulas = []
posiciones = []

lamina = lámina(posicion = 0, anchura= anchura, altura=dim_y, rango=rango, velocidad_oscilacion=2.0, velocidad_desplazamiento=.0)
for x in range(-dim_x//2, dim_x//2)[:]:
    #if x > lamina.posicion and x < lamina.posicion+lamina.anchura: continue
    for y in range(dim_y):
        if np.random.rand(1)*100 <= densidad:
            angulo = np.random.rand(1)[0]*360
            velocidad = np.random.rand(1)[0]*0.1+0.1
            particulas.append(particle([x,y], angulo, velocidad))

            posiciones.append([x,y])

#particulas = [particle([50.0,30.0], 160.0, 1.0)]

# Crea la figura y el objeto de ejes
fig, ax = plt.subplots(1, figsize=(15,5))
fig.set_size_inches(10,5, forward=True)

# Crea la animación con dos frames
ani = animation.FuncAnimation(fig, animate, frames=100, interval=10, repeat=False)
# Muestra la animación
plt.show()

# Guarda la animación
print('Creating animation')
ani.save('animacion_4.gif', writer='pillow', fps=30)
print('Animation created')

# Mostrar en streamlit #
#import streamlit as st
#import streamlit.components.v1 as components
#components.html(ani.to_jshtml(), height=1000, width=1000)
########################