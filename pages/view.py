import streamlit as st
import pandas as pd
import numpy as np
import datetime

# Définir le style de la page
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
    # Exemple de DataFrame pour démonstration
    st.session_state.df = pd.DataFrame({
        'ID': [1, 2, 3, 4, 5],
        'Nom': ['Minou', 'Rex', 'Bella', 'Médor', 'Félix'],
        'Type': ['Chat', 'Chien', 'Chat', 'Chien', 'Chat'],
        'Couleur': ['Noir', 'Marron', 'Blanc', 'Noir', 'Gris'],
        'Âge': [3, 5, 2, 7, 4]
    })

if "filtered_df" not in st.session_state:
    st.session_state.filtered_df = st.session_state.df

# Sélectionner une colonne à afficher
st.header("Recherche de données dans la base de données")
all_columns = st.session_state.df.columns.tolist()
selected_column = st.selectbox("Sélectionnez une colonne à afficher", all_columns)

# Demander le nom de la nouvelle colonne
col_name = st.text_input("Entrez le nom de la colonne à afficher")

if col_name:  # Vérifier si le nom de la colonne n'est pas vide
    if col_name in st.session_state.df.columns:
        st.write(f"Valeurs de la colonne {col_name} :")
        
        # Afficher les valeurs de la colonne
        st.dataframe(st.session_state.df[[col_name]])
        
        # Ajouter des critères de sélection supplémentaires
        if st.session_state.df[col_name].dtype in ['int64', 'float64']:
            # Si la colonne est numérique, permettre à l'utilisateur de définir une plage de valeurs
            min_val = st.number_input(f"Valeur minimum pour {col_name}", value=float(st.session_state.df[col_name].min()))
            max_val = st.number_input(f"Valeur maximum pour {col_name}", value=float(st.session_state.df[col_name].max()))
            st.session_state.filtered_df = st.session_state.df[(st.session_state.df[col_name] >= min_val) & (st.session_state.df[col_name] <= max_val)]
        else:
            # Si la colonne est textuelle, permettre à l'utilisateur de rechercher une correspondance partielle
            search_term = st.text_input(f"Termes à rechercher dans {col_name}")
            st.session_state.filtered_df = st.session_state.df[st.session_state.df[col_name].str.contains(search_term, case=False, na=False)]
        
        # Afficher le DataFrame filtré
        st.write(f"Données filtrées selon les critères pour {col_name} :")
        st.dataframe(st.session_state.filtered_df)
        
        # Bouton pour télécharger les résultats filtrés
        csv = st.session_state.filtered_df.to_csv(index=False)
        st.download_button(
            label="Télécharger les résultats filtrés en CSV",
            data=csv,
            file_name='resultats_filtres.csv',
            mime='text/csv'
        )
    else:
        st.write(f"La colonne '{col_name}' n'existe pas dans le DataFrame.")

# Bouton de réinitialisation du filtre
if st.button("Réinitialiser les filtres"):
    st.session_state.filtered_df = st.session_state.df
    st.experimental_rerun()
