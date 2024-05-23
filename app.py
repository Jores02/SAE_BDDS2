import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Dataset App", page_icon="💾", initial_sidebar_state="collapsed"
)

st.image("cat.gif")
st.markdown("# Dataset")
st.write(
    "This app lets you create datasets, update them, navigate through them and much more !"
)

tabMain, tabInfo = st.tabs(["Main", "Info"])

with tabInfo:
    st.write("")
    st.write("")

    st.subheader("🎈 What is Streamlit?")
    st.markdown(
        "[Streamlit](https://streamlit.io) is an open-source Python library that allows users to create interactive, web-based data visualization and machine learning applications without the need for extensive web development knowledge"
    )

    st.write("---")

    st.subheader("📖 Resources")
    st.markdown(
        """
    - Streamlit
        - [Documentation](https://docs.streamlit.io/)
        - [Gallery](https://streamlit.io/gallery)
        - [Cheat sheet](https://docs.streamlit.io/library/cheatsheet)
        - [Book](https://www.amazon.com/dp/180056550X) (Getting Started with Streamlit for Data Science)
        - Deploy your apps using [Streamlit Community Cloud](https://streamlit.io/cloud) in just a few clicks 
    """
    )
    
    st.write("---")

    st.subheader("👥 About us")
    st.markdown(
        """
    This project was carried out by a group of 3 computer science students.
    - Enzo Vandepoele
        - [GitHub](https://github.com/Unicron03)
        - [LinkedIn](https://www.linkedin.com/in/enzo-vandepoele-3224ab2b2/)
    - John Micallef
        - [GitHub](https://github.com/johnmclf)
        - [LinkedIn](https://www.linkedin.com/in/john-micallef-8227482bb/)
    - Amen Ahouandogbo
        - [GitHub](https://github.com/Jores02)
        - [LinkedIn](https://www.linkedin.com/in/amen-ahouandogbo-069604220/)
    """
    )

with tabMain:
    st.write("")
    st.write("")

    col1, col2, col3, col4, col5 = st.columns([1,2,2,1,1])

    with col2:
        st.page_link("pages/create.py", label="CREATE", icon="1️⃣")

    with col3:
        st.page_link("pages/update.py", label="UPDATE", icon="2️⃣")

    with col4:
        st.page_link("pages/view.py", label="VIEW", icon="3️⃣")
    
st.markdown("---")
st.markdown(
    "More infos at [github.com/Unicron03/datasetApp](https://github.com/Unicron03/datasetApp)"
)