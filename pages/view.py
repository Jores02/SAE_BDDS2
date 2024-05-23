import streamlit as st
import pandas as pd
import numpy as np
from inspect import signature
import pandas as pd
import datetime

st.markdown(
    """
    <style>
    body {
        background-image: url("https://www.numerama.com/wp-content/uploads/2016/09/grumpycat.jpg");
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialiser session_state si nécessaire
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()
if "new_row" not in st.session_state:
    st.session_state.new_row = {}
if "col_names" not in st.session_state:
    st.session_state.col_names = []
if "show_download_buttons" not in st.session_state:
    st.session_state.show_download_buttons = False
if "show_signature_button" not in st.session_state:
    st.session_state.show_signature_button = False

#col1, col2, col3 = st.columns(3)

#with col1:
#    st.page_link("create.py", label="CREATE", icon="🏠")

#with col2:
#    st.page_link("update.py", label="UPDATE", icon="🏠")

#with col3:
#    st.page_link("view.py", label="VIEW", icon="🏠")