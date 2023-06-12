import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm



import streamlit as st

st.set_page_config(layout='wide')


#------------------- DEFINICIÓN DE FUNCIONES -----------------------

# Ley de Snell
# n_1 * sin(O_1) = n_2 * sin(O_2)
def snell(n_1, n_2, O_1):
    if abs(n_1/n_2 * np.sin(O_1/180*np.pi) )>1: return None
    return np.arcsin( n_1/n_2 * np.sin(O_1/180*np.pi) ) * 180/np.pi


# -------------------------------------------------------------------

st.title(' Los fantasmas de la carretera')
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

COL1.markdown('''A la derecha verás una simulación de "La ley de Snell". ¡Siéntete libre de jugar con ella mientras lees la explicación!
                ''')

# Parámetros iniciales
col1, col2 = COL2.columns(2) 
n_1 = col1.number_input('Índice de refracción del medio SUPERIOR', 1.,5., value = 1.4,format='%.3f')
n_x = col1.number_input('Índice de refracción del medio INFERIOR', 1.,5., value = 1.2, format='%.3f')

O_1 = col2.slider('Ángulo de incidencia (º)', 0, 90, value=30)
n_medios = col2.slider('Número de medios', 2,100)
n_medios-=1

incremento_n = (n_x - n_1)/n_medios

fig, ax = plt.subplots(figsize=(12,10))
ax.axis('off')
ax.set_xlim(-1,1)
ax.set_ylim(-1,1)

if n_medios == 1:
    ax.text(-1,.85, 'Medio 1', fontsize=24)
    ax.text(-1,-.85, 'Medio 2', fontsize=24)

# Rayo incidente
longitud_rayos = 1
inc_x = [-longitud_rayos * np.sin(np.pi*O_1/180),0]
inc_y = [longitud_rayos * np.cos(np.pi*O_1/180),0]

ax.fill_between([-1,1], [1,1], color='white') # medio 1
ax.vlines(0, -1, 1, color='grey', linestyles='dashed') # vertical
ax.plot(inc_x, inc_y, color='blue', label='Rayo incidente')

# Rayo Reflejado

longitud_rayos = .8
reflejado_x = [longitud_rayos * np.sin(np.pi*O_1/180),0]
reflejado_y = [longitud_rayos * np.cos(np.pi*O_1/180),0]

ax.fill_between([-1,1], [1,1], color='white') # medio 1
ax.vlines(0, -1, 1, color='grey', linestyles='dashed') # vertical
ax.plot(reflejado_x, reflejado_y, color='green', label='Rayo reflejado')


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
for i in range(n_medios):
    O_2 = snell(n_1, n_1+(i+1)*incremento_n, O_2)
    if O_2!=None:
        longitud_segmentos = 1/n_medios/np.cos(np.pi*O_2/180)

        refrac_x = [0 + refrac_x[1], refrac_x[1] + longitud_segmentos * np.sin(np.pi*O_2/180)]
        refrac_y = [0 + refrac_y[1], refrac_y[1] + -longitud_segmentos * np.cos(np.pi*O_2/180)]
    
        if i==0: plt.plot(refrac_x, refrac_y, color='red', label='Rayo refractado')
        else: plt.plot(refrac_x, refrac_y, color='red')
    else: break

ax.legend(fontsize=16)
COL2.pyplot(fig)


COL1.markdown(r'''El índice de refracción nos indica cómo viaja la luz en un medio: aire, agua, vidrio, etc. Cualquier cosa por la que pueda pasar la luz.''' )

COL1.markdown(r'''Al pasar de un medio a otro con distinto índice de refracción, la luz se
desvía abruptamente. A esto se le llama "refracción". ''', help='Dependiendo de si el nuevo índice es mayor o menor, la desviación se produce en un sentido u otro. ¡Compruébalo!')

COL1.markdown(r'''Un cambio de medios sucesivo, hace que la luz se "curve", aparentemente.''', help='Prueba a seleccionar un "Número de medios" alto.')

COL1.markdown(r'''La densidad del aire afecta a su índice de refracción. A menor densidad,
menor índice de refracción.''')

COL1.markdown(r''' Al calentarse, el aire se expande, por lo que la densidad del aire caliente
es mayor que la del frío.''')


COL1.markdown(r'''  Es decir: ¡El índice de refracción del aire caliente es menor que el del
aire frío!''')

COL1.latex(r'''
    Temperatura \uparrow \,\, \Longrightarrow densidad \downarrow \,\, \Longrightarrow índice \,\,  refracción \downarrow
''')


st.header('Pero: ¿qué pinta la temperatura aquí?')

st.markdown('')


