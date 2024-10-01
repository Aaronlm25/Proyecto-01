import Levenshtein as lev

def organize(similar_locations: dict) -> dict:
    """
    Funcion para organizar los elementos en el diccionario devuelto en el metodo revise, esto se hace en orden descendente.
    Args:
        similar_locations (dict): ciudades similares a la ubicacion del usuario.

    Returns:
        ordered_locations (dict) : ubicaciones ordenadas.
    """
    ordered_locations = dict(sorted(similar_locations.items(), reverse=True))
    return ordered_locations

def first_n(similar: dict, n: int) -> list:
    """
    Funcion para obtener los primeros n elementos del diccionario con las palabras odenadas devueltas por revise.
    las primeras 5 palabras del diccionario ordenado son almacenadas en una lista de longitud n.
    Args:
        similar (dict): diccionario con las palabras parecidas.
        int: cantidad de palabras similares deseadas.

    Returns:
        first_n (list): lista de n palabras similares con la ubicacion deseada.
    """
    first_n = []
    for key in similar:
        for item in similar.get(key):
            if len(first_n) < n:
                first_n.append(item)
    return first_n

def revise(ubication: str, cities : list) -> list:
    """
    Funcion para correguir la entrada del usuario empleando el algoritmo de distancia de Levenshtein.
    Se emplea un indice de coincidencia de 0.4 por defecto y las coincidencias son almacenadas en un diccionario de acuerdo a su grado de coincidencia

    Args:
        ubication (str): ubicacion de la cual se desea conocer el clima.
        cities (list) : lisa con los nombres de las ciudades.

    Returns:
        (list): contiene las 5 palabras con mayor indice de coincidencia.
    """
    if not ubication:
        return []
    user_ubication = ubication.lower()
    coincidence_index = 0.4
    coincidences = {}
    for x in cities:
        if x[0].lower() == user_ubication[0]:
            levenshtein_index = lev.ratio(user_ubication, x)
            if levenshtein_index >= coincidence_index:
                if levenshtein_index not in coincidences:
                    coincidences[levenshtein_index] = set()
                coincidences[levenshtein_index].add(x)
    ordered_coincidences = organize(coincidences)
    return first_n(ordered_coincidences, 5)