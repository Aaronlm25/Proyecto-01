import Levenshtein as lev
import csv
import unidecode as ucode

from static.python.data_manager import DataCollector
from static.python.path_manager import FileManager, FileNotFound

FILE_MANAGER=FileManager()

try:
   
    DATA_MANAGER = DataCollector(FILE_MANAGER)

except FileNotFound as e:
    print(f"Error: {e}")
    
class InvalidCacheFileException(Exception):
    """
    Clase de excepcion del archivo de cache dado,
    se lanza cuando el archivo no es .json
    """
    def __init__(self, message : str):
        super().__init__(message)

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

def revise(user_ubication: str, coincidence_index: int):
    """
    Funcion para correguir la entrada del usuario
    Args:
        user_ubication (String): Ubicacion de la cual se desea conocer el clima
        coincidence_index (int): Indice que se desea poner como condicion para las comparaciones 

    Returns:
        list: contiene las 5 palabras con mayor indice de coincidencia
    """
    cities = DATA_MANAGER.get_cities()
    coincidences = {}
    for x in cities:
        levenshtein_index = lev.ratio(user_ubication, x)
        if levenshtein_index >= coincidence_index:
            if levenshtein_index not in coincidences:
                coincidences[levenshtein_index] = set()
            coincidences[levenshtein_index].add(x)
    ordered_coincidences = organize(coincidences)
    return first_n(ordered_coincidences, 5)