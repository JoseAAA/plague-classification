import os
import logging
import mlflow
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from PIL import Image
import numpy as np
from io import BytesIO
from mlflow.tracking import MlflowClient
from ultralytics import YOLO

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración de FastAPI
app = FastAPI()

# Variables de entorno
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5555")

# Inicialización de MLflow
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
client = MlflowClient()

# Función para cargar el mejor modelo desde MLflow
def load_best_model():
    experiment_name = "Plague Classification"
    experiment = client.get_experiment_by_name(experiment_name)

    if experiment is None:
        logger.error(f"Experiment '{experiment_name}' not found.")
        raise Exception("Experiment not found")

    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        filter_string="",
        run_view_type=1
    )

    # Buscar el mejor modelo etiquetado como BEST
    best_run = next((run for run in runs if run.data.tags.get("model_status") == "best"), None)
    
    if not best_run:
        logger.error("No best model found.")
        raise Exception("No best model found")

    # Descargar los artefactos del modelo
    model_path = client.download_artifacts(best_run.info.run_id, path="weights/best.pt")
    logger.info(f"Loading best model from {model_path}")

    # Cargar el modelo YOLO desde el directorio descargado
    model = YOLO(model_path)
    return model

# Cargar el mejor modelo al inicio del servicio
model = load_best_model()

# Endpoint de predicción
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # Leer la imagen
        image = Image.open(BytesIO(await file.read())).convert("RGB")
        image = np.array(image)
        
        # Realizar la predicción
        results = model.predict(source=image, save=False)
        names = list(results[0].names.values())
        probs = results[0].probs.data.tolist()
        
        logger.info("Prediction successful", extra={"predictions": names})
        return {"names": names, "probs": probs}

    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail="Prediction failed")
