import pandas as pd
import Levenshtein as lev

def revise(user_ubication):
    ubication = user_ubication.lower()
    """
    Args:
        ubicacion (String): Ubicacion de la cual se desea conocer el clima

    Returns:
        set: contiene las palabras con mayor indice de coincidencia
    """    
    # Ruta al archivo CSV
    archivo_csv = './static/datalist/ciudades.csv'
    #Conjunto col las coincidencias
    coincidences = set()
    # Leer el archivo CSV
    cities = pd.read_csv(archivo_csv)
    # Extraer una columna y convertirla en una lista
    column = cities[ubication[0]].tolist()
    #Iteramos sobre los elementos en la columna y los comparamos con la ubicacion deseada
    for x in column:
        coincidence_index  = lev.ratio(ubication, x)
        if coincidence_index >= .6:
            coincidences.add(x)
    return coincidences