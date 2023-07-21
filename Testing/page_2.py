import streamlit as st
from st_pages import Page, show_pages
st.set_page_config('Hello Forum',initial_sidebar_state='collapsed')


show_pages(
    [
        Page('page_1.py', 'Page 1'),
        Page('page_2.py', 'Page 2'),
    ]
)

st.markdown("""
            <style>
            [data-testid="stSidebar"] {
                display: none
            }

            [data-testid="collapsedControl"] {
                display: none
            }
            </style>
            """, unsafe_allow_html=True)




