import streamlit as st
import pandas as pd
import json
import io

# Fonction pour lire les fichiers
def load_file(file):
    if file.name.endswith('.json'):
        data = json.load(file)
        return pd.DataFrame(data)
    elif file.name.endswith('.csv'):
        return pd.read_csv(file)
    elif file.name.endswith('.parquet'):
        return pd.read_parquet(file)
    else:
        st.error("Format de fichier non pris en charge!")
        return None

# Téléchargement du fichier
uploaded_file = st.file_uploader("Choisissez un fichier JSON, CSV ou Parquet", type=["json", "csv", "parquet"])

if uploaded_file is not None:
    df = load_file(uploaded_file)
    if df is not None:
        st.write('### DataFrame original :')
        st.dataframe(df)

        st.write('### Recherches :')

        filtered_df = df.copy()

        # Recherches simples
        with st.expander("Recherches simples", expanded=False):
            st.write("#### Recherches simples")

            # Afficher un selectbox avec toutes les colonnes du DataFrame
            all_columns = df.columns.tolist()
            selected_column = st.selectbox("Sélectionnez une colonne à afficher", all_columns, key="simple_selectbox")

            if selected_column:
                # Afficher les valeurs de la colonne sélectionnée
                st.write(f"Valeurs de la colonne {selected_column} :")
                st.dataframe(df[[selected_column]])

                # Option de recherche simple dans une colonne textuelle
                if df[selected_column].dtype == 'object':
                    search_term = st.text_input(f"Rechercher dans la colonne {selected_column}", key="simple_search_term")
                    if search_term:
                        filtered_df = df[df[selected_column].str.contains(search_term, case=False, na=False)]
                        st.write(f"Résultats de la recherche pour '{search_term}' dans la colonne {selected_column} :")
                        st.dataframe(filtered_df)

        # Recherches avancées
        with st.expander("Recherches avancées", expanded=False):
            st.write("#### Recherches avancées")

            # Sélection de la colonne à afficher
            selected_column = st.selectbox("Sélectionnez une colonne à afficher (recherche avancée)", all_columns, key="adv_selectbox")

            if selected_column:
                st.write(f"Valeurs de la colonne {selected_column} :")
                st.dataframe(df[[selected_column]])

                # Ajouter des critères de sélection supplémentaires
                if df[selected_column].dtype in ['int64', 'float64']:
                    # Si la colonne est numérique, permettre à l'utilisateur de définir une plage de valeurs
                    min_val = st.number_input(f"Valeur minimum pour {selected_column}", value=float(df[selected_column].min()), key="min_val")
                    max_val = st.number_input(f"Valeur maximum pour {selected_column}", value=float(df[selected_column].max()), key="max_val")
                    filtered_df = df[(df[selected_column] >= min_val) & (df[selected_column] <= max_val)]
                else:
                    # Si la colonne est textuelle, permettre à l'utilisateur de rechercher une correspondance partielle
                    search_term = st.text_input(f"Termes à rechercher dans {selected_column}", key="adv_search_term")
                    if search_term:
                        filtered_df = df[df[selected_column].str.contains(search_term, case=False, na=False)]

                # Afficher le DataFrame filtré
                st.write(f"Données filtrées selon les critères pour {selected_column} :")
                st.dataframe(filtered_df)

        # Options pour télécharger
        st.write('### Télécharger les données filtrées :')
        with st.expander("Options de téléchargement", expanded=False):
            st.markdown(
                """
                <style>
                .small-button button {
                    font-size: 0.8em !important;
                    padding: 0.25em 0.5em !important;
                }
                </style>
                """,
                unsafe_allow_html=True
            )
            st.markdown('<div class="small-button">', unsafe_allow_html=True)

            if not filtered_df.empty:
                modified_json = filtered_df.to_json(orient='records', indent=2)
                modified_csv = filtered_df.to_csv(index=False).encode('utf-8')

                try:
                    buffer = io.BytesIO()
                    # Convertir explicitement les colonnes en types compatibles
                    for col in filtered_df.columns:
                        if filtered_df[col].dtype == 'object':
                            filtered_df[col] = filtered_df[col].astype('string')

                    filtered_df.to_parquet(buffer, index=False)
                    modified_parquet = buffer.getvalue()

                    st.download_button(
                        label="Télécharger en JSON",
                        data=modified_json,
                        file_name="filtered_data.json",
                        mime="application/json"
                    )
                    st.download_button(
                        label="Télécharger en CSV",
                        data=modified_csv,
                        file_name="filtered_data.csv",
                        mime="text/csv"
                    )
                    st.download_button(
                        label="Télécharger en Parquet",
                        data=modified_parquet,
                        file_name="filtered_data.parquet",
                        mime="application/octet-stream"
                    )
                except Exception as e:
                    st.error(f"Erreur lors de la conversion en Parquet: {e}")

            st.markdown('</div>', unsafe_allow_html=True)
