import requests
import threading
import time
from static.python.data_manager import DataCollector, DataManager
from autocorrect import revise
from requests.exceptions import RequestException, HTTPError

KEY = 'a3117bc0d7c113aba1f25b2fb28748e1'
LOCK = threading.Lock()
FLIGHT_DATA_PATH = './weather_app/static/datalist/vuelos.csv'
IATA_DATA_PATH = './weather_app/static/datalist/datos_destinos.csv'
LOCATION_DATA_PATH = './weather_app/static/datalist/datos_destinos_viajes.csv'
CITIES_DATA_PATH = './weather_app/static/datalist/cities_2.csv'
data_collector = DataCollector(FLIGHT_DATA_PATH, IATA_DATA_PATH, LOCATION_DATA_PATH, CITIES_DATA_PATH)
data_manager = DataManager(data_collector)

def get_weather(city: str, weather_records: dict):
    if not is_weather_valid(city, weather_records):
        with LOCK:
            try:
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={KEY}&units=metric&lang=es"
                response = requests.get(url)
                response.raise_for_status()
                return response.json()
            except (RequestException, HTTPError) as e:
                raise RequestException('Error al hacer el request') from e
    else:
        return weather_records[city]

def is_weather_valid(city: str, weather_records: dict):
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
        range(200, 233): "img/Storm.png",         
        range(300, 322): "light_rain_icon.svg",    
        range(500, 505): "rain_icon.svg",         
        511: "img/Snow.png",                      
        range(520, 532): "rain_icon.svg",          
        range(600, 623): "img/Snow.png",          
        range(701, 782): "fog_icon.svg",           
        800: "img/Sunny.png",                     
        801: "img/Parcialmente nublado.png",            
        802: "img/Nublado.png",                   
        range(803, 805): "img/Nublado.png"         
    }
    try:
        weather_id = json_data['weather'][0]['id']
        icon = 'default_icon.svg'
        for key in icon_map:
            if weather_id == key or (isinstance(key, range) and weather_id in key):
                icon = icon_map[key]
                break
        json_data['weather'][0]['icon'] = icon
    except KeyError:
        raise ValueError('El json es invalido')

def search_by_iata(iata_code: str, weather_records: dict):
    """
    Hace el request del clima a la API de acuerdo al codigo IATA

    Args:
        iata_code (str): codigo IATA.

    Returns:
        weather (dict): Informacion del clima.
    """
    city = data_manager.get_city(iata_code)
    if not city:
        raise ValueError('Ciudad invalida')
    weather = get_weather(city, weather_records)
    determine_icon(weather)
    return weather

def search_by_city(city: str, weather_records: dict):
    """
    Hace el request del clima a la API de acuerdo al nombre de una ciudad

    Args:
        city (str): nombre de la ciudad

    Returns:
        weather (dict): Informacion del clima.
    """
    similar = revise(city, 0.7)
    if not similar:
        raise ValueError('Ciudad invalida')
    weather = get_weather(similar[0], weather_records)
    determine_icon(weather)
    return weather

def search_by_id(flight_number: str, weather_records: dict):
    """
    Hace el request del clima a la API de acuerdo con un numero de ticket

    Args:
        flight_number (str): Ticket del vuelo.

    Returns:
        flight_weather (tuple): Contiene la informacion del clima de llegada y de salida.
    """
    try:
        flight_info = data_manager.search_flight(flight_number)
    except TypeError as e:
        raise ValueError('Vuelo no encontrado.')
    departure = data_manager.get_city(flight_info['departure'])
    arrival = data_manager.get_city(flight_info['arrival'])
    if not departure or not arrival:
        raise ValueError('Ticket invalido.')
    flight_weather = (get_weather(departure, weather_records), get_weather(arrival, weather_records))
    determine_icon(flight_weather[0])
    determine_icon(flight_weather[1])
    return flight_weather