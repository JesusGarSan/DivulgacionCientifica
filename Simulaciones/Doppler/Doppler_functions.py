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
#import setup_page
#setup_page.setup_page()

#------------------------------------------------------------------------- DEFINICIÓN DE FUNCIONES ------------------------------------------------------------------------

# Efecto Doppler
def Doppler(v_f, v_r, f_0, v=343.2):

    # f_0 : Frecuencia de la emisión (Hz)
    # v : velocidad del sonido. v = 343,2 m/s
    # v_r : velocidad del receptor (m/s). Positiva si la fuente se aleja del receptor
    # v_f : velocidad de la fuente (m/s). Positiva si la fuente se acerca al receptor
    
    f = (v - v_r)/(v - v_f) * f_0

    return np.abs(f)

# Conversión de velocidades
def kmh_to_ms(kmh):
    return kmh*3600/1000



#@st.cache_data
def Doppler_audio(v_e, v_r, c, input_file, output_file):

    #CASO NO SUPERSÓNICO FUNCIONAL
    # PENDIENTE DE ADAPTAR PARA LE CASO SUPERSÓNICO
    
    # Cargar el archivo de audio
    audio_data, sample_rate = librosa.load(input_file, sr=None)

    # Alterar la frecuencia

    rate = (1-(v_e-v_r)/c)
    delta_f = Doppler(v_e, v_r, f_0, c) - f_0

    if np.abs(delta_f) > 4000:
        st.warning('La diferencia entre la velocidad del emisor y la del receptor no puede ser tan parecida a la velocidad del sonido.')
        return


    if rate < 0:
        audio_data_alterado = np.flipud(audio_data) # Usamos esto para invertir temporalmente el audio. Lo usamos si la velocidad supera a la del sonido en le medio
        audio_data_alterado = librosa.effects.pitch_shift(audio_data, sr=sample_rate, n_steps=int(-delta_f/100))
    else:
        audio_data_alterado = audio_data
        audio_data_alterado = librosa.effects.pitch_shift(audio_data, sr=sample_rate, n_steps=int(delta_f/100))

    audio_data_alterado = librosa.effects.time_stretch(audio_data_alterado, rate= np.abs(1/rate) )

    # Crear archivo de audio con la frecuencia alterada
    sf.write(output_file, audio_data_alterado, sample_rate)





@st.cache_data(show_spinner=False)
def crear_animación(parametros, dim_x, dim_y, escala_figura=.28, height = 600, width = 1000):

    # Crear la figura y los ejes
    #fig = plt.figure(figsize=(10,3))
    fig = plt.figure(figsize= (dim_x * escala_figura, dim_y * escala_figura))
    ax = fig.add_axes((0,0,1,1), frameon=False) #Frameon = False quita el are de afuera de los ejes.
    #ax.axis('off')
    ax.set_frame_on=False
    ax.set_xlim(-dim_x/2, dim_x/2)
    ax.set_ylim(-dim_y/2, dim_y/2)

    circles = []

    velocidad_emisor = parametros['velocidad_emisor']
    velocidad_receptor = parametros['velocidad_receptor']
    f_emisor = parametros['f_emisor']
    posicion_inicial_emisor_x = parametros['posicion_inicial_emisor_x']
    posicion_inicial_emisor_y = parametros['posicion_inicial_emisor_y']
    posicion_inicial_receptor_x = parametros['posicion_inicial_receptor_x']
    posicion_inicial_receptor_y = parametros['posicion_inicial_receptor_y']
    intervalo_emision = parametros['intervalo_emision']
    n_frames = parametros['n_frames']
    velocidad_animacion = parametros['velocidad_animacion']
    velocidad_sonido = parametros['velocidad_sonido']
    velocidad_propagacion = parametros['velocidad_propagacion']
    escala_velocidad = parametros['escala_velocidad']
    escala = parametros['escala']
    radio_inicial = parametros['radio_inicial']

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
    circle_emisor = plt.Circle((posicion_inicial_emisor_x, posicion_inicial_emisor_y), radio_inicial, color='#FF220C', fill=True, label='Emisor')
    ax.add_artist(circle_emisor)
    # Dibujar el borde del punto original en la posición inicial como una circunferencia negra
    circle_emisor_border = plt.Circle((posicion_inicial_emisor_x, posicion_inicial_emisor_y), radio_inicial, color='black', fill=False, linewidth=2)
    ax.add_artist(circle_emisor_border)

    # Dibujar el punto original en la posición inicial como un círculo rojo
    circle_receptor = plt.Circle((posicion_inicial_receptor_x, posicion_inicial_receptor_y), radio_inicial, color='#5DA271', fill=True, label='Receptor')
    ax.add_artist(circle_receptor)
    # Dibujar el borde del punto original en la posición inicial como una circunferencia negra
    circle_receptor_border = plt.Circle((posicion_inicial_receptor_x, posicion_inicial_receptor_y), radio_inicial, color='black', fill=False, linewidth=2)
    ax.add_artist(circle_receptor_border)

    ax.legend(loc='upper right')
    # Crear la animación
    ani = animation.FuncAnimation(fig, update_anim, frames=n_frames, interval=velocidad_animacion, blit=True)

    # Mostrar la animación
    #animacion = HTML(anim.to_jshtml())

    # ATENCIÓN: COMENTAR CUANDO NO SE ESTÁ USANDO PARA GENERAR GIFS EN LOCAL, ESTROPEA LA NIMACIÓN DE LA WEB
    # Guardar la animación
    #print('Creating animation')
    #ani.save('animacion.gif')
    #print('Animation created')

    st.markdown(f"""
                <h1 style="color: red">
                """, unsafe_allow_html=True)
    import streamlit.components.v1 as components
    components.html(ani.to_jshtml(default_mode='Once'), height=height, width=width)


def dashboard_parametros():

    escala = 1/40
    dim_x = 2000 * escala
    dim_y = 600 * escala
        
    posicion_inicial_emisor_y = 0  # Posición inicial en el eje y del emisor
    posicion_inicial_receptor_y = 0  # Posición inicial en el eje y del receptor
    radio_inicial = (dim_x/2) * escala  # Radio inicial de los círculos de las emisiones.

    column = st.columns(4)

    column[0].markdown('**EMISOR (Punto naranja):**')
    #posicion_inicial_emisor_y = column[0].slider('Vertical', -dim_y/2, dim_y/2, 0.0 )
    velocidad_emisor = column[0].number_input('Velocidad (m/s)', value= 10.0, min_value=-1000.0, max_value=+1000.0, step= 1.0, )
    f_emisor = column[0].number_input('Frecuencia emitida (Hz)', value= 5000, min_value=10, max_value=20000, step= 100, )
    posicion_inicial_emisor_x = column[0].slider('Posición horizontal', -dim_x/2, dim_x/2, -dim_x/3 )



    column[2].markdown('**ANIMACIÓN**')
    intervalo_emision = column[2].number_input('Intervalo de emisión', value=4, min_value=1, max_value=20, help='Número de frames entre una emisión y la siguiente')
    n_frames = column[2].number_input('Nº de fotogramas', value=30, min_value=1, max_value=100, help='Número de imágenes que constituyen la animación')
    velocidad_animacion = column[2].number_input('Tiempo entre frames', value=50, min_value=10, max_value=300)

    column[3].markdown('**Parámetros físicos**')
    with column[3]:
        romper_fisica= st_toggle_switch('Romper la física', track_color='#FF4B4B', active_color='#FF4B4B')
    velocidad_sonido = column[3].number_input('Velocidad del sonido (m/s)', value = 343.0, min_value=1.0, max_value=2000.0, disabled=not(romper_fisica), help='')
    escala_velocidad = column[3].number_input('Escala de velocidad (1/...?)', value = 10.0, min_value=1.0, max_value=1000.0, disabled=not(romper_fisica), help='Reducción artificial de la velocidad para que sea observable en la animación (No se considera esta reducción en los cálculos.)')

    velocidad_propagacion = velocidad_sonido * escala / escala_velocidad # Velocidad de proagación de la onda. (m/s)

    column[1].markdown('**RECEPTOR (Punto rojo):**')
    #posicion_inicial_receptor_y = column[1].slider('Vertical', -dim_y/2, dim_y/2, 0.0, key='y_receptor' )
    velocidad_receptor = column[1].number_input('Velocidad (m/s)', value= 0.0, min_value=-1000.0, max_value=+1000.0, step= 1.0, key='velocidad_receptor' )
    column[1].markdown('Frecuenca recibida:')
    f_receptor = round( Doppler(velocidad_emisor, velocidad_receptor, f_emisor, v = velocidad_sonido), 2 )
    column[1].markdown(f"{f_receptor } Hz")
    posicion_inicial_receptor_x = column[1].slider('Posición horizontal', -dim_x/2, dim_x/2, +dim_x/3, key='x_receptor' )
    velocidad_emisor*=escala
    velocidad_receptor*=escala

    
    parametros = {
        "velocidad_emisor": velocidad_emisor,
        "velocidad_receptor": velocidad_receptor,
        "posicion_inicial_emisor_x": posicion_inicial_emisor_x,
        "posicion_inicial_emisor_y": posicion_inicial_emisor_y,
        "posicion_inicial_receptor_x": posicion_inicial_receptor_x,
        "posicion_inicial_receptor_y": posicion_inicial_receptor_y,
        "intervalo_emision": intervalo_emision,
        "n_frames": n_frames,
        "velocidad_animacion": velocidad_animacion,
        "velocidad_sonido": velocidad_sonido,
        "velocidad_propagacion": velocidad_propagacion,
        "escala_velocidad": escala_velocidad,
        "escala": escala,
        "radio_inicial": radio_inicial,
        "f_emisor": f_emisor,
        "f_receptor": f_receptor,
    }


    return parametros, dim_x, dim_y


# ------ ALTERADOR DE AUDIO VIA DOPPLER NO SE QUÉ -------
def Doppler_audio_dashboard(parametros):
    column = st.columns(2)
    archivo = column[0].file_uploader('Sube tu audio:', type=['mp3', 'wav', 'flac', 'ogg', 'aiff', 'AU'], accept_multiple_files=False)
    #column_1 = column[1].columns(3)
    #v_e = column_1[0].number_input('Velocidad del emisor (m/s)', value=10.0)
    #v_r = column_1[1].number_input('Velocidad del receptor (m/s)', value=0.0)
    #c   = column_1[2].number_input('Velocidad sonido (m/s)', value=343.2)

    global f_0
    f_0 = parametros['f_emisor']
    v_e = parametros['velocidad_emisor']  /parametros['escala']
    v_r = parametros['velocidad_receptor']/parametros['escala']
    c   = parametros['velocidad_sonido']


    from streamlit_extras.no_default_selectbox import selectbox
    with column[0]:
        seleccion = selectbox('O utiliza alguno de los de prueba:', options=['sirena.wav', '_secret_.mp3', 'me colé.mp3'])

    input_file, output_file = False, False

    if archivo and seleccion ==None:
        filename = archivo.name
    elif seleccion !=None:
        archivo = 'Galería/Audio/'+seleccion
        filename = seleccion
        
    if archivo or seleccion!=None:
        input_file=archivo
        output_file = 'Galería/Audio/Doppler_simulation_output.wav'

        #return v_e, v_r, c, input_file, output_file

        with column[1]:
            with st.spinner('Alterando Audio...'):
               Doppler_audio(v_e, v_r, c, input_file, output_file)
                

        column[1].markdown(f'**Audio Original** ({filename}):')
        column[1].audio(archivo)


        delta_f = Doppler(v_e, v_r, f_0, c) - f_0
        help_string = f"El corrimiento en frecuencias se ha calculado considerando que la emisión es de **{f_0}Hz**. Esto puede no ajustarse bien a según que audios."

        if delta_f > 0: column[1].markdown(f'**Audio Alterado**(+{round(delta_f)}Hz): ', help=help_string)
        if delta_f <= 0: column[1].markdown(f'**Audio Alterado**({round(delta_f)}Hz): ', help=help_string)
        audio_file = open(output_file, 'rb')
        column[1].audio(audio_file)

