import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm



import streamlit as st
import streamlit.components.v1 as com
with open('styles.css') as styles:
    design = styles.read()

st.set_page_config(layout='wide')


#------------------- DEFINICIÓN DE FUNCIONES -----------------------

# Ley de Snell
# n_1 * sin(O_1) = n_2 * sin(O_2)
def snell(n_1, n_2, O_1):
    if abs(n_1/n_2 * np.sin(O_1/180*np.pi) )>1: return None
    return np.arcsin( n_1/n_2 * np.sin(O_1/180*np.pi) ) * 180/np.pi


# -------------------------------------------------------------------

#st.title(' Los fantasmas de la carretera')
com.html(f"""
         <div>
         <style>
         {design}
         </style>
         <h1>
         Los fantasmas de la carretera
         </h1>
         </div>
         """)
COL1, COL2 = st.columns(2)

COL1.image('charco.png')

COL2.markdown('''Cuando vamos por la carretera podemos a veces ver unos curiosos "charcos" de agua en la lejanía. Estos "charcos" se esfuman cuando nos acercamos a ellos, como si se evaporasen en pocos segundos.
                ''')           
COL2.markdown('''Estos charcos se dejan ver más a menudo en los días soleados y calurosos de verano. Aunque sí se dan las condiciones adecuadas, podemos verlos en cualquier momento del año.
                Pero, ¿cuáles son las "condiciones adecuadas"? ¿Qué son si quiera estos "charcos"?.
                ''')
                


st.divider()



st.header('Una simulación vale más que mil palabras')
COL1, COL2 = st.columns(2)

COL1.markdown('''Para entender bien estos charcos tenemos que entender primero cómo viaja la luz y qué es lo que llamamos "índice de refracción". Pero no te preocupes, que no tiene misterio.
                ''')

COL1.markdown('''NOTA:  A la derecha verás una simulación de "La ley de Snell". ¡Siéntete libre de jugar con ella mientras lees la explicación!
                ''')

# Parámetros iniciales
col1, col2 = COL2.columns(2) 
n_1 = col1.number_input('Índice de refracción del medio SUPERIOR', 1.,5., value = 1.,format='%.3f')
n_x = col1.number_input('Índice de refracción del medio INFERIOR', 1.,5., value = 1.2, format='%.3f')

O_1 = col2.slider('Ángulo de incidencia (º)', 0, 90, value=60)
n_medios = col2.slider('Número de medios', 2,100)
n_medios-=1

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
colormap = cm.get_cmap('Wistia', 256)
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

        if n_medios == 1:
            divisor = 2
            if refrac_x[1] > 0.5: divisor = refrac_x[1]*2
            ax.arrow( (refrac_x[0]+refrac_x[1])/divisor, (refrac_y[0]+refrac_y[1])/divisor, 0.02*np.sin(np.pi*O_2/180), -0.02*np.cos(np.pi*O_2/180), width=.008, color=color_refrac, length_includes_head=True)
            dibujar_flecha=False

        if (refrac_x[0]>0.5 or refrac_y[0]<-0.5) and dibujar_flecha:
            ax.arrow( refrac_x[0], refrac_y[0], 0.02*np.sin(np.pi*O_2/180), -0.02*np.cos(np.pi*O_2/180), width=.008, color=color_refrac, length_includes_head=True)
            dibujar_flecha=False

        if i==0: plt.plot(refrac_x, refrac_y, color=color_refrac, label='Rayo refractado')
        else: plt.plot(refrac_x, refrac_y, color=color_refrac)
    else:   
        if dibujar_flecha==True and i>0:
            ax.arrow( refrac_x[0], refrac_y[0], 0.02*np.sin(np.pi*O_1/180), -0.02*np.cos(np.pi*O_1/180), width=.008, color=color_refrac, length_includes_head=True)
        break

ax.legend(fontsize=16)
COL2.pyplot(fig)

COL1.divider()
COL1.markdown(r'''El índice de refracción nos indica cómo viaja la luz en un medio: aire, agua, vidrio, etc. Cualquier cosa por la que pueda pasar la luz.''' )

COL1.markdown(r'''Al pasar de un medio a otro con distinto índice de refracción suceden dos cosas:''')
COL1.markdown(r'''  - La luz que incide se refleja, regresando al medio del que provenía pero en otra dirección. A esto le llamamos "Reflexión".''', help='El ángulo entre la vertical y el rayo que incide es el mismo que hay entre la vertical y el rayo reflejado. ¡Compruébalo!')

COL1.markdown(r'''- La luz pasa al otro medio, desviándose abruptamente en el proceso. A este fenómeno le llamamos "Refracción". ''', help='Dependiendo de si el nuevo índice es mayor o menor, la desviación se produce en un sentido u otro. ¡Compruébalo!')

COL1.markdown(r'''Un cambio de medios sucesivo, hace que la luz se "curve", aparentemente.''', help='Prueba a seleccionar un "Número de medios" alto.')

COL1.markdown(r'''La densidad del aire afecta a su índice de refracción. A menor densidad,
menor índice de refracción.''')

COL1.markdown(r''' Al calentarse, el aire se expande, por lo que la densidad del aire caliente
es menor que la del frío.''')


COL1.markdown(r'''  Es decir: ¡El índice de refracción del aire caliente es menor que el del
aire frío!''')

COL1.latex(r'''
    Temperatura \uparrow \,\, \Longrightarrow densidad \downarrow \,\, \Longrightarrow índice \,\,  refracción \downarrow
''')


st.header('Pero: ¿qué pinta la temperatura aquí?')

st.markdown('Como hemos visto, medios con diferentes índices de refracción refractan la luz de distinta manera (de forma más o menos pronunciada y en un sentido u otro).')
st.markdown('El asfalto de las carreteras suele estar a temperaturas relativamente altas, tanto por el caso de los coches como por el brillo del Sol (¡más aun en verano!).')
st.markdown('De este modo, el alfalto hace como de sartén para el aire que lo toca, haciendo que el aire que está más cerca del asfalto se encuentre muy caliente, y progresivamente más frío según nos elevamos.')
st.markdown('Hemos dicho que el aire a mayor temperatura cuenta con un índice de refracción menor. ¿Qué pasará si en nuestra simulación indicamos un índice de refracción alto para el Medio 1 (aire frío, lejos del asfalto), y un índice de refracción bajo para el medio más cercano al asfalto (aire caliente)?. ¡Haz la prueba!')
st.markdown('Cómo puedes ver, el rayo de luz se eleva con respecto al rayo de luz incidente. Si hacemos mayor la diferencia de los índices de refracción vemos que el efecto se amplifica. Lo mismo pasa en los días calurosos de verano, cuando el asfalto está más caliente.')
st.markdown('¡Podemos ir un paso más allá! Si aumentamos el número de medios, simularemos las distintas capas de aire que se forman: más calientes abajo, más frías arriba. Podemos ver como las distintas capas de aire hacen que el rayo de luz se refracte sin llegar a tocar el suelo.')
st.markdown('Si la elevación del rayo de luz debido a la refracción es la suficiente, podemos llegar a ver un rayo de luz proveniente del cielo como si vienese del suelo, ¡al igual que pasa con el reflejo de un charco!')

st.markdown('')


