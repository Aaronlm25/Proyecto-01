import Levenshtein as lev
from collections import defaultdict

def organize(similar_locations: dict) -> dict:
    """
    Organize the elements in the dictionary.

    Funcion para organizar los elementos en el diccionario devuelto en el metodo revise, esto se hace en orden descendente.
    Args:
        similar_locations (dict): Cities similar to the user's location.

    Returns:
        dict: Ordered locations.
    """
    return dict(sorted(similar_locations.items(), reverse=True))

def first_n(similar: dict, n: int) -> list:
    """
    Funcion para obtener los primeros n elementos del diccionario con las palabras odenadas devueltas por revise.
    las primeras 5 palabras del diccionario ordenado son almacenadas en una lista de longitud n.
    Args:
        similar (dict): Dictionary with similar words.
        n (int): Number of desired similar words.

    Returns:
        list: List of n similar words to the desired location.
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
    Funcion para correguir la entrada del usuario empleando el algoritmo de distancia de Levenshtein.
    Se emplea un indice de coincidencia de 0.4 por defecto y las coincidencias son almacenadas en un diccionario de acuerdo a su grado de coincidencia

    Args:
        ubication (str): Location for which the weather is desired.
        cities (list): List with the names of the cities.

    Returns:
        list: Contains the 5 words with the highest coincidence index.
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