import json
import requests

# URL de Kibana (ajusta según sea necesario)
kibana_url = "http://localhost:5601"

# Nombre del patrón de índice para el servicio de predicción
index_pattern_name = "prediction_service-*"

# Endpoint para crear y eliminar patrones de índice en Kibana
create_api_endpoint = f"{kibana_url}/api/index_patterns/index_pattern"
delete_api_endpoint = f"{kibana_url}/api/index_patterns/index_pattern/{index_pattern_name}"

# Headers (puedes agregar autenticación aquí si es necesario)
headers = {"kbn-xsrf": "true", "Content-Type": "application/json"}

# Función para eliminar el patrón de índice existente (si existe)
def delete_index_pattern():
    response = requests.delete(delete_api_endpoint, headers=headers)
    if response.status_code == 200:
        print(f"Patrón de índice existente eliminado correctamente: {index_pattern_name}")
    elif response.status_code == 404:
        print(f"Patrón de índice {index_pattern_name} no encontrado. Procediendo a crear.")
    else:
        print(f"Fallo al eliminar el patrón de índice. Código de estado: {response.status_code}")
        print(response.text)

# Crear un nuevo patrón de índice con el campo de tiempo correcto
index_pattern = {
    "index_pattern": {
        "title": index_pattern_name,
        "timeFieldName": "@timestamp",  # Asegúrate de que este campo coincida con el campo de tiempo en tus documentos
        "fields": {}
    }
}

# Eliminar el patrón de índice existente (si existe)
delete_index_pattern()

# Crear el nuevo patrón de índice
response = requests.post(create_api_endpoint, headers=headers, data=json.dumps(index_pattern))

# Verificar el estado de la solicitud y mostrar el resultado
if response.status_code == 200:
    print("Nuevo patrón de índice creado correctamente.")
    print(response.json())
else:
    print(f"Fallo al crear el nuevo patrón de índice. Código de estado: {response.status_code}")
    print(response.text)
