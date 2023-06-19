# ----------------------------------------------------------------------- IMPORTACIÓN DE LIBRERÍAS ------------------------------------------------------------------------

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import HTML
import numpy as np
import librosa
import soundfile as sf



import streamlit as st
import streamlit.components.v1 as com


from streamlit_toggle import st_toggle_switch

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

from st_pages import Page, Section, show_pages, show_pages_from_config, add_page_title


#show_pages(
#    [
#        Page("DC.py", "Home", "🏠"),
#        Page("Artículos/Artículos.py","Artículos", icon="📎"),
#        Page("Artículos/Refracción/Refracción.py","Los fantasmas de la carretera", icon="🛣️"),
#        Page("Simulaciones/Snell.py", "Simulaciones", icon="👻"),
#    ]
#)


# ---------------------------------------------------------------------- CONTENIDO PROPIO DE LA PÁGINA ----------------------------------------------------------------------

#------------------------------------------------------------------------- DEFINICIÓN DE FUNCIONES ------------------------------------------------------------------------


# Efecto Doppler
def Doppler(v_f, v_r, f_0):

    # f_0 : Frecuencia de la emisión (Hz)
    # v : velocidad del sonido. v = 343,2 m/s
    # v_r : velocidad del receptor (m/s). Positiva si la fuente se aleja del receptor
    # v_f : velocidad de la fuente (m/s). Positiva si la fuente se acerca al receptor
    
    v = 343.2
    f = (v - v_r)/(v - v_f) * f_0

    return f

# Conversión de velocidades

def kmh_to_ms(kmh):
    return kmh*3600/1000

#@st.cache_data
def Doppler_audio(input_file, output_file, delta_f):
    # Cargar el archivo de audio
    audio_data, sample_rate = librosa.load(input_file, sr=None)

    # Alterar la frecuencia
    audio_data_alterado = librosa.effects.pitch_shift(audio_data, sr=sample_rate, n_steps=int(delta_f/100))

    # Crear archivo de audio con la frecuencia alterada
    sf.write(output_file, audio_data_alterado, sample_rate)

@st.cache_data
def crear_animación(parametros_cache):

    # Función para actualizar la animación en cada cuadro
    def update_anim(frame):
        # Calcular la posición x del círculo en función del tiempo (frame)
        x_emisor = posicion_inicial_emisor_x + frame * velocidad_emisor
        x_receptor = posicion_inicial_receptor_x + frame * velocidad_receptor

        # Coordenadas cartesianas del círculo
        theta = np.linspace(0, 2 * np.pi, 100)
        y = np.sin(theta)

        # Actualizar la posición del punto
        circle_emisor.set_center((x_emisor, posicion_inicial_emisor_y))
        circle_emisor_border.set_center((x_emisor, posicion_inicial_emisor_y))

        circle_receptor.set_center((x_receptor, posicion_inicial_receptor_y))
        circle_receptor_border.set_center((x_receptor, posicion_inicial_receptor_y))

        # Actualizar los radios de las circunferencias anteriores con una velocidad de crecimiento ajustada
        #velocidad_propagacion = 0.01  # Velocidad de crecimiento de los círculos
        for c in circles:
            c.set_radius(c.get_radius() + velocidad_propagacion)  # Incremento del radio

        # Crear y dibujar una nueva circunferencia en intervalos regulares
        if frame % intervalo_emision == 0 and frame!=0:
            linewidth = 1  # Grosor de la línea de las circunferencias azules
            new_circle = plt.Circle((x_emisor, posicion_inicial_emisor_y), circle_emisor.radius, color='blue', fill=False, linewidth=linewidth)
            ax.add_artist(new_circle)
            circles.append(new_circle)

        return circle_emisor, circle_emisor_border, *circles


    # Dibujar el punto original en la posición inicial como un círculo naranja
    circle_emisor = plt.Circle((posicion_inicial_emisor_x, posicion_inicial_emisor_y), radio_inicial, color='orange', fill=True)
    ax.add_artist(circle_emisor)
    # Dibujar el borde del punto original en la posición inicial como una circunferencia negra
    circle_emisor_border = plt.Circle((posicion_inicial_emisor_x, posicion_inicial_emisor_y), radio_inicial, color='black', fill=False, linewidth=2)
    ax.add_artist(circle_emisor_border)

    # Dibujar el punto original en la posición inicial como un círculo rojo
    circle_receptor = plt.Circle((posicion_inicial_receptor_x, posicion_inicial_receptor_y), radio_inicial, color='red', fill=True)
    ax.add_artist(circle_receptor)
    # Dibujar el borde del punto original en la posición inicial como una circunferencia negra
    circle_receptor_border = plt.Circle((posicion_inicial_receptor_x, posicion_inicial_receptor_y), radio_inicial, color='black', fill=False, linewidth=2)
    ax.add_artist(circle_receptor_border)


    # Crear la animación
    anim = animation.FuncAnimation(fig, update_anim, frames=n_frames, interval=velocidad_animacion, blit=True)

    # Mostrar la animación
    animacion = HTML(anim.to_jshtml())


    st.markdown(f"""
                <h1 style="color: red">
                """, unsafe_allow_html=True)
    import streamlit.components.v1 as components
    components.html(anim.to_jshtml(), height=400, width=1000)



# ----------------------------------------------------------------------------------- SIMULACIÓN --------------------------------------------------------------------------

# Crear la figura y los ejes
fig = plt.figure(figsize=(10,3))
ax = fig.add_axes((0,0,1,1), frameon=False) #Frameon = Flase quita el are de afuera de los ejes.
#ax.axis('off')
ax.set_frame_on=False



#-----------------------------------------------------------------------------------
# Parámetros controlables
escala = 1/40
escala_velocidad = 1/10
# Establecer límites de los ejes
dim_x = 2000 * escala
dim_y = 600 * escala
ax.set_xlim(-dim_x/2, dim_x/2)
ax.set_ylim(-dim_y/2, dim_y/2)

# Variables para almacenar las circunferencias creadas
circles = []

    #Parámetros físicos
posicion_inicial_emisor_x = -dim_x/3 # Posición inicial en el eje x del emisor
posicion_inicial_emisor_y = 0  # Posición inicial en el eje y del emisor
velocidad_emisor = 10 * escala  # Velocidad del emisor. (m/s)
posicion_inicial_receptor_x = dim_x/3  # Posición inicial en el eje x del receptor
posicion_inicial_receptor_y = 0  # Posición inicial en el eje y del receptor
velocidad_receptor = 1 * escala  # Velocidad del receptor. (m/s)
velocidad_propagacion = 343.2 * escala * escala_velocidad # Velocidad de proagación de la onda. (m/s)

    # Parámetros de la animación
radio_inicial = (dim_x/2) * escala  # Radio inicial de los círculos de las emisiones.
intervalo_emision = 4  # Intervalo entre emisiones. Propósitos gráficos
#-----------------------------------------------------------------------------------------------


column = st.columns(4)

column[0].markdown('**EMISOR (Punto naranja):**')
#posicion_inicial_emisor_y = column[0].slider('Vertical', -dim_y/2, dim_y/2, 0.0 )
velocidad_emisor = column[0].number_input('Velocidad (m/s)', value= 10.0, min_value=-30.0, max_value=+30.0, step= 1.0, )
f_emisor = column[0].number_input('Frecuencia emitida (Hz)', value= 5000, min_value=10, max_value=20000, step= 100, )
posicion_inicial_emisor_x = column[0].slider('Posición horizontal', -dim_x/2, dim_x/2, -dim_x/3 )

column[1].markdown('**RECEPTOR (Punto rojo):**')
#posicion_inicial_receptor_y = column[1].slider('Vertical', -dim_y/2, dim_y/2, 0.0, key='y_receptor' )
velocidad_receptor = column[1].number_input('Velocidad (m/s)', value= 0.0, min_value=-30.0, max_value=+30.0, step= 1.0, key='velocidad_receptor' )
column[1].markdown('Frecuenca recibida:')
f_receptor = round( Doppler(velocidad_emisor, velocidad_receptor, f_emisor), 2)
column[1].markdown(f"{f_receptor } Hz")
posicion_inicial_receptor_x = column[1].slider('Posición horizontal', -dim_x/2, dim_x/2, +dim_x/3, key='x_receptor' )

velocidad_emisor*=escala
velocidad_receptor*=escala


column[3].markdown('**Parámetros físicos**')

with column[3]:
    romper_fisica= st_toggle_switch('Romper la física', track_color='#FF4B4B', active_color='#FF4B4B')
velocidad_sonido = column[3].number_input('Velocidad del sonido (m/s)', value = 343.0, min_value=1.0, max_value=2000.0, disabled=not(romper_fisica), help='')
escala_velocidad = column[3].number_input('Escala de velocidad (1/...?)', value = 10.0, min_value=1.0, max_value=1000.0, disabled=not(romper_fisica), help='Reducción artificial de la velocidad para que sea observable en la animación (No se considera esta reducción en los cálculos.)')


column[2].markdown('**ANIMACIÓN**')
intervalo_emision = column[2].number_input('Intervalo de emisión', value=4, min_value=1, max_value=20, help='Número de frames entre una emisión y la siguiente')
n_frames = column[2].number_input('Nº de fotogramas', value=30, min_value=1, max_value=100, help='Número de imágenes que constituyen la animación')
velocidad_animacion = column[2].number_input('Tiempo entre frames', value=50, min_value=10, max_value=100)


parametros_cache = [velocidad_emisor, velocidad_receptor, f_emisor, posicion_inicial_emisor_x, posicion_inicial_receptor_x,
                    intervalo_emision, n_frames, velocidad_animacion, velocidad_sonido, escala_velocidad]


crear_animación(parametros_cache)



# ESTO SE QUEDA PENDIENTE DE HACERLO CON G-AUDIO DELANTE Y PODER TIRAR DE ESE CÓDIGO
column = st.columns(2)
archivo = column[0].file_uploader('Sube tu audio', type=['mp3', 'wav', 'flac', 'ogg', 'aiff', 'AU'], accept_multiple_files=False)

from streamlit_extras.no_default_selectbox import selectbox
with column[0]:
    seleccion = selectbox('O utiliza alguno de los de prueba:', options=['sirena.wav', '_secret_.mp3'])



if archivo and seleccion ==None:
    filename = archivo.name
elif seleccion !=None:
    archivo = 'Simulaciones/'+seleccion
    filename = seleccion
    
if archivo or seleccion!=None:
    input_file=archivo
    output_file = 'Simulaciones/Doppler_test.wav'
    delta_f = f_receptor-f_emisor  # Frecuencia a aumentar en Hz

    with column[1]:
        Doppler_audio(input_file, output_file, delta_f)

    column[1].markdown(f'**Audio Original** ({filename}):')
    column[1].audio(archivo)

    if delta_f>0: column[1].markdown(f'**Audio Alterado**(+{round(delta_f)}Hz) : ')
    if delta_f<=0: column[1].markdown(f'**Audio Alterado**({round(delta_f)}Hz) : ')
    audio_file = open(output_file, 'rb')
    column[1].audio(audio_file)


