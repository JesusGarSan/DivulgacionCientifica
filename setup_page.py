import streamlit as st
from st_pages import Page, Section, show_pages, show_pages_from_config, add_page_title, hide_pages


def setup_page():


    st.set_page_config('El Quid', '🔍', 'wide', initial_sidebar_state='collapsed')
    #add_page_title()

    # Comentamos las siguientes líneas durante el desarrollo
    hide_streamlits()
    show_header()



def show_header():
    st.markdown('<style>' + open('./Header/header_styles.css').read() + '</style>', unsafe_allow_html=True)
    st.markdown(open('./Header/header_html.html').read(), unsafe_allow_html=True)

def hide_streamlits():
    hide_st_style = """
                <style>
                mainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                [data-testid="collapsedControl"] {
                display: none
                }
                </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)