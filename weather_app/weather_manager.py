import requests
import csv
import threading
import static.python.gather as gatherer

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
        
def seach_by_iata(iata_code):
    """
    Hace una peticion a la API segun un codigo IATA.

    Args:
        iata_code (str): Código IATA del aeropuerto.

    Returns:
        dict: Información del clima si el código IATA es válido.
        dict: Error Código IATA no válido si no lo es.tr: Error Codigo IATA invalido si
    """
    
    weather_data={}
    city = gatherer.get_city(iata_code)
    if city:
        weather_data['city'] =get_weather(city)
    else:
        weather_data['error'] = "Código IATA no válido."
    return weather_data
        
def seach_by_city(city):
    """
    Hace una petición a la API según una ciudad.

    Args:
        city (str): Nombre de la ciudad.

    Returns:
        dict: Información del clima si la ciudad es válida.
        dict: Error 'Ciudad no válida' si no lo es.
    """
    weather_data = {}
    weather_info = get_weather(city)
    
    if weather_info:
        if 'weather' in weather_info:
            weather_data['city'] = weather_info
        else:
            weather_data['error'] = "Ciudad no válida."
    else:
        weather_data['error'] = "Error al obtener los datos del clima."
    
    return weather_data

        
def seach_by_id(flight_number):
    """
    Realiza una búsqueda del clima para una ciudad en función del número de vuelo.

    Args:
        flight_number (str): Número de vuelo que se utilizará para buscar la información.

    Returns:
        dict: Información del clima para la ciudad de salida o llegada.
              Si el vuelo no se encuentra, devuelve un mensaje de error.
    """
    weather_data = {}
    
    # Busca la información del vuelo utilizando el número de vuelo proporcionado.
    flight_info = gatherer.buscar_vuelo(flight_number)
    
    # Verifica si 'flight_info' es un diccionario para asegurarse de que la búsqueda fue exitosa.
    if isinstance(flight_info, dict):  
        departure = flight_info['departure']  
        arrival = flight_info['arrival']      
    else:
        weather_data['error'] = flight_info
        return weather_data  
    
    if departure == "MEX":
        city = gatherer.get_city(departure)
    else:
        city = gatherer.get_city(arrival)
    
    weather_data['city'] = get_weather(city)
    
    return weather_data
