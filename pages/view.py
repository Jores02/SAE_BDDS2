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

        # Initialisation des filtres
        if 'simple_filter' not in st.session_state:
            st.session_state.simple_filter = None
        if 'advanced_filters' not in st.session_state:
            st.session_state.advanced_filters = []
        if 'filtered_df1' not in st.session_state:
            st.session_state.filtered_df1 = None
        if 'filtered_df2' not in st.session_state:
            st.session_state.filtered_df2 = None

        # Fonction pour convertir les valeurs des filtres
        def convert_value(value, dtype):
            if dtype == 'int64':
                return int(value)
            elif dtype == 'float64':
                return float(value)
            return value

        # Fonction pour appliquer les filtres avancés
        def apply_advanced_filters(df, filters):
            for column_name, condition, value in filters:
                col_dtype = df[column_name].dtype
                if condition == 'equals':
                    value = convert_value(value, col_dtype)
                    df = df[df[column_name] == value]
                elif condition == 'contains':
                    df = df[df[column_name].astype(str).str.contains(value, na=False)]
                elif condition == 'greater_than':
                    value = convert_value(value, col_dtype)
                    df = df[df[column_name] > value]
                elif condition == 'less_than':
                    value = convert_value(value, col_dtype)
                    df = df[df[column_name] < value]
                elif condition == 'between':
                    min_value, max_value = value
                    min_value = convert_value(min_value, col_dtype)
                    max_value = convert_value(max_value, col_dtype)
                    df = df[df[column_name].between(min_value, max_value)]
            return df

        # Recherche simple
        st.write('### Recherche simple :')
        simple_column = st.selectbox('Colonne', df.columns, key='simple_filter_column')
        simple_value = st.text_input('Valeur', key='simple_filter_value')
        if st.button('Appliquer filtre simple'):
            st.session_state.simple_filter = (simple_column, simple_value)
            st.experimental_rerun()

        if st.session_state.simple_filter:
            column_name, value = st.session_state.simple_filter
            filtered_df = df[df[column_name].astype(str).str.contains(value, na=False)]
            st.write('### DataFrame après filtrage simple :')
            st.dataframe(filtered_df)

            # Sauvegarder le DataFrame filtré simple dans session_state
            st.session_state.filtered_df = filtered_df

        # Recherche avancée
        st.write('### Recherche avancée :')
        with st.form(key='advanced_filter_form'):
            column_name = st.selectbox('Colonne', df.columns, key='advanced_filter_column')
            condition = st.selectbox('Condition', ['equals', 'contains', 'greater_than', 'less_than', 'between'], key='advanced_filter_condition')
            if condition == 'between':
                value1 = st.text_input('Valeur minimale', key='advanced_filter_value1')
                value2 = st.text_input('Valeur maximale', key='advanced_filter_value2')
                value = (value1, value2)
            else:
                value = st.text_input('Valeur', key='advanced_filter_value')
            add_filter = st.form_submit_button('Ajouter le filtre')

        if add_filter:
            st.session_state.advanced_filters.append((column_name, condition, value))
            st.experimental_rerun()

        # Afficher les filtres avancés en attente
        st.write('### Filtres avancés en attente :')
        for i, f in enumerate(st.session_state.advanced_filters):
            column_name, condition, value = f
            col1, col2 = st.columns([3, 1])
            with col1:
                if condition == 'between':
                    st.write(f"Colonne '{column_name}', Condition : {condition}, Valeurs : {value[0]} et {value[1]}")
                else:
                    st.write(f"Colonne '{column_name}', Condition : {condition}, Valeur : {value}")
            with col2:
                if st.button('Supprimer', key=f'delete_advanced_filter_{i}'):
                    st.session_state.advanced_filters.pop(i)
                    st.experimental_rerun()

        # Appliquer les filtres avancés et afficher le DataFrame filtré
        if st.button('Appliquer les filtres avancés'):
            filtered_df = apply_advanced_filters(df, st.session_state.advanced_filters)
            st.write('### DataFrame après filtrage avancé :')
            st.dataframe(filtered_df)

            # Sauvegarder le DataFrame filtré dans session_state
            st.session_state.filtered_df = filtered_df

        # Options pour télécharger les filtres appliqués
        st.write('### Télécharger les filtres appliqués :')
        with st.expander("Options de téléchargement des filtres", expanded=False):
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

            if 'filtered_df1' in st.session_state and st.session_state.filtered_df1 is not None:
                filtered_json1 = st.session_state.filtered_df1.to_json(orient='records', indent=2)
                filtered_csv1 = st.session_state.filtered_df1.to_csv(index=False).encode('utf-8')

                try:
                    buffer1 = io.BytesIO()
                    for col in st.session_state.filtered_df1.columns:
                        if st.session_state.filtered_df1[col].dtype == 'object':
                            st.session_state.filtered_df1[col] = st.session_state.filtered_df1[col].astype('string')
                    st.session_state.filtered_df1.to_parquet(buffer1, index=False)
                    filtered_parquet1 = buffer1.getvalue()

                    st.download_button(
                        label="Télécharger en JSON (Filtres 1)",
                        data=filtered_json1,
                        file_name="filtered_data1.json",
                        mime="application/json"
                    )
                    st.download_button(
                        label="Télécharger en CSV (Filtres 1)",
                        data=filtered_csv1,
                        file_name="filtered_data1.csv",
                        mime="text/csv"
                    )
                    st.download_button(
                        label="Télécharger en Parquet (Filtres 1)",
                        data=filtered_parquet1,
                        file_name="filtered_data1.parquet",
                        mime="application/octet-stream"
                    )
                except Exception as e:
                    st.error(f"Erreur lors de la conversion en Parquet: {e}")

            if 'filtered_df2' in st.session_state and st.session_state.filtered_df2 is not None:
                filtered_json2 = st.session_state.filtered_df2.to_json(orient='records', indent=2)
                filtered_csv2 = st.session_state.filtered_df2.to_csv(index=False).encode('utf-8')

                try:
                    buffer2 = io.BytesIO()
                    for col in st.session_state.filtered_df2.columns:
                        if st.session_state.filtered_df2[col].dtype == 'object':
                            st.session_state.filtered_df2[col] = st.session_state.filtered_df2[col].astype('string')
                    st.session_state.filtered_df2.to_parquet(buffer2, index=False)
                    filtered_parquet2 = buffer2.getvalue()

                    st.download_button(
                        label="Télécharger en JSON (Filtres 2)",
                        data=filtered_json2,
                        file_name="filtered_data2.json",
                        mime="application/json"
                    )
                    st.download_button(
                        label="Télécharger en CSV (Filtres 2)",
                        data=filtered_csv2,
                        file_name="filtered_data2.csv",
                        mime="text/csv"
                    )
                    st.download_button(
                        label="Télécharger en Parquet (Filtres 2)",
                        data=filtered_parquet2,
                        file_name="filtered_data2.parquet",
                        mime="application/octet-stream"
                    )
                except Exception as e:
                    st.error(f"Erreur lors de la conversion en Parquet: {e}")

            st.markdown('</div>', unsafe_allow_html=True)

        # Bouton pour filtrer les données
        st.write('### Filtrer et télécharger deux ensembles de données :')
        col1, col2 = st.columns(2)
        with col1:
            if st.button('Filtrer et stocker les données comme "Filtres 1"'):
                st.session

