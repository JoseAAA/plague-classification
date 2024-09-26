import json
import requests

# URL de Kibana (ajusta según sea necesario)
kibana_url = "http://localhost:5601"

# Nombre del patrón de índice para el servicio de predicción
index_pattern_name = "prediction_service-*"

# Endpoint para obtener, crear y eliminar patrones de índice en Kibana
get_api_endpoint = f"{kibana_url}/api/index_patterns/_find?title={index_pattern_name}"
create_api_endpoint = f"{kibana_url}/api/index_patterns/index_pattern"
delete_api_endpoint = f"{kibana_url}/api/index_patterns/index_pattern/{index_pattern_name}"

# Headers (puedes agregar autenticación aquí si es necesario)
headers = {"kbn-xsrf": "true", "Content-Type": "application/json"}

# Función para verificar si el patrón de índice ya existe
def check_index_pattern_exists():
    response = requests.get(get_api_endpoint, headers=headers)
    if response.status_code == 200:
        patterns = response.json()["saved_objects"]
        if patterns:
            print(f"El patrón de índice '{index_pattern_name}' ya existe en Kibana.")
            return True
        else:
            print(f"El patrón de índice '{index_pattern_name}' no existe.")
            return False
    else:
        print(f"Fallo al verificar el patrón de índice. Código de estado: {response.status_code}")
        return False

# Función para eliminar el patrón de índice existente (si existe)
def delete_index_pattern():
    if check_index_pattern_exists():
        response = requests.delete(delete_api_endpoint, headers=headers)
        if response.status_code == 200:
            print(f"Patrón de índice existente eliminado correctamente: {index_pattern_name}")
        elif response.status_code == 404:
            print(f"Patrón de índice {index_pattern_name} no encontrado.")
        else:
            print(f"Fallo al eliminar el patrón de índice. Código de estado: {response.status_code}")
            print(response.text)

# Función para crear un nuevo patrón de índice
def create_index_pattern():
    index_pattern = {
        "index_pattern": {
            "title": index_pattern_name,
            "timeFieldName": "@timestamp",
            "fields": {}
        }
    }
    response = requests.post(create_api_endpoint, headers=headers, data=json.dumps(index_pattern))
    if response.status_code == 200:
        print("Nuevo patrón de índice creado correctamente.")
        print(response.json())
    else:
        print(f"Fallo al crear el nuevo patrón de índice. Código de estado: {response.status_code}")
        print(response.text)

# Eliminar el patrón de índice existente (si existe)
delete_index_pattern()

# Crear el nuevo patrón de índice
create_index_pattern()
