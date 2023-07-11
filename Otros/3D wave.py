from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation




fig = plt.figure(figsize=(8, 8))
ax = plt.axes(projection = '3d')

# Creating array points using numpy


n_inicial_ondas = 15 # Número de ondas que componen la señal
polarizar = False # Aplicar polarizador vertical
desfasar = True # True para el caso de luz natural
desfases = np.random.rand(n_inicial_ondas) * 2*np.pi /5
rotar = 0 #nº de grados a rotar por cada frame
incremento_ondas = 0 #nº de frames tras los cuales se añade una onda (0 para no aplicar incremento). Hace desfasar = False

n_ondas = n_inicial_ondas
lines = []

np.random.seed(1)


def animate(frame, incremento_ondas = incremento_ondas, polarizar = polarizar, desfasar = desfasar, rotar = rotar):

    line = np.linspace(0,6*np.pi, 1000)
    amplitud = 0.6
    x = line
    y = line * 0
    z = np.sin(x + frame/np.pi)*amplitud
    ax.cla()
    
    plt.grid(True)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    global n_ondas
    if incremento_ondas!=0:
        desfasar=False
        if frame % incremento_ondas == 0 :
            n_ondas+=1




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

    ax.view_init(-160, 60-frame/6)

# Crea la animación
ani = FuncAnimation(fig, animate, frames=200, interval=1)


print('Creando animación')

ani.save(f'animación.gif', writer='pillow', fps = 25)

print('Animación creada')
n_ondas = n_inicial_ondas
#plt.show()