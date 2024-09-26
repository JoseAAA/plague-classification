import mlflow
from mlflow.tracking import MlflowClient
import yaml
import logging

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config(config_path="model/config.yaml"):
    """Carga la configuración desde un archivo YAML."""
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config

def select_best_model(config):
    mlflow.set_tracking_uri("http://localhost:5555")
    experiment_name = "Plague Classification"
    client = MlflowClient()
    experiment = client.get_experiment_by_name(experiment_name)

    if experiment is None:
        logger.error(f"Experimento '{experiment_name}' no encontrado.")
        return

    # Obtener todas las ejecuciones del experimento
    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        filter_string="",
        run_view_type=1
    )

    best_metric = float('inf')  # Cambiar a infinito positivo para buscar el mínimo
    best_run = None

    # Evaluar cada ejecución
    for run in runs:
        run_id = run.info.run_id
        metrics = run.data.metrics
        val_loss = metrics.get("val/loss", float('inf'))  # Cambia la métrica a val/loss
        logger.info(f"Evaluando modelo {run_id} con val/loss: {val_loss}")

        # Buscar el mejor modelo (mínima pérdida)
        if val_loss < best_metric:
            best_metric = val_loss
            best_run = run_id

    # Etiquetar los modelos
    for run in runs:
        run_id = run.info.run_id
        if run_id == best_run:
            client.set_tag(run_id, "model_status", "best")
            logger.info(f"Modelo {run_id} etiquetado como BEST.")
        else:
            client.set_tag(run_id, "model_status", "archived")
            logger.info(f"Modelo {run_id} etiquetado como ARCHIVADO.")

    logger.info(f"El mejor modelo es {best_run} con val/loss: {best_metric}")

if __name__ == "__main__":
    try:
        config = load_config()
        select_best_model(config)
    except Exception as e:
        logger.error(f"Error durante la selección del mejor modelo: {str(e)}")