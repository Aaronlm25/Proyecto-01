import unidecode
import pandas as pd
import Levenshtein as lev

def revise(user_ubication):
    
    ubication = unidecode.unidecode(user_ubication).lower()
    """
    Args:
        ubicacion (String): Ubicacion de la cual se desea conocer el clima

    Returns:
        list: contiene las 5 palabras con mayor indice de coincidencia
    """    
    # Ruta al archivo CSV
    archivo_csv = './weather_app/static/datalist/ciudades.csv'
    #Diccionario col las coincidencias e indice de coincidencia
    coincidences = {}
    # Leer el archivo CSV
    cities = pd.read_csv(archivo_csv)
    # Extraer una columna y convertirla en una lista
    column = cities[ubication[0]].tolist()
    #Iteramos sobre las ciudades en la columna y las comparamos con la ubicacion deseada
    for x in column:
        coincidence_index  = lev.ratio(ubication, x)
        #Filtro para considerar unicamente a las palabras en un rango de coincidencia especifico
        if coincidence_index >= 0.5:
            if coincidence_index not in coincidences:
                #creamos una nueva llave en el diccionario
                coincidences[coincidence_index] = set()
            coincidences[coincidence_index].add(x)
    ordered_coincidences = ordenar(coincidences)
    return primeros_n(ordered_coincidences, 5)

def ordenar(similar_locations):
    """
    Funcion para ordenar los elementos en el diccionario
    Args:
        similar_locations (dict): ciudades similares a la ubicacion del usuario

    Returns:
        dict: Ubicaciones ordenadas
    """
    ordered_locations = dict(sorted(similar_locations.items(), reverse = True))
    return ordered_locations

def primeros_n(similar, n):
    """
    Funcion para obtener los primeros n elementos de un diccionario
    Args:
        similar (dict) : Diccionario con las palabras parecidas
        n int : cantidad de palabras similares deseadas

    Returns:
        list: Lista de n palabras similares con la ubicacion deseada
    """
    first_n = []
    #Recorremos las keys del diccionario
    for key in similar:
        #Recorremos los elementos en las keys
        for item in similar.get(key):
            #La longitud de la lista debe ser del tamano establecido
            if len(first_n) < n:
                first_n.append(item)
    return first_n