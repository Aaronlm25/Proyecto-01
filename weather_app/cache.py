import os
import json

def get_data(file_route):
    existance_insurer(file_route)
    raw_data = []
    data = {}
    # Mete todos los objetos json del archivo .json en 
    # un diccionario cuya llave es el nombre de la ciudad
    # para facil manipulacion
    with open(file_route, 'r') as file:
        if os.path.getsize(file_route) != 0:
            raw_data = json.load(file)
    for weather in raw_data:
        data[weather['name']] = weather
    return data

def update(file_route, weather):
    existance_insurer(file_route)
    raw_data = []
    # Abre el archivo cache y si no es vacio obtiene
    # un objeto json.
    with open(file_route, 'r') as file:
        if os.path.getsize(file_route) != 0:
            raw_data = json.load(file)
    # Si ya se a tiene registrado el clima de una ciudad 
    # lo sobreescribe.
    override = False
    for data in raw_data:
        if weather['name'] == data['name']:
            raw_data.remove(data)
            raw_data.append(weather)
            override = True
            break
    if not (raw_data and override):
        raw_data.append(weather)
    with open(file_route, 'w') as file:
        json.dump(raw_data, file, indent=4)

def existance_insurer(file_route):
    if not os.path.exists(file_route):
        file = open(file_route, 'x')
        file.close()