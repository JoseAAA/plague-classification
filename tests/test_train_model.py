import pytest
from model.train_model import train_model, load_config

# Fixture para la configuración del YAML
@pytest.fixture
def config():
    return load_config("model/config.yaml")

# Prueba para el entrenamiento del modelo
def test_train_model(config):
    try:
        train_model(config)
    except Exception as e:
        pytest.fail(f"Error durante el entrenamiento del modelo: {str(e)}")
