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
    if np.abs(value1 - value2) <=0.01: return True
    else: return False

def plot_frame(posiciones, lamina, concentraciones):
    posiciones_ = np.array(posiciones)
    ax.clear()
    ax.set_frame_on=False
    #ax.axis('off')
    #ax.set_xticks([])
    #ax.set_yticks([])
    ax.set_xlim(-dim_x/2, dim_x/2)
    ax.set_ylim(0, dim_y)
    ax.add_patch(Rectangle((lamina.posicion-lamina.anchura, 0), lamina.anchura*2, lamina.altura, facecolor='gray'))
    if len(posiciones)>0:
        ax.scatter(posiciones_[:,0], posiciones_[:,1], s=4)
        ax.scatter(posiciones_[490:500,0], posiciones_[490:500,1], s=14, c='red') # Coloreamos un punto arbitrario rojo
    #ax.vlines(lamina.posicion, 0,100, colors='black')
    #ax.vlines(lamina.extremos[1], 0,100, colors='red')

    #ax[1].clear()
    #ax[1].set_xlim(0, dim_x)
    #ax[1].set_ylim(0, dim_y)
    #ax[1].plot(concentraciones)


    plt.show()

def animate(frame):
    time_interval = 1e-5 # Cada frame equivale a 1 micro segundo
    time = frame * time_interval
    lamina.mover(time)

    posiciones = []
    concentraciones = [0]*300
    prev_particulas = particulas
    for particula in prev_particulas:
        particula.mover(lamina)
        posiciones.append(particula.posicion)
        particula.time += time_interval

    
    import copy
    temp_lamina = copy.deepcopy(lamina)
    temp_lamina.mover(frame)

    plot_frame(posiciones, lamina, concentraciones)


def random_grid(n_points, dim_x = 100, dim_y = 100):
    points = []
    for _ in np.arange(n_points):
        x = np.random.rand(1)[0] * dim_x*2 - dim_x
        y = np.random.rand(1)[0] * dim_y*2 - dim_y
        points.append([x,y])

    return np.array(points)

#------------------------------------- DEFINICIÓN DE CLASES ------------------------------------

# Clase lámina 
class lámina:
    def __init__(self, posicion, anchura, altura, amplitud, frecuencia, desfase):
        self.posicion = posicion
        self.anchura = anchura
        self.altura = altura
        self.extremos = [posicion - anchura, posicion + anchura]

        self.amplitud = amplitud
        self.frecuencia = frecuencia
        self.periodo = 1/frecuencia
        self.desfase = desfase # En radianes!!

    def x(self, t):
        A = self.amplitud
        w = 2* np.pi / self.periodo
        phi = self.desfase

        x = self.posicion + A * np.cos(w*t + phi)

        return x

    def mover(self, time):
        self.posicion = self.x(time)
        self.extremos = [self.posicion - self.anchura, self.posicion + self.anchura]
        


# Clase partícula 
class particle:
    def __init__(self, posicion, angulo, velocidad, amplitud, frecuencia, desfase):
        self.posicion = np.array(posicion)*1.0
        self.posicion_inicial = self.posicion
        self.angulo = angulo
        self.direccion = np.array([cos(angulo), sin(angulo)])#.T[0]
        self.direccion[1] = 0 # CORRECIÓN TEMPORAL HASTA Q DECIDA Q HCAER CON LOS REBOTES
        self.velocidad = velocidad
        self.libre = True

        self.MAS = False
        self.amplitud = amplitud
        self.frecuencia = frecuencia
        self.periodo = 1/frecuencia
        self.desfase = desfase # En radianes!!
        self.time =0

    def x(self, t):
        A = self.amplitud
        w = 2* np.pi / self.periodo
        phi = self.desfase

        if self.MAS == True:
            x = self.posicion_inicial[0] + A * np.cos(w*self.time + phi)
        else:
            x = self.posicion[0]

        aux = w*t + phi / 2*np.pi
        if approx(aux, int(aux), 1): self.MAS = False
            
        return x

    def mover(self, lamina):
        if self.MAS ==True:
            self.posicion[0] = self.x(self.time) + self.direccion[0]*self.velocidad
            self.posicion[1] += self.direccion[1] * self.velocidad

        elif self.MAS==False:
           #Comprobamos si hay alguna partícula de aprox el mismo valor de x que la particula actual para iniciar su MAS
            for objeto in particulas:
                if objeto.posicion[0]  <= self.posicion[0] and objeto.posicion[0]+ .5 > self.posicion[0] and objeto.MAS == True and objeto.desfase + objeto.frecuencia*2*np.pi*self.time > np.pi:
                    self.time = 0
                    self.posicion_inicial = self.posicion
                    self.MAS = True
                    self.desfase = 0
                    break

        if self.posicion[0] <= lamina.extremos[1]:
            self.posicion[0] = np.clip(self.posicion[0], lamina.extremos[1], dim_x/2)
            self.desfase = np.pi
            self.MAS = True

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

np.random.seed(2)

global dim_x, dim_y

dim_x = 300
dim_y = 20
anchura = 4.0
amplitud = 3
frecuencia = 5000
desfase = 0

lamina = lámina(0 -anchura, anchura, dim_y, amplitud, frecuencia, desfase)
posiciones = random_grid(3000, dim_x, dim_y).tolist()
posiciones = np.where(np.array(posiciones)[0,:], posiciones, posiciones)
particulas = []
#print( np.where(np.array(posiciones)[0,:], posiciones, posiciones))

for posicion in posiciones:
    angulo = np.random.rand(1)[0]*360
    velocidad = np.random.rand(1)[0]*0.05+0.05
    nueva_particula = particle(posicion, angulo, velocidad, amplitud, frecuencia, desfase)
    particulas.append(nueva_particula)

particulas=[]
prev_particulas = particulas

# Crea la figura y el objeto de ejes
fig, ax = plt.subplots(1, figsize=(15,5))
fig.set_size_inches(10,5, forward=True)

# Crea la animación con dos frames
ani = animation.FuncAnimation(fig, animate, frames=300, interval=100, repeat=False)
# Muestra la animación
plt.show()

# Guarda la animación
print('Creating animation')
ani.save('./Simulaciones/Doppler/partículas libres.gif', writer='pillow', fps=15)
print('Animation created')

# Mostrar en streamlit #
#import streamlit as st
#import streamlit.components.v1 as components
#components.html(ani.to_jshtml(), height=1000, width=1000)
########################
