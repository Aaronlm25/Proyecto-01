import requests
import threading
import time
import os
from static.python.data_manager import DataCollector
from static.python.path_manager import FileManager, FileNotFound
from requests.exceptions import RequestException, HTTPError
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv('KEY')
LOCK = threading.Lock()
FILE_MANAGER = FileManager()
try:
    DATA_MANAGER = DataCollector(FILE_MANAGER)
except FileNotFound as e:
    print(f"Error: {e}")

def get_weather(city: str, weather_records: dict) -> dict:
    """
    Obtiene los datos meteorológicos para una ciudad específica.
    Si los datos meteorológicos ya están en los registros y son válidos, se devuelve esa información. 
    Si no, se realiza una solicitud a la API de OpenWeather para obtener la información actualizada.

    Args:
        city (str): El nombre de la ciudad para la que se desea obtener el clima.
        weather_records (dict): Un diccionario que contiene los registros meteorológicos por ciudad.

    Returns:
        weather (dict): Un diccionario con la información meteorológica actual de la ciudad.

    Raises:
        RequestException: Si ocurre un error al realizar la solicitud a la API.
    """
    if not is_weather_valid(city, weather_records):
        with LOCK:
            try:
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={KEY}&units=metric&lang=es"
                response = requests.get(url)
                response.raise_for_status()
                weather = response.json()
                determine_icon(weather)
                return weather
            except (RequestException, HTTPError) as e:
                raise RequestException('Error al hacer el request') from e
    else:
        return weather_records[city]

def is_weather_valid(city: str, weather_records: dict) -> bool:
    """
    Verifica si los registros meteorológicos para una ciudad son válidos.

    Los registros se consideran válidos si la ciudad está presente en el diccionario
    de registros y si la información no ha expirado.

    Args:
        city (str): El nombre de la ciudad que se va a verificar.
        weather_records (dict): Un diccionario que contiene los registros meteorológicos por ciudad.

    Returns:
        (bool): True si los registros meteorológicos son válidos, False en caso contrario.
    """
    THREE_HOUR_INTERVAL = 10800
    if city not in weather_records.keys():
        return False
    weather = weather_records[city]
    requested_time = weather['dt']
    if time.time() - requested_time >= THREE_HOUR_INTERVAL:
        return False
    return True

def determine_icon(json_data: dict):
    """
    Determina el icono de acuerdo al ID.
    Usa un diccionario que mapea los IDs a los respectivos iconos.

    Args:
        json_data (dict): Informacion del clima de una ubicacion.
    """
    if not json_data:
        raise ValueError('The JSON object is None')
    icon_map = {
        range(200, 233): "static/img/storm.gif",         
        range(300, 322): "static/img/light-rain.gif",    
        range(500, 505): "static/img/rain.gif",          
        511: "static/img/snow.gif",                     
        range(520, 532): "static/img/rain.gif",          
        range(600, 623): "static/img/snow.gif",          
        range(701, 782): "static/img/clouds.png",           
        800: "static/img/sunny.png",                     
        801: "static/img/cloud_sun.png",             
        802: "static/img/clouds.png",                    
        range(803, 805): "static/img/clouds.png"         
    }
    try:
        weather_id = json_data['weather'][0]['id']
        icon = 'default_icon.svg'
        for key in icon_map:
            if weather_id == key or (isinstance(key, range) and weather_id in key):
                icon = icon_map[key]
                break
        json_data['weather'][0]['icon'] = icon
    except KeyError as e:
        raise ValueError('El json es invalido') from e

def search_by_iata(iata_code: str, weather_records: dict) -> dict:
    """
    Hace el request del clima a la API de acuerdo al codigo IATA

    Args:
        iata_code (str): codigo IATA.

    Returns:
        weather (dict): Informacion del clima.
    """
    city = DATA_MANAGER.get_city(iata_code)
    if not city:
        raise ValueError('Ciudad invalida')
    weather = get_weather(city, weather_records)
    determine_icon(weather)
    return weather

def search_by_city(city: str, weather_records: dict) -> dict:
    """
    Hace el request del clima a la API de acuerdo al nombre de una ciudad

    Args:
        city (str): nombre de la ciudad

    Returns:
        weather (dict): Informacion del clima.
    """
    weather = get_weather(city, weather_records)
    determine_icon(weather)
    return weather

def search_by_id(flight_number: str, weather_records: dict) -> tuple:
    """
    Hace el request del clima a la API de acuerdo con un numero de ticket

    Args:
        flight_number (str): Ticket del vuelo.

    Returns:
        flight_weather (tuple): Contiene la informacion del clima de llegada y de salida.
    """
    try:
        flight_info = DATA_MANAGER.search_flight(flight_number)
    except TypeError as e:
        raise ValueError('Vuelo no encontrado.')
    departure = DATA_MANAGER.get_city(flight_info['departure'])
    arrival = DATA_MANAGER.get_city(flight_info['arrival'])
    if not departure or not arrival:
        raise ValueError('Ticket invalido.')
    flight_weather = (get_weather(departure, weather_records), get_weather(arrival, weather_records))
    determine_icon(flight_weather[0])
    determine_icon(flight_weather[1])
    return flight_weather