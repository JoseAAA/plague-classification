import mlflow
from ultralytics import YOLO
from ultralytics import settings
import os
import logging
import yaml
import shutil
import joblib

# Configuracion de mlflow en Yolo
settings.update({"mlflow": True})
settings.reset()

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Leer configuración desde config.yaml
def load_config(config_path="model/config.yaml"):
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config

def train_model(config):
    # Configuración de MLflow
    os.environ["MLFLOW_EXPERIMENT_NAME"] = "Plague Classification"
    os.environ["MLFLOW_RUN"] = f"YOLOv8-{config['model']['epochs']}-{config['model']['batch_size']}-{config['model']['img_size']}"
    os.environ["MLFLOW_TRACKING_URI"] = "http://localhost:5555"
    logger.info("Creación de las Variables de entorno para la configuración de MLFLOW.")

    # Eliminar Carpeta
    if os.path.exists("runs"):
        shutil.rmtree("runs")
    logger.info("Carpeta runs Eliminado.")

    # Crear y entrenar el modelo YOLO
    model = YOLO(config["model"]["model_name"])
    logger.info("Iniciando el entrenamiento del modelo YOLOv8.")
    results = model.train(
        data=config["paths"]["processed_dir"],
        epochs=config["model"]["epochs"],
        batch=config["model"]["batch_size"],
        imgsz=config["model"]["img_size"],
        device=config["model"]["device"],
        save=True,
        save_period=1
    )

if __name__ == "__main__":
    try:
        # Cargar configuración desde config.yaml
        config = load_config("model/config.yaml")
        train_model(config)
    except Exception as e:
        logger.error(f"Error durante el entrenamiento del modelo: {str(e)}")

