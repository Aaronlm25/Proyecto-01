import csv
import random
import string

# Ruta del archivo CSV que contiene los datos de los vuelos
flight_data_file_path = './weather_app/static/datalist/vuelos.csv'

#lee los datos de vuelo del archivo cvs
def load_flight_data(path):
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

# Recibe una lista de listas con 3 elementos los
# cuales son: ciudad, iata, aeropuerto
def get_city(iata):
    for list in get_destiny_data('./weather_app/static/datalist/datos_destinos.csv'):
        if list[1] == iata:
            return list[0]
    return None

# Lee los datos del archivo CSV
def get_destiny_data(path):
    destiny_data = []
    with open(path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Salta el encabezado si existe
        destiny_data = list(reader)
    return destiny_data

#busca los datos del vuelo por su tiket
def get_flight_info(flight_number):
    """
    Obtiene la información de un vuelo dado su número de vuelo.

    Args:
        flight_number (str): El número del vuelo.

    Returns:
        dict or None: Un diccionario con la información de salida y llegada, o None si el vuelo no existe.
    """
    return flight_data.get(flight_number.upper(), None)

