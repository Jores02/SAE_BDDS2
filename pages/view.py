import streamlit as st
import pandas as pd

# Initialisation de st.session_state.df pour l'exemple
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame({
        "nom": ["Alice", "Bob", "Charlie"],
        "age": [25, 30, 35],
        "ville": ["Paris", "Lyon", "Marseille"]
    })

# Titre de la page
st.title("Page de Recherche de Données Innovante")

# Sidebar pour la sélection des colonnes
st.sidebar.header("Options de Recherche")
all_columns = st.session_state.df.columns.tolist()
selected_column = st.sidebar.selectbox("Sélectionnez une colonne à afficher", all_columns)

# Pré-remplir le champ de texte avec le nom de la colonne sélectionnée
col_name = st.text_input("Entrez le nom de la colonne à afficher", value=selected_column)

# Utilisation de colonnes pour une mise en page plus attractive
col1, col2 = st.columns(2)

if col_name:
    if col_name in st.session_state.df.columns:
        st.subheader(f"Valeurs de la colonne {col_name}")
        
        # Afficher les valeurs de la colonne
        st.dataframe(st.session_state.df[[col_name]])
        
        # Ajouter des critères de sélection supplémentaires
        with col1:
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
        with col2:
            st.subheader(f"Données filtrées selon les critères pour {col_name}")
            st.dataframe(filtered_df)
            
        # Ajout d'une visualisation graphique
        if st.button("Afficher le graphique des données filtrées"):
            if st.session_state.df[col_name].dtype in ['int64', 'float64']:
                st.line_chart(filtered_df[col_name])
            else:
                st.bar_chart(filtered_df[col_name].value_counts())
                
        # Option de téléchargement des données filtrées
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Télécharger les données filtrées en CSV",
            data=csv,
            file_name='filtered_data.csv',
            mime='text/csv',
        )
    else:
        st.error(f"La colonne '{col_name}' n'existe pas dans le DataFrame.")
else:
    st.info("Veuillez sélectionner ou entrer le nom d'une colonne.")
