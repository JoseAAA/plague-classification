# Imagen base
FROM python:3.10-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos necesarios
COPY requirements.txt requirements.txt
COPY app.py app.py

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Comando para ejecutar la aplicación
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=5000"]
