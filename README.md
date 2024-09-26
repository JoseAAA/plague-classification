# Proyecto de Clasificación de Plagas en Hojas de Tomate con MLOps

Este proyecto sigue las buenas prácticas de **MLOps** para la clasificación de plagas en hojas de tomate utilizando el modelo YOLOv8. El pipeline abarca la preparación de datos, el entrenamiento, la selección de modelos, el monitoreo y la implementación de un servicio de predicción.

## Descripción del Proyecto

El objetivo del proyecto es proporcionar un pipeline completo para la clasificación de plagas en hojas de tomate. Se utilizan herramientas como **MLflow**, **Docker**, **FastAPI** y **Streamlit** para garantizar un entorno reproducible, escalable y automatizado para entrenar y desplegar modelos.

## Estructura del Proyecto

El proyecto sigue una estructura modular para facilitar su mantenibilidad, escalabilidad y comprensión.

```
plague-classification/
├── data/                      # Datos sin procesar y procesados
├── model/                     # Scripts y configuraciones del modelo
├── monitoring/                # Configuración de monitoreo y detección de drift
├── notebooks/                 # Análisis exploratorio de datos
├── prediction_service/        # Servicio de predicción con Gradio y FastAPI
├── frontend/                  # Interfaz de usuario para subir imágenes
├── tests/                     # Pruebas unitarias y de integración
├── .gitignore                 # Archivos y carpetas a ignorar en git
├── training.docker-compose.yml# Configuración Docker Compose para el entrenamiento
├── serving.docker-compose.yml # Configuración Docker Compose para la inferencia y monitoreo
├── training.env               # Variables de entorno para el entrenamiento
└── README.md                  # Documentación del proyecto
```

## Requisitos

### Software

- **Python**: 3.10 o superior
- **Docker** y **Docker Compose**: Para contenerizar los servicios.
- **WSL** (Windows Subsystem for Linux): Requerido si usas Windows para ejecutar Docker y otros servicios Linux.

### Dependencias del Proyecto

Las dependencias están divididas según el propósito:

- **model/requirements.txt**: Dependencias para entrenamiento del modelo.
- **frontend/requirements.txt**: Dependencias para la interfaz de usuario.
- **prediction_service/requirements.txt**: Dependencias para el servicio de predicción.

### Dependencias Principales

- **YOLOv8**: Modelo para la clasificación de imágenes.
- **MLflow**: Seguimiento de experimentos.
- **FastAPI**: API para el servicio de predicción.
- **Streamlit**: Interfaz web para subir imágenes y visualizar predicciones.
- **Logstash y Elasticsearch**: Monitoreo y almacenamiento de logs.

## Guía de Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/JoseAAA/plague-classification.git
cd plague-classification
```
### 2. Crear y activar un entorno virtual (opcional pero recomendado)

```bash
python3 -m venv venv
source venv/bin/activate  # Para Linux/Mac
venv\Scripts\activate   # Para Windows
```

### 3. Instalar dependencias

Para instalar las dependencias del modelo y otras herramientas:

```bash
pip install -r model/requirements.txt
```

### 4. Configurar Docker y Docker Compose

Asegúrate de tener Docker y Docker Compose instalados en tu sistema. Si usas Windows, sigue los siguientes pasos:

- Habilita WSL 2.
- Instala Docker Desktop y configúralo para usar WSL 2.

### 5. Entrenamiento del Modelo

### Crear la red compartida
Para que los servicios de comuniquen entre ello, es nesesario crear un red compartida.

```bash
docker network create shared_network
```
### Configuracion de MLflow
Para entrenar el modelo, utiliza Docker Compose con el archivo `training.docker-compose.yml`. Este archivo configura los servicios necesarios como MLflow, MinIO y PostgreSQL.

```bash
docker compose --env-file training.env -f training.docker-compose.yml up --build
```
Accede a MLflow en [http://localhost:5555](http://localhost:5555) para monitorear los experimentos de entrenamiento.

### Carpeta de Imagenes
Coloca las imágenes en la carpeta 'data/raw/' (crear carpeta). Cada subcarpeta dentro de raw/ debe representar una clase. Ejemplo:

```
data/raw/
├── Clase_A/
│   ├── imagen1.jpg
│   ├── imagen2.jpg
│   └── ...
├── Clase_B/
│   ├── imagen1.jpg
│   ├── imagen2.jpg
│   └── ...

```

### Configuración de parametros
En el archivo 'model/config.yaml' se encuentran los parametros para la selección y entrenamiento del modelo.

### Preprocesamiento de Datos
Ejecuta el script de preprocesamiento para dividir las imágenes en conjuntos de entrenamiento, validación y prueba:

```bash
python3 model/data_preprocessing.py 
```
### Entrenamiento del Modelo y Seguimiento de Experimentos
```bash
python3 model/train_model.py 
```
### Seleccion del mejor modelo
```bash
python3 model/select_model.py
```
### 6. Servir el Modelo y Realizar Predicciones

Para servir el modelo y realizar predicciones, utiliza el archivo `serving.docker-compose.yml`:

```bash
docker compose -f serving.docker-compose.yml up --build
```

Accede a los siguientes servicios:

- **Frontend**: [http://localhost:5002](http://localhost:5002) - Subida de imágenes y visualización de predicciones.
- **Servicio de Predicción**: [http://localhost:5001](http://localhost:5001) - API para realizar predicciones.
- **Elasticsearch y Kibana**: [http://localhost:5601](http://localhost:5601) - Monitoreo de logs y rendimiento.

### Crear un patrón de índice en Kibana
Si es la primera vez que usas Kibana, necesitarás crear un patrón de índice para visualizar los logs. Ejecuta el script create_index_pattern.py para configurarlo automáticamente:

```bash
python3 monitoring/create_index_pattern.py
```
### 7. Pruebas Unitarias

Para ejecutar las pruebas unitarias y de integración, utiliza pytest:

```bash
pytest tests/
```

## Monitoreo y Detección de Drift

El monitoreo de drift y la detección de cambios en los datos se realiza en tiempo real utilizando `drift_monitoring.py` y Elasticsearch para capturar logs. Asegúrate de tener configurado correctamente los servicios de monitoreo en el archivo `docker-compose.yml`.

## Solución de Problemas

- **Errores de autenticación en PostgreSQL**: Si encuentras problemas de autenticación, verifica que las credenciales de usuario y contraseña en `training.env` coincidan con las configuradas en los contenedores.
- **Problemas de permisos con Docker**: Asegúrate de que tu usuario esté agregado al grupo de Docker con `sudo usermod -aG docker $USER` y reinicia tu sesión.

## Conclusiones y Siguientes Pasos

- Mejora continua del modelo utilizando nuevos datos.
- Optimización del pipeline de entrenamiento y predicción.
- Implementación de alertas para detección de drift y fallos en producción.