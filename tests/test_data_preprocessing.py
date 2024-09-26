import os
import pytest
from model.data_preprocessing import load_config, create_dataset_structure, setup_logging

# Fixture para cargar la configuración del YAML
@pytest.fixture
def config():
    return load_config("model/config.yaml")

# Fixture para el logger
@pytest.fixture
def logger():
    return setup_logging()

# Prueba para cargar el archivo de configuración
def test_load_config(config):
    assert "paths" in config
    assert "data_dir" in config["paths"]
    assert os.path.exists(config["paths"]["data_dir"])

# Prueba para la creación de la estructura de datos
def test_create_dataset_structure(config, logger):
    create_dataset_structure(config, logger)
    processed_dir = config["paths"]["processed_dir"]
    assert os.path.exists(os.path.join(processed_dir, "train"))
    assert os.path.exists(os.path.join(processed_dir, "val"))
    assert os.path.exists(os.path.join(processed_dir, "test"))

    # Limpiar después de la prueba
    if os.path.exists(processed_dir):
        os.system(f"rm -rf {processed_dir}")
