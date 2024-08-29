import os
import json

def update(file_route, data):
    # Asegúrate de que el directorio exista
    os.makedirs(os.path.dirname(file_route), exist_ok=True)

    # Crear o actualizar el archivo
    with open(file_route, 'w') as file:
        json.dump(data, file)

def existance_insurer(file_route):
    # Asegúrate de que el directorio exista
    if not os.path.exists(os.path.dirname(file_route)):
        os.makedirs(os.path.dirname(file_route))

    # Crear el archivo si no existe
    if not os.path.isfile(file_route):
        with open(file_route, 'w') as file:
            pass
