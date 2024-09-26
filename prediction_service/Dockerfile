# Imagen base de Python
FROM python:3.10-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos del servicio
COPY requirements.txt requirements.txt
COPY app.py app.py

# Instalar las dependencias necesarias del sistema para OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Comando para correr la aplicación
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
