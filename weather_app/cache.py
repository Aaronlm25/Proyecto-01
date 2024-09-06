import csv
import json
import time
import threading
from pathlib import Path
from threading import Thread

from requests import HTTPError, RequestException
from weather_manager import get_weather
from static.python.data_manager import DataCollector, DataManager

FLIGHT_DATA_PATH = './weather_app/static/datalist/vuelos.csv'
IATA_DATA_PATH= './weather_app/static/datalist/datos_destinos.csv'

data_colector = DataCollector(FLIGHT_DATA_PATH,IATA_DATA_PATH)
data_manager = DataManager(data_colector)

class InvalidCacheFileException(Exception):
    """
    Clase de excepcion del archivo de cache dado,
    se lanza cuando el archivo no es .json
    """
    def __init__(self, message : str):
        super().__init__(message)

class Cache:
    """
    Clase para manejar el cache de los climas

    Args:
    path : str
        La ruta del archivo de cache
    """
    def __init__(self, path : str):
        self.__existance_insurer(path)
        # Todos los climas de las ciudades registradas
        self.weather_records = dict()
        # Permite detener el hilo donde se calcula el clima
        self.STOP_FLAG = threading.Event() 

    def get_destiny_data(self, path):

        """
        Lee los datos de destinos desde un archivo CSV y los carga en una lista.

        El archivo CSV debe tener los datos en el siguiente formato:
        city_name, iata_code, airport_name

        Args:
            path (str): Ruta del archivo CSV que contiene los datos de destinos.

        Returns:
            list: Una lista de listas, donde cada sublista contiene la información de una ciudad.
        """
        destiny_data = []
        with open(path, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Salta el encabezado si existe
            destiny_data = list(reader)
        return destiny_data

    def get_data(self):
        """
        Obtiene el cache como un diccionario cuyas llaves son los nombres de las 
        ciudades y los valores son objetos json

        Returns:
            self.weather_records: Un diccionario con todos los climas de las ciudades registradas
        """
        raw_data = []
        # Si weather_records es vacio intenta ver si hay datos en el archivo .json
        if len(self.weather_records) == 0:
            with self.path.open('r') as file:
                if self.path.stat().st_size != 0:
                    raw_data = json.load(file)
            for weather in raw_data:
                name = weather['name']
                self.weather_records[name] = weather
        return self.weather_records

    def update(self, weather : dict):
        """
        Actualiza el clima de una sola ciudad

        Args:
            weather : objeto json que contiene informacion del clima de una ciudad
        """
        name = weather['name']
        self.weather_records[name] = weather
        
    def update_weather(self, destiny_data : list):
        """
        Proceso en segundo plano que hace las peticiones de los climas de las 
        distintas ciudades registradas.

        Args:
            destiny_data: lista de las ciudades registradas cada elemento es una lista
                          de tamano 3 que contiene:
                          [0] : Nombre de la ciudad
                          [1] : IATA
                          [2] : Codigo de aeroopuerto
        """
        REQUEST_INTERVAL = 1.2
        THREE_HOUR_INTERVAL = 10800
        i = 0
        while not self.STOP_FLAG.is_set():
            data = destiny_data[i]
            time.sleep(REQUEST_INTERVAL)
            try:
                weather = get_weather(data[0], self.weather_records)
            except (RequestException, HTTPError):
                weather = None
            if weather:
                self.update(weather)
            i += 1
            if i == len(destiny_data):
                i = 0
                time.sleep(THREE_HOUR_INTERVAL)

    def start(self):
        """
        Comienza el proceso del cache y las peticiones de los climas.
        """
        # lista de las ciudades registradas
        data = self.get_destiny_data('./weather_app/static/datalist/datos_destinos.csv')
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
        with self.path.open('w') as file:
            json.dump(raw_data, file, indent=4)
        self.STOP_FLAG.set()

    def __existance_insurer(self, path):
        """
        Se asegura de que la ruta y el archivo existan.
        """
        self.path = Path(path)
        if self.path.suffix != '.json':
            raise InvalidCacheFileException('El archivo cache deber ser .json')
        # Asegúrate de que el directorio exista
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.touch(exist_ok=True)
        
    