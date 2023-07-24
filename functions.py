import streamlit as st


def mostrar_publicaciones(tipo, filename='publicaciones.csv'):
    """
    Función utilizada para mostrar las publicaciones (Artículos, Simulaciones, DIY) dentro de su página correspondiente.
    Escogemos qué tipo de publicación enseñar a través de la variable "tipo"

    tipo: (str) Para escoger qué tipo de publicación mostrar - ['Simulación', 'Artículo']
    filename: archivo del que extraer la lista de publicaciones

    """

    # --- Required Libraries ---
    
    import pandas as pd
    from PIL import Image
    from  streamlit_extras.switch_page_button import switch_page

    # --- Actual Function ---

    column = st.columns(2)
    last_coordinates = None
    publicaciones = pd.read_csv(filename, delimiter=';')
    publicaciones = publicaciones.iloc[::-1]
    index=0
    for i, publicacion in publicaciones.iterrows():
        # Mostramos sólo Artículos/Simulacione según el tipo elegido
        if publicacion.Tipo != tipo: continue
        # Mostramos sólo las publiaciones correspondientes a la categoría seleccionada
        if not filter_results(st.session_state['category_menu'], publicacion.categorias): continue
        # Mostramos sólo las publicaciones afines a la búsqueda
        import unidecode # usamos unidcode para ignorar tildes
        # Comprobamos si la búsqueda se encuentra en el título o etiquetas de la publicación
        search = unidecode.unidecode(st.session_state.search).lower()
        search_words = search.split()
        coincidende = False
        for word in search_words:
            if (word in unidecode.unidecode(publicacion.nombre_publico).lower() or
            word in unidecode.unidecode(publicacion.etiquetas).lower()): coincidende = True
            else: coincidende = False
        if coincidende==False and search!='': continue
        index+=1

        # Imagen asociada al artículo
        #img = Image.open("Galería/Imágenes/" + publicacion.ruta_imagen)
        #img = img.resize((500,300))
        with column[(index+1)%2]:
            cuadro_publicacion(publicacion.Tipo, publicacion.ruta_imagen, publicacion.nombre_publico)


def filter_results(choice, categories):

    """
    Función que detecta si la categoría seleccionada por "category_selector()" está en cierta publicación.
    Esta función es llamada por "mostrar_publicaciones()" para cada publicación. 
    """
    
    if choice == 'Todas' or choice==None: return True
    if choice in categories: return True
    return False



def search_bar(tipo):
    from st_keyup import st_keyup


    if 'search' not in st.session_state:
        st.session_state.search = ''
    search = st.session_state.search

    if tipo =='Simulación': search = st_keyup('Búsqueda', placeholder='Busca la simulación que quieras...', label_visibility='collapsed')
    if tipo =='Artículo': search = st_keyup('Búsqueda', placeholder='Busca el artículo que quieras...', label_visibility='collapsed')
    if tipo =='DIY': search = st_keyup('Búsqueda', placeholder='Busca el experimento casero que quieras...', label_visibility='collapsed')
    st.session_state.search = search


def category_selector():
    """
    Función utilizada para mostrar las publicaciones (Artículos, Simulaciones, DIY) dentro de su página correspondiente.
    Escogemos qué tipo de publicación enseñar a través de la variable "tipo"

    tipo: (str) Para escoger qué tipo de publicación mostrar - ['Simulación', 'Artículo']
    filename: archivo del que extraer la lista de publicaciones

    """

    # --- Required Libraries ---
    from streamlit_option_menu import option_menu
    
    # --- Actual Function ---

    # Manual Item Selection
    if st.session_state.get('switch_button', False):
        st.session_state['category_menu'] = (st.session_state.get('category_menu',0) + 1) % 4
        manual_select = st.session_state['category_menu']
    else:
        manual_select = None


    # Option Menu
    option_menu('Categorías', ['Todas', '---', 'Óptica', 'Ondas'],
                manual_select=manual_select,
                menu_icon='list', key='category_menu',
                styles={
                    "container": {},
                    "icon": {},
                })
            
    return
    
def cuadro_publicacion(tipo, ruta_imagen, nombre):
    """
    Función que genera la tarjeta (imagen + título) de una publicación concreta

    img: Imagen a representar
    nombre: nombre de la publicación a mostrar

    """

    # --- Required Libraries ---
    
    from  streamlit_extras.switch_page_button import switch_page 
    from st_clickable_images import clickable_images

    # --- Actual Function ---
    if tipo == 'Simulación': red= 255; blue= 0
    if tipo == 'Artículo': red= 0; blue= 255
    st.markdown(f"""
                <style>
                .image-text {{
                    position: absolute;
                    bottom: 0;
                    left: 0;
                    right: 0;
                    background-color: rgba({red}, 0, {blue}, 0.5);
                    color: white;
                    padding: 5px;
                    font-size: 20px;
                    text-align: center;
                    /* Solución temporal al problema de que asome el cuadro de texto por debajo de la imagen */
                    margin-top:-23.5px; 
                    margin-bottom: 23.5px;
                }}
                </style>
                """, unsafe_allow_html=True)
    #last_coordinates = streamlit_image_coordinates(img)
    click = clickable_images(
    [
        f"https://github.com/JesusGarSan/DivulgacionCientifica/blob/main/Galer%C3%ADa/Im%C3%A1genes/{ruta_imagen}?raw=true",
    ],
    img_style={"margin": "0px", "height": "250px", "width": "100%", "cursor": "pointer", "position": "relative", "display": "inline-block"},
    key = nombre
)
    st.markdown(f"""
                <a href="{nombre}" target="_self">
                <span class="image-text">
                {nombre}
                </span>
                </a>
                """, unsafe_allow_html=True)
    if click == 0 : switch_page(nombre)
    #last_coordinates = None
    #if last_coordinates!=None: switch_page(nombre)
    # Botón de acceso al artículo
    # boton = st.button(nombre, use_container_width=True)
    # if boton: switch_page(nombre)

    return