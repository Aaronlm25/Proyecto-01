import requests
import threading
import static.python.gather as data_collector
from autocorrect import revise

KEY = 'a3117bc0d7c113aba1f25b2fb28748e1'
LOCK = threading.Lock()

def get_weather(city : str):
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
        
def determine_icon(json_data : dict): # faltan implementar los svg
    """
    Determina el icono basado en el ID del clima.

    Utiliza un diccionario que mapea los IDs de clima a los nombres de archivo de iconos correspondientes.

    Args:
        json_data (dict) : Informacion del clima de una ubicacion.
    """
    icon_map = {
        range(200, 233): "storm_icon.svg",         # Tormenta
        range(300, 322): "light_rain_icon.svg",    # Lluvia ligera
        range(500, 505): "rain_icon.svg",          # Lluvia
        511: "snow_icon.svg",                      # Nieve
        range(520, 532): "rain_icon.svg",          # Lluvia
        range(600, 623): "snow_icon.svg",          # Nieve
        range(701, 782): "fog_icon.svg",           # Neblina
        800: "clear_icon.svg",                     # Despejado
        801: "partly_cloudy_icon.svg",             # Algunas nubes
        802: "clouds_icon.svg",                    # Nubes
        range(803, 805): "cloudy_icon.svg"         # Nublado
    }
    try:
        weather_id = json_data['weather'][0]['id']
        icon = 'default_icon.svg'
        for key in icon_map.keys():
            if weather_id == key or (isinstance(key, range) and weather_id in key):
                icon = icon_map[key]
                break
        json_data['weather'][0]['icon'] = icon
    except KeyError as e:
        print(f"Error: Faltan claves en los datos del clima: {e}")

def search_by_iata(iata_code : str):
    """
    Hace una peticion a la API segun un codigo IATA.

    Args:
        iata_code (str): Código IATA del aeropuerto.

    Returns:
        weather (dict): Informacion del clima.
    """
    city = data_collector.get_city(iata_code)
    if not city:
        return None
    
    weather = get_weather(city)
    if weather:
        determine_icon(weather)
    return weather
        
def search_by_city(city : str):
    """
    Hace una petición a la API según una ciudad.

    Args:
        city (str): Nombre de la ciudad.

    Returns:
        weather: Informacion del clima.
    """
    similar = revise(city, 0.7)
    if not similar:
        similar = [city]
    
    weather = get_weather(similar[0])
    if weather:
        determine_icon(weather)
    return weather

def search_by_id(flight_number : str):
    """
    Realiza una búsqueda del clima para una ciudad en función del número de vuelo.

    Args:
        flight_number (str): Número de vuelo que se utilizará para buscar la información.

    Returns:
        flight_weather (tuple): Contiene la informacion del clima del lugar de destino y de partida 
                                de un vuelo.
    """
    flight_info = data_collector.search_flight(flight_number)
    if not isinstance(flight_info, dict):
        return ()
    departure = data_collector.get_city(flight_info.get('departure', ''))
    arrival = data_collector.get_city(flight_info.get('arrival', ''))
    if not departure or not arrival:
        return ()
    flight_weather = (get_weather(departure), get_weather(arrival))
    if flight_weather[0]:
        determine_icon(flight_weather[0])
    if flight_weather[1]:
        determine_icon(flight_weather[1])
    return flight_weather
