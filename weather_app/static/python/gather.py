import csv
import random
import string

# Ruta del archivo CSV que contiene los datos de los vuelos
flight_data_file_path = './weather_app/static/datalist/vuelos.csv'

def load_flight_data(path):
    """
    Lee los datos de vuelos desde un archivo CSV y los carga en un diccionario.

    El archivo CSV debe tener los datos en el siguiente formato:
    flight_number, departure_iata, arrival_iata

    Args:
        path (str): Ruta del archivo CSV que contiene los datos de vuelos.

    Returns:
        dict: Un diccionario donde las claves son los números de vuelo y los valores
              son diccionarios con la información de salida y llegada.
              
    Raises:
        FileNotFoundError: Si el archivo especificado no se encuentra.
    """
    flight_data = {}
    try:
        with open(path, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Omitir la fila de encabezado si está presente
            for row in reader:
                flight_number = row[0]
                departure_iata = row[1]
                arrival_iata = row[2]
                flight_data[flight_number] = {'departure': departure_iata, 'arrival': arrival_iata}
    except FileNotFoundError:
        print(f"Error: El archivo {path} no se encuentra.")
    return flight_data

# Cargar los datos de vuelo desde el archivo CSV
flight_data = load_flight_data(flight_data_file_path)

def get_city(iata):
    """
    Obtiene el nombre de la ciudad basado en el código IATA del aeropuerto.

    Lee los datos de un archivo CSV que contiene información de destinos.

    Args:
        iata (str): Código IATA del aeropuerto.

    Returns:
        str: Nombre de la ciudad correspondiente al código IATA, o None si no se encuentra.
    """
    for list in get_destiny_data('./weather_app/static/datalist/datos_destinos.csv'):
        if list[1] == iata:
            return list[0]
    return None

def get_destiny_data(path):
    """
    Lee los datos de destinos desde un archivo CSV y los carga en una lista.

    El archivo CSV debe tener los datos en el siguiente formato:
    city_name, iata_code, airport_name

    Args:
        path (str): Ruta del archivo CSV que contiene los datos de destinos.

    Returns:
        list: Una lista de listas, donde cada sublista contiene la información de una ciudad.
    """
    destiny_data = []
    with open(path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Salta el encabezado si existe
        destiny_data = list(reader)
    return destiny_data

def buscar_vuelo(ticket):
    """
    Busca la información del vuelo basado en el número de ticket.

    Utiliza el diccionario de datos de vuelo cargado previamente.

    Args:
        ticket (str): Número del ticket de vuelo.

    Returns:
        dict or str: Un diccionario con la información del vuelo (salida y llegada)
                     o un mensaje indicando que no se encontró información si el ticket no está en los datos.
    """
    if ticket in flight_data:
        return flight_data[ticket]
    else:
        return f"No se encontró información para el ticket: {ticket}"
