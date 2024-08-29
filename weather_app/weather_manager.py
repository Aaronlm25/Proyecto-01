import requests
import csv
import threading
KEY = 'a3117bc0d7c113aba1f25b2fb28748e1'
LOCK = threading.Lock()
def get_weather(city):
    # Evita que se hagan dos peticiones al mismo tiempo pues esto es motivo de baneo
    with LOCK:
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={KEY}&units=metric&lang=es"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener datos: {e}")
            return None

#se usa para leer el archivo csv y los guarda
def load_flight_data(file_path):
    """
    Carga datos de vuelos desde un archivo CSV y retorna un diccionario con los datos.
    """
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

#Guarda todos los datos del csv leidos en un .txt
def save_flight_data_to_txt(flight_data, txt_file_path):
    """
    Guarda los datos de vuelo en un archivo de texto.
    """
    try:
        with open(txt_file_path, mode='w') as file:
            for flight_number, info in flight_data.items():
                file.write(f"{flight_number}: Departure: {info['departure']}, Arrival: {info['arrival']}\n")
    except IOError as e:
        print(f"Error al escribir el archivo {txt_file_path}: {e}")