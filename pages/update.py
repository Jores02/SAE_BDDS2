﻿import streamlit as st
import pandas as pd
import numpy as np

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

#col1, col2, col3 = st.columns(3)

#with col1:
#    st.page_link("create.py", label="CREATE", icon="🏠")

#with col2:
#    st.page_link("update.py", label="UPDATE", icon="🏠")

#with col3:
#    st.page_link("view.py", label="VIEW", icon="🏠")