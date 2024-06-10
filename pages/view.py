import streamlit as st
import pandas as pd

# Fonction pour lire le fichier uploadé
def load_data(file):
    if file is not None:
        try:
            df = pd.read_csv(file)
            return df
        except Exception as e:
            st.error(f"Erreur lors du chargement du fichier : {e}")
            return None
    return None

# Charger le fichier uploadé et l'ajouter à st.session_state
uploaded_file = st.file_uploader("Choisissez un fichier CSV", type=["csv"])
if uploaded_file:
    st.session_state.df = load_data(uploaded_file)

# Initialiser un DataFrame par défaut pour l'exemple si aucun fichier n'est uploadé
if "df" not in st.session_state or st.session_state.df is None:
    st.session_state.df = pd.DataFrame({
        "nom": ["Alice", "Bob", "Charlie"],
        "age": [25, 30, 35],
        "ville": ["Paris", "Lyon", "Marseille"]
    })

# Afficher un selectbox avec toutes les colonnes du DataFrame
all_columns = st.session_state.df.columns.tolist()
selected_column = st.selectbox("Sélectionnez une colonne à afficher", all_columns)

# Pré-remplir le champ de texte avec le nom de la colonne sélectionnée
col_name = st.text_input("Entrez le nom de la colonne à afficher", value=selected_column)

if col_name:
    if col_name in st.session_state.df.columns:
        st.write(f"Valeurs de la colonne {col_name} :")
        
        # Afficher les valeurs de la colonne
        st.dataframe(st.session_state.df[[col_name]])
        
        # Ajouter des critères de sélection supplémentaires
        if st.session_state.df[col_name].dtype in ['int64', 'float64']:
            # Si la colonne est numérique, permettre à l'utilisateur de définir une plage de valeurs
            min_val = st.number_input(f"Valeur minimum pour {col_name}", value=float(st.session_state.df[col_name].min()))
            max_val = st.number_input(f"Valeur maximum pour {col_name}", value=float(st.session_state.df[col_name].max()))
            filtered_df = st.session_state.df[(st.session_state.df[col_name] >= min_val) & (st.session_state.df[col_name] <= max_val)]
        else:
            # Si la colonne est textuelle, permettre à l'utilisateur de rechercher une correspondance partielle
            search_term = st.text_input(f"Termes à rechercher dans {col_name}")
            filtered_df = st.session_state.df[st.session_state.df[col_name].str.contains(search_term, case=False, na=False)]
        
        # Afficher le DataFrame filtré
        st.write(f"Données filtrées selon les critères pour {col_name} :")
        st.dataframe(filtered_df)
    else:
        st.write(f"La colonne '{col_name}' n'existe pas dans le DataFrame.")
