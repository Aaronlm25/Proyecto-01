"""
Clases cache y excepcion de cache, permite la 
recoleccion de datos en segundo plano y 
evita peticiones redundantes.

Author: @Gibran-RL @pamoraf @Aaronlm25 @Azakhy
Version: 1.0
"""
import json
import time
import threading
from pathlib import Path
from threading import Thread
from weather_exceptions import WeatherRequestError
from json import JSONDecodeError
from weather_manager import get_weather

class InvalidCacheFileError(Exception):
    """
    Clase de excepcion del archivo de cache dado, se lanza cuando el archivo no es .json.
    """
    def __init__(self, message : str):
        """
            Args:
                message (str) : Mensaje de error que describe la excepcion.
        """
        super().__init__(message)

class Cache:
    """
    Clase para manejar el cache de los climas.

    Attributes:
        path (str): La ruta del archivo de cache.
        __cities (list) : Lista de ciudades a considerar.
        weather_records (dict) : Diccionario que contiene el clima de las ciudades.
        __STOP_FLAG (Event) : Bandera para que controla el proceso de cache.
        __thread (Thread) : Hilo de ejecucion destinado ejecutar el metodo __update_cache.
        __LOCK (Lock) :  Perimte que comportaminto compartido por diferentes hilos,
                         se ejecute de manera segura.
    """
    def __init__(self, path : str, cities : list):
        """
        Inicializa la clase Cache cargando las ciudades y la ruta del .json.

        Args:
            path (str) : La ruta del .json.
            cities (list) : Lista de los nombres de las ciudades

        Raises:
            InvalidCacheFileError : si el nombre de la ruta no coincide con un .json o el json 
                                    no tiene el formato apropiado (utf-8)
        """
        self.__existance_insurer(path)
        self.__cities = cities
        self.weather_records = dict()
        self.__STOP_FLAG = threading.Event() 
        self.__STOP_FLAG.set()
        self.__thread = None
        self.__LOCK = threading.Lock()
        self.get_data()

    def get_data(self) -> dict:
        """
        Obtiene el cache como un diccionario cuyas llaves son los nombres de las 
        ciudades y los valores son objetos json.

        Returns:
            self.weather_records (dict): Un diccionario con todos los climas de las ciudades registradas.
        
        Raises:
            InvalidCacheFileError : Si el formato del cache es invalido.
        """
        raw_data = []
        if len(self.weather_records) == 0:
            try:
                with self.path.open('r', encoding='utf-8') as file:
                    if self.path.stat().st_size != 0:
                        raw_data = json.load(file)
            except JSONDecodeError:
                raise InvalidCacheFileError('El formato del cache es invalido.')
            for weather in raw_data:
                name = weather['name']
                self.weather_records[name] = weather
        return self.weather_records

    def update(self, weather : dict):
        """
        Actualiza el clima de una sola ciudad.

        Args:
            weather : Objeto json que contiene informacion del clima de una ciudad.
        """
        with self.__LOCK:
            name = weather['name']
            self.weather_records[name] = weather
        
    def __update_weather_records(self):
        """
        Proceso en segundo plano que hace las peticiones de los climas de las 
        distintas ciudades registradas.
        """
        THREE_HOUR_INTERVAL = 10800
        i = 0
        while not self.__STOP_FLAG.is_set():
            data = self.__cities[i]
            weather = None
            try:
                weather = get_weather(data, self.weather_records)
            except (WeatherRequestError, ValueError):
                weather = None
            if weather:
                self.update(weather)
            i += 1
            if i == len(self.__cities):
                i = 0
                self.__save()
                self.__sleep(THREE_HOUR_INTERVAL)

    def __sleep(self, duration : int):
        """
        Permite esperar la canitidad deseada con la caracteristica de poder
        deterner la espera.

        Args:
            duration (int) : Cantidad a esperar en segundos.
        """
        for _ in range(duration):
            if self.__STOP_FLAG.is_set():
                break
            time.sleep(1)

    def start(self):
        """
        Comienza el proceso del cache y las peticiones de los climas.
        """
        self.__STOP_FLAG.clear()
        if not self.__thread:
            self.__thread = Thread(
                target=self.__update_weather_records,
                name='cache'
            )
            self.__thread.start()

    def stop(self):
        """
        Detiene el proceso del cache y las peticiones de los climas.
        Guarda la informacion recolectada por weather_records en el archivo
        cache.json.
        """
        self.__STOP_FLAG.set()
        if self.__thread:
            self.__thread.join()
            self.__thread = None
        self.__save()

    def is_active(self) -> bool:
        """
        Permite saber si se estan haciendo las peticiones de clima.

        Returns:
            bool : El estado de la actividad de las peticiones de clima.
        """
        return not self.__STOP_FLAG.is_set()
    
    def __save(self):
        """
        Guarda la informacion recolectada por weather_records en el archivo
        cache.json.
        """
        with self.__LOCK:
            raw_data = []
            for weather in self.weather_records.values():
                raw_data.append(weather)
            with self.path.open('w', encoding='utf-8') as file:
                json.dump(raw_data, file, indent=4, ensure_ascii=False)

    def __existance_insurer(self, path : str):
        """
        Se asegura de que la ruta y el archivo existan.
        Args : 
            path (str): La ruta del archivo.

        Raises:
            InvalidCacheFileError : Si el formato del cache es invalido.
        """
        self.path = Path(path)
        if self.path.suffix != '.json':
            raise InvalidCacheFileError('El archivo cache deber ser .json')
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.touch(exist_ok=True)