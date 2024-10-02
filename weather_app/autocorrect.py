import Levenshtein as lev
from collections import defaultdict

def organize(similar_locations: dict) -> dict:
    """
    Organiza los elementos en el diccionario.

    Función para organizar los elementos en el diccionario devuelto en el método revise, esto se hace en orden descendente.
    
    Args:
        similar_locations (dict): Ciudades similares a la ubicación del usuario.

    Returns:
        dict: Ubicaciones ordenadas.
    """
    return dict(sorted(similar_locations.items(), reverse=True))

def first_n(similar: dict, n: int) -> list:
    """
    Función para obtener los primeros n elementos del diccionario con las palabras ordenadas devueltas por revise.
    Las primeras n palabras del diccionario ordenado son almacenadas en una lista de longitud n.
    
    Args:
        similar (dict): Diccionario con palabras similares.
        n (int): Número de palabras similares deseadas.

    Returns:
        list: Lista de n palabras similares a la ubicación deseada.
    """
    first_n_items = []
    for items in similar.values():
        for item in items:
            if len(first_n_items) < n:
                first_n_items.append(item)
            else:
                return first_n_items
    return first_n_items

def revise(ubication: str, cities: list) -> list:
    """
    Función para corregir la entrada del usuario empleando el algoritmo de distancia de Levenshtein.
    Se emplea un índice de coincidencia de 0.4 por defecto y las coincidencias son almacenadas en un diccionario de acuerdo a su grado de coincidencia.

    Args:
        ubication (str): Ubicación para la cual se desea el clima.
        cities (list): Lista con los nombres de las ciudades.

    Returns:
        list: Lista con las 5 ciudades con el mayor índice de coincidencia ordenadas
              de mayor a menor.
    """
    if not ubication:
        return []
    user_ubication = ubication.lower()
    coincidence_index = 0.4
    coincidences = defaultdict(set)
    for city in cities:
        if city[0].lower() == user_ubication[0]:
            levenshtein_index = lev.ratio(user_ubication, city)
            if levenshtein_index >= coincidence_index:
                coincidences[levenshtein_index].add(city)
    ordered_coincidences = organize(coincidences)
    return first_n(ordered_coincidences, 5)