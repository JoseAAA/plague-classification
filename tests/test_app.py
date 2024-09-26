import pytest
from fastapi.testclient import TestClient
from prediction_service.app import app

client = TestClient(app)

# Fixture para cargar una imagen de prueba
@pytest.fixture
def test_image():
    with open("tests/test_image.jpg", "rb") as img:
        return img.read()

# Prueba para el endpoint /predict
def test_predict(test_image):
    response = client.post("/predict", files={"file": test_image})
    assert response.status_code == 200
    result = response.json()
    assert "names" in result
    assert "probs" in result
    assert isinstance(result["names"], list)
    assert isinstance(result["probs"], list)
    assert len(result["names"]) == len(result["probs"])

# Prueba para verificar errores con archivos inválidos
def test_predict_invalid_file():
    response = client.post("/predict", files={"file": b"not_an_image"})
    assert response.status_code == 500
    assert response.json() == {"detail": "Prediction failed"}

# Prueba para el endpoint de refresco de modelo
def test_refresh_model():
    response = client.get("/refresh_model")
    assert response.status_code == 200
    assert response.json() == {"status": "Model refreshed successfully"}
