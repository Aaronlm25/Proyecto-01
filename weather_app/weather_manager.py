import requests
import threading
import time
import os
from static.python.data_manager import DataManager
from requests.exceptions import RequestException, HTTPError
from dotenv import load_dotenv
from weather_exceptions import *

load_dotenv()
LOCK = threading.Lock()
DATA_COLLECTOR = DataManager().get_data_collector()

def get_weather(city: str, weather_records: dict) -> dict:
    """
    Obtiene los datos meteorológicos para una ciudad específica.
    Si los datos meteorológicos ya están en los registros y son válidos, se devuelve esa información. 
    Si no, se realiza una solicitud a la API de OpenWeather para obtener la información actualizada.

    Args:
        city (str): El nombre de la ciudad para la que se desea obtener el clima.
        weather_records (dict): Un diccionario que contiene los registros meteorológicos por ciudad.

    Returns:
        dict: Un diccionario con la información meteorológica actual de la ciudad.

    Raises:
        WeatherRequestError: Si ocurre un error al realizar la solicitud a la API.
        ValueError: Si el objeto JSON no existe o no es válido.
    """
    KEY = os.getenv('KEY')
    REQUEST_INTERVAL = 1.1
    if not is_weather_valid(city, weather_records):
        with LOCK:
            try:
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={KEY}&units=metric&lang=es"
                response = requests.get(url)
                response.raise_for_status()
                weather = response.json()
                determine_icon(weather)
                weather['name'] = city
                time.sleep(REQUEST_INTERVAL)
                return weather
            except (RequestException, HTTPError) as e:
                raise WeatherRequestError('Error al hacer el request') from e
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
        bool: True si los registros meteorológicos son válidos, False en caso contrario.
    """
    THREE_HOUR_INTERVAL = 10800
    if city not in weather_records.keys():
        return False
    weather = weather_records[city]
    requested_time = weather['dt']
    return time.time() - requested_time < THREE_HOUR_INTERVAL

def determine_icon(json_data: dict):
    """
    Determina el icono de acuerdo al ID.
    Usa un diccionario que mapea los IDs a los respectivos iconos.

    Args:
        json_data (dict): Información del clima de una ubicación.

    Raises:
        ValueError: Si el objeto JSON no existe o no es válido.
    """
    if not json_data:
        raise ValueError('El objeto JSON es None')
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
        raise ValueError('El JSON es inválido') from e

def search_by_iata(iata_code: str, weather_records: dict) -> dict:
    """
    Hace la solicitud del clima a la API de acuerdo al código IATA.

    Args:
        iata_code (str): Código IATA.

    Returns:
        dict: Información del clima.

    Raises:
        IATANotFoundError: Si la ciudad no tiene un IATA asociado.
    """
    city = DATA_COLLECTOR.get_city(iata_code)
    if not city:
        raise IATANotFoundError('No se encontró el código IATA')
    weather = get_weather(city, weather_records)
    return weather

def search_by_city(city: str, weather_records: dict) -> dict:
    """
    Hace la solicitud del clima a la API de acuerdo al nombre de una ciudad.

    Args:
        city (str): Nombre de la ciudad.

    Returns:
        dict: Información del clima.

    Raises:
        CityNotFoundError: Si no se encontro la ciudad.
    """
    if city not in DATA_COLLECTOR.get_cities():
        raise CityNotFoundError('No se encontro la ciudad proporcionada')
    weather = get_weather(city, weather_records)
    return weather

def search_by_id(flight_number: str, weather_records: dict) -> tuple:
    """
    Hace la solicitud del clima a la API de acuerdo con un número de ticket.

    Args:
        flight_number (str): Ticket del vuelo.

    Returns:
        tuple: Contiene la información del clima de llegada y de salida.

    Raises:
        FlightNotFoundError: Si el vuelo no tiene datos asociados.
    """
    flight_info = DATA_COLLECTOR.search_flight(flight_number)
    if not flight_info:
        raise FlightNotFoundError('No se tiene registrado ese ticket.')
    departure = DATA_COLLECTOR.get_city(flight_info['departure'])
    arrival = DATA_COLLECTOR.get_city(flight_info['arrival'])
    if not departure or not arrival:
        raise FlightNotFoundError('Ticket con destino u origen invalidos.')
    flight_weather = (get_weather(departure, weather_records), get_weather(arrival, weather_records))
    return flight_weather