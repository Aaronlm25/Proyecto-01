import json
import time
import threading
from pathlib import Path
from threading import Thread
from requests import HTTPError, RequestException
from weather_manager import get_weather
from static.python.data_manager import DataCollector
from static.python.path_manager import FileManager, FileNotFound

FILE_MANAGER=FileManager()
try:
    DATA_MANAGER = DataCollector(FILE_MANAGER)
except FileNotFound as e:
    print(f"Error: {e}")
    
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
        self.weather_records = dict()
        self.STOP_FLAG = threading.Event() 
        self.get_data()
        self.thread = None
        self.LOCK = threading.Lock()


    def get_data(self):
        """
        Obtiene el cache como un diccionario cuyas llaves son los nombres de las 
        ciudades y los valores son objetos json

        Returns:
            self.weather_records: Un diccionario con todos los climas de las ciudades registradas
        """
        raw_data = []
        if len(self.weather_records) == 0:
            try:
                with self.path.open('r', encoding='utf-8') as file:
                    if self.path.stat().st_size != 0:
                        raw_data = json.load(file)
            except json.JSONDecodeError:
                raise InvalidCacheFileException('El formato del cache es invalido.')
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
        with self.LOCK:
            name = weather['name']
            self.weather_records[name] = weather
        
    def __update_weather_records(self, destiny_data : list):
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
        REQUEST_INTERVAL = 1.1
        THREE_HOUR_INTERVAL = 10800
        i = 0
        while not self.STOP_FLAG.is_set():
            data = destiny_data[i]
            time.sleep(REQUEST_INTERVAL)
            weather = None
            try:
                weather = get_weather(data, self.weather_records)
            except (RequestException, HTTPError):
                weather = None
            if weather:
                self.update(weather)
            i += 1
            if i == len(destiny_data):
                i = 0
                self.__save()
                self.__sleep(THREE_HOUR_INTERVAL)

    def __sleep(self, duration : int):
        """
        Args:
            duration (int) : cantidad a esperar en segundos.
        Permite esperar la canitidad deseada con la caracteristica de poder
        deterner la espera.
        """
        for i in range(duration):
            if self.STOP_FLAG.is_set():
                break
            time.sleep(1)

    def start(self):
        """
        Comienza el proceso del cache y las peticiones de los climas.
        """
        if not self.thread:
            data = DATA_MANAGER.get_destiny_data()
            self.thread = Thread(target=self.__update_weather_records, args=[data], name='cache')
            self.thread.start()

    def stop(self):
        """
        Detiene el proceso del cache y las peticiones de los climas.
        Guarda la informacion recolectada por weather_records en el archivo
        cache.json.
        """
        self.STOP_FLAG.set()
        if self.thread:
            self.thread.join()
        self.__save()

    def __save(self):
        """
        Guarda la informacion recolectada por weather_records en el archivo
        cache.json.
        """
        with self.LOCK:
            raw_data = []
            for weather in self.weather_records.values():
                raw_data.append(weather)
            with self.path.open('w', encoding='utf-8') as file:
                json.dump(raw_data, file, indent=4, ensure_ascii=False)

    def __existance_insurer(self, path):
        """
        Se asegura de que la ruta y el archivo existan.
        """
        self.path = Path(path)
        if self.path.suffix != '.json':
            raise InvalidCacheFileException('El archivo cache deber ser .json')
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.touch(exist_ok=True)
        
    