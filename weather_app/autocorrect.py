import Levenshtein as lev
import csv
import unidecode as ucode

def extract_column(file_path, ubication):
    """Funcion para extraer una columna del .csv

    Args:
        file_path (str): ruta hacia el .csv
        ubication (str): ubicacion de la cual se desea consultar el clima

    Returns:
        list: columna a la que pertenece la ubicacion
    """
    if len(ubication) == 0:
        return []
    column = []
    with open(file_path, mode='r') as cities_file:
        reader = csv.DictReader(cities_file)
        headers = reader.fieldnames
        if ubication[0] in headers:
            for row in reader:
                column.append(row[ubication[0]])
        else:
            return []
    return column

def organize(similar_locations):
    """
    Funcion para organize los elementos en el diccionario
    Args:
        similar_locations (dict): ciudades similares a la ubicacion del usuario

    Returns:
        dict: Ubicaciones ordenadas
    """
    ordered_locations = dict(sorted(similar_locations.items(), reverse = True))
    
    return ordered_locations

def first_n(similar, n):
    """
    Funcion para obtener los primeros n elementos de un diccionario
    Args:
        similar (dict) : Diccionario con las palabras parecidas
        n int : cantidad de palabras similares deseadas

    Returns:
        list: Lista de n palabras similares con la ubicacion deseada
    """
    first_n = []
    
    for key in similar:
        for item in similar.get(key):
            if len(first_n) < n:
                first_n.append(item)
                
    return first_n

def revise(user_ubication, coincidence_index):
    """
    Funcion para correguir la entrada del usuario
    Args:
        user_ubication (String): Ubicacion de la cual se desea conocer el clima
        coincidence_index (int): Indice que se desea poner como condicion para las comparaciones 

    Returns:
        list: contiene las 5 palabras con mayor indice de coincidencia
    """
    ubication = ucode.unidecode(user_ubication).lower()
    file_path = './weather_app/static/datalist/ciudades.csv'    
    
    column = extract_column(file_path, ubication)
    
    coincidences = {}
    
    for x in column:
        levenshtein_index  = lev.ratio(ubication, x)
        if levenshtein_index >= coincidence_index:
            if levenshtein_index not in coincidences:
               coincidences[levenshtein_index] = set()
            coincidences[levenshtein_index].add(x)
    ordered_coincidences = organize(coincidences)
    
    return first_n(ordered_coincidences, 5)
