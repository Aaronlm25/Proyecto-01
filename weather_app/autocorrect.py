import Levenshtein as lev
import csv
import unidecode as ucode

def organize(similar_locations: dict):
    """
    Funcion para organize los elementos en el diccionario
    Args:
        similar_locations (dict): ciudades similares a la ubicacion del usuario

    Returns:
        dict: Ubicaciones ordenadas
    """
    ordered_locations = dict(sorted(similar_locations.items(), reverse=True))
    return ordered_locations

def first_n(similar: dict, n: int):
    """
    Funcion para obtener los primeros n elementos de un diccionario
    Args:
        similar (dict): Diccionario con las palabras parecidas
        int: cantidad de palabras similares deseadas

    Returns:
        list: Lista de n palabras similares con la ubicacion deseada
    """
    first_n = []
    for key in similar:
        for item in similar.get(key):
            if len(first_n) < n:
                first_n.append(item)
    return first_n

def read():
    file_path = './weather_app/static/datalist/cities_2.csv'
    cities = []
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            cities.append(row[0])
    return cities

def revise(user_ubication: str, coincidence_index: int):
    """
    Funcion para correguir la entrada del usuario
    Args:
        user_ubication (String): Ubicacion de la cual se desea conocer el clima
        coincidence_index (int): Indice que se desea poner como condicion para las comparaciones 

    Returns:
        list: contiene las 5 palabras con mayor indice de coincidencia
    """
    cities = read()
    coincidences = {}
    for x in cities:
        levenshtein_index = lev.ratio(user_ubication, x)
        if levenshtein_index >= coincidence_index:
            if levenshtein_index not in coincidences:
                coincidences[levenshtein_index] = set()
            coincidences[levenshtein_index].add(x)
    ordered_coincidences = organize(coincidences)
    return first_n(ordered_coincidences, 5)