import streamlit as st




@st.cache_data('Authenticate')
def authenticate(username, password):
    return username == "buddha" and password == "s4msara"

username = st.text_input('username')
password = st.text_input('password')

if authenticate(username, password):
    st.success('You are authenticated!')
    st.write(st.slider('Test widget')) # <- just to show that widgets work here
else:
    st.error('The username or password you have entered is invalid.')