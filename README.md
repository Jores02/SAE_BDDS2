### Exécution avec Docker

```bash
docker build -t tst_app --progress=plain .
```

Puis

```bash
docker run -p 8501:8501 tst_app
```

### Exécution en ligne

Vous pouvez visualiser le site en ligne ici : https://amena-datasetapp.streamlit.app/
