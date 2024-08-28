import requests
import time
import cache
import threading
KEY = 'a3117bc0d7c113aba1f25b2fb28748e1'
STOP_EVENT = threading.Event()
def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={KEY}&units=metric&lang=es"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener datos: {e}")
        return None
    
# Se usa para calcular constantemente las climas, en un hilo de ejecucion.
def update_weather(destiny_data):
    for data in destiny_data:
        if STOP_EVENT.is_set():
            break   
        time.sleep(1.2)
        weather = get_weather(data[0])
        if weather:
            cache.update('./weather_app/static/json/cache.json', weather)

