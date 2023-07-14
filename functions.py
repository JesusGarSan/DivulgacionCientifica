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
        if publicacion.Tipo != tipo: continue
        index+=1

        # Imagen asociada al artículo
        img = Image.open("Galería/Imágenes/" + publicacion.ruta_imagen)
        img = img.resize((600,300))
        column[(index+1)%2].image(img, use_column_width=True )

        # Botón de acceso al artículo
        if column[(index+1)%2].button(publicacion.nombre_publico, use_container_width=True) or last_coordinates!=None:
            switch_page(publicacion.nombre_publico)