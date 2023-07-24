import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle

import numpy as np


#------------------------------------- DEFINICIÓN DE FUNCIONES ------------------------------------

def sin(theta):
    return np.sin(theta*np.pi/180)

def cos(theta):
    return np.cos(theta*np.pi/180)

def approx(value1, value2, precision = 0.01): #Devuleve si el valor es aproximadamente igual a otro o no
    if np.abs(value1 - value2) <= precision: return True
    else: return False

def plot_frame(posiciones, lamina):
    posiciones_ = np.array(posiciones)
    ax.clear()
    ax.set_frame_on=False
    ax.axis('off')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(-dim_x/2, dim_x/2)
    ax.set_ylim(0, dim_y)
    #ax.vlines(0, -100, 100, 'red')
    ax.add_patch(Rectangle((lamina.posicion-lamina.anchura, 0), lamina.anchura*2, lamina.altura, facecolor='gray'))
    if len(posiciones) > 0:
        ax.scatter(posiciones_[:,0], posiciones_[:,1], s=4)
        ax.scatter(posiciones_[490:500,0], posiciones_[490:500,1], s=14, c='red') # Coloreamos un punto arbitrario rojo
    plt.show()

def animate(frame):
    time_interval = 1e-5  # Cada frame equivale a 1 micro segundo
    time = frame * time_interval
    lamina.mover_lamina(time)

    posiciones = []
    for particula in particulas:
        particula.mover_particula(lamina)
        posiciones.append(particula.posicion)
        particula.time += time_interval
    
    #import copy
    #temp_lamina = copy.deepcopy(lamina)
    #temp_lamina.mover_lamina(time)

    plot_frame(posiciones, lamina)


def random_grid(n_points, dim_x = 100, dim_y = 100):
    points = []
    for _ in np.arange(n_points):
        x = np.random.rand(1)[0] * dim_x - dim_x/2
        y = np.random.rand(1)[0] * dim_y
        points.append([x,y])

    return np.array(points)

#------------------------------------- DEFINICIÓN DE CLASES ------------------------------------

# Clase lámina 
class lámina:
    def __init__(self, posicion, anchura, altura, amplitud, frecuencia, desfase):
        self.posicion = posicion
        self.posicion_inicial = posicion
        self.anchura = anchura
        self.altura = altura
        self.extremos = [posicion - anchura, posicion + anchura]
        self.time = 0.0

        self.amplitud = amplitud
        self.frecuencia = frecuencia
        self.desfase = desfase # En radianes!!

    def x(self, t):
        A = self.amplitud
        w = 2* np.pi * self.frecuencia
        phi = self.desfase

        x = self.posicion_inicial + A * np.cos(w*t + phi)
        return x

    def mover_lamina(self, time):
        self.posicion = self.x(time)
        self.extremos = [self.posicion - self.anchura, self.posicion + self.anchura]
        


# Clase partícula 
class particle:
    def __init__(self, posicion, angulo, velocidad, amplitud, frecuencia, desfase):
        self.posicion = np.array(posicion)*1.0
        self.posicion_inicial = self.posicion
        self.angulo = angulo
        self.direccion = np.array([cos(angulo), sin(angulo)])#.T[0]
        # Escalamos la dirección
        self.direccion[0]*=dim_x
        self.direccion[1]*=dim_y


        #self.direccion[1] = 0 # CORRECIÓN TEMPORAL HASTA Q DECIDA Q HCAER CON LOS REBOTES
        self.velocidad = velocidad
        self.libre = True

        self.MAS = False
        self.tipo_movimiento = 'confinado'
        self.amplitud = amplitud
        self.frecuencia = frecuencia
        self.periodo = 1/frecuencia
        self.desfase = desfase # En radianes!!
        self.time = 0

    def x(self, t): 
        A = self.amplitud
        w = 2* np.pi * self.frecuencia
        phi = self.desfase

        x = self.posicion_inicial[0] + A * np.cos(w*t + phi)
        return x

    def mover_particula(self, lamina = False):
        tipo = self.tipo_movimiento
        if tipo =='libre':
            self.posicion += self.velocidad*self.direccion
            return
        extremos = lamina.extremos

        if self.posicion[0] < extremos[1] and self.tipo_movimiento!='MAS':
            self.posicion[0] = np.clip(self.posicion[0], extremos[1], dim_x/2)
            self.tipo_movimiento='MAS'
            tipo = self.tipo_movimiento
            self.posicion_inicial = self.posicion
            self.time = 0.0
            #self.frecuencia = lamina.frecuencia
            return

        #if self.posicion[0] < -100:
        #    self.tipo_movimiento = 'MAS'
        #    tipo = self.tipo_movimiento
        #    self.posicion[0] = np.clip(self.posicion[0], -100, dim_x/2)
        #    self.posicion_inicial = self.posicion
        #    self.time = 0.0

        if tipo == 'MAS':
            self.MAS = True
            if lamina != False: self.amplitud = lamina.amplitud
            self.posicion[0] =  self.x(self.time)
            #print(self.time, self.amplitud, self.posicion_inicial[0])

        if tipo =='confinado':
            self.rebotar()
            self.posicion += self.velocidad*self.direccion
            


    def rebotar(self):
        if self.posicion[0]<=-dim_x/2 or self.posicion[0]>=dim_x/2: # Rebote con la vertical
            self.angulo = + 180 - self.angulo
        if self.posicion[1]<=0 or self.posicion[1] >= dim_y:
            self.angulo = - self.angulo

        self.direccion = np.array([cos(self.angulo), sin(self.angulo)])#.T[0]
        self.direccion[0]*=dim_x
        self.direccion[1]*=dim_y
        self.posicion += self.direccion*self.velocidad#.T[0]

        self.posicion[0] = np.clip(self.posicion[0], -dim_x/2, dim_x/2)
        self.posicion[1] = np.clip(self.posicion[1], 0.0, dim_y)
        

#-------------------------------------

np.random.seed(1)
global dim_x, dim_y

dim_x = 300
dim_y = 20
anchura = 4.0
amplitud = 4.0
frecuencia = 5000
desfase = 0

lamina = lámina(0-140, anchura, dim_y, amplitud, frecuencia, desfase)
posiciones = random_grid(300, dim_x, dim_y).tolist()
posiciones = np.where(np.array(posiciones)[0,:], posiciones, posiciones)
particulas = []
#print( np.where(np.array(posiciones)[0,:], posiciones, posiciones))

for posicion in posiciones:
    angulo = np.random.rand(1)[0]*360
    velocidad = np.random.rand(1)[0]*0.05+0.05
    velocidad *=.05
    nueva_particula = particle(posicion, angulo, velocidad, amplitud, frecuencia, desfase)
    particulas.append(nueva_particula)

# Descomentar esta línea para no dibujar las partículas
# particulas=[] 

prev_particulas = particulas

# Crea la figura y el objeto de ejes
fig, ax = plt.subplots(1, figsize=(15,5))
fig.set_size_inches(10,5, forward=True)
fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)

# Crea la animación con dos frames
ani = animation.FuncAnimation(fig, animate, frames=240, interval=100, repeat=False)
# Muestra la animación
plt.show()

# Guarda la animación
print('Creating animation')
ani.save('animación.gif', writer='pillow', fps=15)
print('Animation created')

# Mostrar en streamlit #
#import streamlit as st
#import streamlit.components.v1 as components
#components.html(ani.to_jshtml(), height=1000, width=1000)
########################
