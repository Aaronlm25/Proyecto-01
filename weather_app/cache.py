import os
import json
import time
import threading
import weather_manager
import static.python.gather as gatherer
from threading import Thread
from pathlib import Path

class InvalidCacheFileException(Exception):
    """
    Clase de excepcion del archivo de cache dado,
    se lanza cuando el archivo no es .json
    """
    def __init__(self, message):
        super().__init__(message)

class Cache:
    """
    Clase para manejar el cache de los climas

    Atributo:
    ---------
    path : str
        La ruta del archivo de cache
    """
    def __init__(self, path : str):
        self.path = path
        self.existance_insurer()
        # Todos los climas de las ciudades registradas
        self.weather_records = dict()
        # Permite detener el hilo donde se calcula el clima
        self.STOP_FLAG = threading.Event() 

    def get_data(self):
        """
        Obtiene el cache como un diccionario cuyas llaves son los nombres de las 
        ciudades y los valores son objetos json

        Regresa
        -------
            self.weather_records: Un diccionario con todos los climas de las ciudades registradas
        """
        self.existance_insurer()
        raw_data = []
        # Si weather_records es vacio intenta ver si hay datos en el archivo .json
        if len(self.weather_records) == 0:
            with open(self.path, 'r') as file:
                if os.path.getsize(self.path) != 0:
                    raw_data = json.load(file)
            for weather in raw_data:
                name = weather['name']
                self.weather_records[name] = weather
        return self.weather_records

    def update(self, weather):
        """
        Actualiza el clima de una sola ciudad

        Parametros
        ----------
            weather : objeto json que contiene informacion del clima de una ciudad
        """
        name = weather['name']
        self.weather_records[name] = weather
        
    def update_weather(self, destiny_data):
        """
        Proceso en segundo plano que hace las peticiones de los climas de las 
        distintas ciudades registradas.

        Parametros
        ----------
            destiny_data: lista de las ciudades registradas cada elemento es una lista
                          de tamano 3 que contiene:
                          [0] : Nombre de la ciudad
                          [1] : IATA
                          [2] : Codigo de aeroopuerto
        """
        for data in destiny_data:
            if self.STOP_FLAG.is_set():
                break
            # Evita baneos pues la api solo deja hacer request 60 veces por minuto 
            time.sleep(1.2)
            # Weather puede ser None si ocurrio un error al hacer el request
            weather = weather_manager.get_weather(data[0])
            if weather:
                self.update(weather)

    def start(self):
        """
        Comienza el proceso del cache y las peticiones de los climas.
        """
        # lista de las ciudades registradas
        data = gatherer.get_destiny_data('./weather_app/static/datalist/datos_destinos.csv')
        thread = Thread(target=self.update_weather, args=[data])
        thread.start()

    def stop(self):
        """
        Detiene el proceso del cache y las peticiones de los climas.
        Guarda la informacion recolectada por weather_records en el archivo
        indicado por path, esto es se guardan los objetos json.
        """
        raw_data = []
        for weather in self.weather_records.values():
            raw_data.append(weather)
        with open(self.path, 'w') as file:
            json.dump(raw_data, file, indent=4)
        self.STOP_FLAG.set()

    def existance_insurer(self):
        """
        Se asegura de que la ruta y el archivo existan.
        """
        file = Path(self.path)
        if file.suffix != '.json':
            raise InvalidCacheFileException('El archivo cache deber ser .json')
        # Asegúrate de que el directorio exista
        file.parent.mkdir(parents=True, exist_ok=True)
        file.touch(exist_ok=True)
    