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

        st.write('### Recherches et Filtrage :')

        filtered_df = df.copy()

        # Colonnes disponibles pour la sélection
        all_columns = df.columns.tolist()

        # Stockage de la colonne sélectionnée pour la recherche simple
        selected_column_simple = st.selectbox("Sélectionnez une colonne à afficher (recherche simple)", all_columns)

        # Recherche simple
        if selected_column_simple:
            with st.expander("Recherche Simple", expanded=True):
                st.write("#### Recherche Simple")
                # Afficher les valeurs de la colonne sélectionnée
                st.write(f"Valeurs de la colonne {selected_column_simple} :")
                st.dataframe(df[[selected_column_simple]])

                # Option de recherche simple dans une colonne textuelle
                if df[selected_column_simple].dtype == 'object':
                    search_term = st.text_input(f"Rechercher dans la colonne {selected_column_simple}")
                    if search_term:
                        filtered_df = df[df[selected_column_simple].str.contains(search_term, case=False, na=False)]
                        st.write(f"Résultats de la recherche pour '{search_term}' dans la colonne {selected_column_simple} :")
                        st.dataframe(filtered_df)

        # Stockage de la colonne sélectionnée pour la recherche avancée
        selected_column_advanced = st.selectbox("Sélectionnez une colonne à afficher (recherche avancée)", all_columns, index=all_columns.index(selected_column_simple) if selected_column_simple else 0)

        # Recherche avancée
        if selected_column_advanced:
            with st.expander("Recherche Avancée", expanded=True):
                st.write("#### Recherche Avancée")
                st.write(f"Valeurs de la colonne {selected_column_advanced} :")
                st.dataframe(df[[selected_column_advanced]])

                # Ajouter des critères de sélection supplémentaires
                if df[selected_column_advanced].dtype in ['int64', 'float64']:
                    # Si la colonne est numérique, permettre à l'utilisateur de définir une plage de valeurs
                    min_val = st.number_input(f"Valeur minimum pour {selected_column_advanced}", value=float(df[selected_column_advanced].min()))
                    max_val = st.number_input(f"Valeur maximum pour {selected_column_advanced}", value=float(df[selected_column_advanced].max()))
                    filtered_df = df[(df[selected_column_advanced] >= min_val) & (df[selected_column_advanced] <= max_val)]
                else:
                    # Si la colonne est textuelle, permettre à l'utilisateur de rechercher une correspondance partielle
                    search_term = st.text_input(f"Termes à rechercher dans {selected_column_advanced}")
                    if search_term:
                        filtered_df = df[df[selected_column_advanced].str.contains(search_term, case=False, na=False)]

                # Afficher le DataFrame filtré
                st.write(f"Données filtrées selon les critères pour {selected_column_advanced} :")
                st.dataframe(filtered_df)

        # Options pour télécharger
        st.write('### Télécharger les données filtrées :')
        with st.expander("Options de téléchargement", expanded=True):
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
