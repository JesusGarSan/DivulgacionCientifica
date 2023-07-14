import pandas as pd
import numpy as np
import streamlit as st
def sin(angulo): #en grados
    return np.sin(angulo * np.pi/180)
def cos(angulo): #en grados
    return np.cos(angulo * np.pi/180)

df= pd.DataFrame(columns=['Tipo', 'Angulo', 'longitud', 'Origen', 'Extremo'])
df2= pd.DataFrame(columns=['Tipo', 'Angulo', 'longitud', 'X', 'Y'])

angulo = -90
longitud = .9

# Primer rayo incidente

extremo=np.array([0,0])

origen=np.array([
    longitud * sin(angulo),
    longitud * cos(angulo),
])

#Rayo incidente
df.loc[len(df.index)] = ['Incidente', angulo, longitud, origen, extremo]
#1º rayo reflejado
df.loc[len(df.index)] = ['Reflejado', -angulo, longitud, extremo, [-origen[0], origen[1]]]




import altair as alt


dimension =1000

source = pd.DataFrame({
    'X': np.linspace(origen[0], extremo[0], dimension),
    'Y': np.linspace(origen[1], extremo[1], dimension),
    'Tipo' : 'Incidente',
    'Angulo' : str(angulo)+'º'
})


for index, row in df.iterrows():
    if index==0: continue
    aux = pd.DataFrame({
        'X': np.linspace(row.Origen[0], row.Extremo[0], dimension),
        'Y': np.linspace(row.Origen[1], row.Extremo[1], dimension),
        'Tipo' : row.Tipo,
        'Angulo' : str(row.Angulo)+'º'
    })
    source = pd.concat([source, aux], ignore_index=True)


#source = df

chart=alt.Chart(source).mark_line(strokeWidth=4).encode(
    alt.X('X', axis=None),
    alt.Y('Y', axis=None),
    color='Tipo' ,
    tooltip= ['Angulo'],
    
).interactive()

st.altair_chart(chart, theme="streamlit", use_container_width=True)


with st.spinner('eadasd'):
    import time
    time.sleep(3)
