import csv
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

def get_flight_info(flight_number):
    flight_data = {
        'AA123': {'departure': 'JFK', 'arrival': 'LAX'},
        'DL456': {'departure': 'ORD', 'arrival': 'ATL'},
    }
    return flight_data.get(flight_number.upper(), None)