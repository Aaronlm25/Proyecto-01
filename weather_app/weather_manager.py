import requests
import threading
import static.python.gather as data_collector
from weather import Weather

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
        
def search_by_iata(iata_code):
    """
    Hace una peticion a la API segun un codigo IATA.

    Args:
        iata_code (str): Código IATA del aeropuerto.

    Returns:
        Weather: Administrador de la informacion del clima
    """
    city = data_collector.get_city(iata_code)
    return Weather(get_weather(city))
        
def search_by_city(city):
    """
    Hace una petición a la API según una ciudad.

    Args:
        city (str): Nombre de la ciudad.

    Returns:
        Weather: Administrador de la informacion del clima
    """
    return Weather(get_weather(city))

        
def search_by_id(flight_number):
    """
    Realiza una búsqueda del clima para una ciudad en función del número de vuelo.

    Args:
        flight_number (str): Número de vuelo que se utilizará para buscar la información.

    Returns:
        Weather: Administrador de la informacion del clima
    """
    # Busca la información del vuelo utilizando el número de vuelo proporcionado.
    flight_info = data_collector.search_flight(flight_number)
    # Verifica si 'flight_info' es un diccionario para asegurarse de que la búsqueda fue exitosa.
    if isinstance(flight_info, dict):  
        departure = flight_info['departure']  
        arrival = flight_info['arrival']      
    else:
        return None  
    if departure == "MEX":
        city = data_collector.get_city(departure)
    else:
        city = data_collector.get_city(arrival)
    return Weather(get_weather(city))
