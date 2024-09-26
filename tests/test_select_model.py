import pytest
from model.select_model import select_best_model, load_config
import mlflow

# Fixture para la configuración
@pytest.fixture
def config():
    return load_config("model/config.yaml")

# Prueba para seleccionar el mejor modelo
def test_select_best_model(config):
    mlflow.set_tracking_uri("http://localhost:5555")
    try:
        select_best_model(config)
    except Exception as e:
        pytest.fail(f"Error al seleccionar el mejor modelo: {str(e)}")

