import streamlit as st
import requests
import pandas as pd

# URL del servicio de predicción
PREDICTION_SERVICE_URL = "http://prediction_service:80/predict"

st.title("Clasificación de Imágenes de Plantas")

# Cargar la imagen
uploaded_file = st.file_uploader("Sube una imagen", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Mostrar la imagen cargada
    st.image(uploaded_file, caption='Imagen cargada.', use_column_width=True)

    # Botón de predicción
    if st.button('Predecir'):
        try:
            # Enviar la imagen al servicio de predicción
            files = {'file': uploaded_file.getvalue()}
            response = requests.post(PREDICTION_SERVICE_URL, files=files)
            response.raise_for_status()  # Verificar si hubo un error en la solicitud

            # Obtener los resultados
            predictions = response.json()
            names = predictions['names']
            probs = predictions['probs']

            # Crear un DataFrame para mostrar los resultados
            df = pd.DataFrame({'Nombre': names, 'Probabilidad': probs})
            df = df.sort_values(by='Probabilidad', ascending=False)  # Ordenar por probabilidad

            # Mostrar la tabla
            st.write(df)

        except requests.exceptions.RequestException as e:
            st.error(f"Error en la predicción: {e}")
