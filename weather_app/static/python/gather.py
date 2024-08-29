import csv
import random
import string
# Obtiene los datos de los destinos, de un archivo
# .csv, el cual contiene por cada destino 3 datos:
# ciudad, iata, aeropuerto
def get_destiny_data(route):
    destiny_data = []
    with open(route, mode='r') as file:
        reader = csv.reader(file)
        data = list(reader)
    for row in data:
        destiny_data.append(row)
    return destiny_data

# Recibe una lista de listas con 3 elementos los
# cuales son: ciudad, iata, aeropuerto
def get_city(iata):
    for list in get_destiny_data('./weather_app/static/datalist/datos_destinos.csv'):
        if list[1] == iata:
            return list[0]
    return None

# Lee los datos del archivo CSV
def get_destiny_data(route):
    destiny_data = []
    with open(route, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Salta el encabezado si existe
        destiny_data = list(reader)
    return destiny_data

#lee los datos de vuelo del archivo cvs
def load_flight_data(file_path):
    flight_data = {}
    try:
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Omitir la fila de encabezado si está presente
            for row in reader:
                flight_number = row[0]
                departure_iata = row[1]
                arrival_iata = row[2]
                flight_data[flight_number] = {'departure': departure_iata, 'arrival': arrival_iata}
    except FileNotFoundError:
        print(f"Error: El archivo {file_path} no se encuentra.")
    return flight_data

#lee los datos del archivo .txt
def save_flight_data_to_txt(flight_data, txt_file_path):
    try:
        # Leer el contenido existente del archivo
        try:
            with open(txt_file_path, mode='r') as file:
                existing_data = file.readlines()
        except FileNotFoundError:
            existing_data = []
        
        # Preparar los nuevos datos para insertar al principio
        new_data = [f"{flight_number}: Departure: {info['departure']}, Arrival: {info['arrival']}\n"
                    for flight_number, info in flight_data.items()]
        
        # Escribir los nuevos datos seguidos por los datos existentes
        with open(txt_file_path, mode='w') as file:
            file.writelines(new_data + existing_data)
    except IOError as e:
        print(f"Error al escribir el archivo {txt_file_path}: {e}")

#Genera los tikets
def generate_ticket():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

#Genera los datos de el evuelo
def generate_flight_data(route):
    flight_data = {}
    data = get_destiny_data(route)
    tickets = set()  # Usamos un conjunto para evitar duplicados

    for row in data:
        if len(row) >= 2:
            origin_iata = row[0]
            destination_iata = row[1]
            
            # Genera un ticket único y asegúrate de que no esté repetido
            ticket = generate_ticket()
            while ticket in tickets:
                ticket = generate_ticket()
            tickets.add(ticket)
            
            flight_data[ticket] = {
                'departure': origin_iata,
                'arrival': destination_iata
            }
    
    return flight_data

# Ruta del archivo CSV que contiene los datos de los vuelos
flight_data_file_path = './weather_app/static/datalist/datos_destinos_viajes.csv'
# Cargar los datos de vuelo desde el archivo CSV
flight_data = generate_flight_data(flight_data_file_path)

# Ruta del archivo TXT para guardar los tickets
tickets_txt_file_path = './weather_app/static/tickets.txt'
# Guardar los datos de vuelo en el archivo TXT
save_flight_data_to_txt(flight_data, tickets_txt_file_path)

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

