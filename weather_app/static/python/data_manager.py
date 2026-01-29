""" 
Clases Data Collector y Data Manager para recolectar datos desde archivos CSV 
evita la lectura constante de los archivos con un patron singleton.

Author: @Gibran-RL
Version: 1.0 
"""
import csv
from static.python.path_manager import FileManager


class DataCollector:
    """
    Clase para recolectar datos desde archivos CSV.

    Atributes:
        file_manager (FileManager): Instancia de FileManager para obtener las rutas de los archivos.
        destiny_path (str): Ruta del archivo CSV que contiene los datos de destinos.
        cities (list): Lista de ciudades.
    """

    def __init__(self, file_manager: FileManager):
        """
        Inicializa la clase DataCollector cargando los datos desde los archivos.

        Args:
            file_manager (FileManager): Instancia de FileManager para obtener las rutas de los archivos.

        Raises:
            FileNotFoundError: Si alguno de los archivos no se encuentra.
            UnicodeDecodeError: Si alguno de los archivos no está codificado en UTF-8.
        """
        destiny_path = file_manager.get_destiny_path()
        self._cities = self.load_cities(destiny_path)
        self._destiny_data = self.load_destiny_data(destiny_path)

    @staticmethod
    def load_cities(path: str) -> list:
        """
        Carga los datos de las ciudades desde un archivo CSV.

        Args:
            path (str): Ruta del archivo CSV que contiene los datos de ciudades.

        Returns:
            ciudades (list): lista de las ciudades ordenada.
        """
        cities = []
        with open(path, 'r', encoding="utf8", newline='') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                cities.append(row[0])
        cities = sorted(cities, key=lambda city: city.lower())
        return cities

    @staticmethod
    def load_destiny_data(path: str) -> list:
        """
        Lee los datos de destinos desde un archivo CSV y los carga en una lista.

        El archivo CSV debe tener los datos en el siguiente formato:
        city_name, iata_code, airport_name

        Args:
            path (str): Ruta del archivo CSV que contiene los datos de destinos.

        Returns:
            list: Una lista de listas, donde cada sublista contiene la información de una ciudad.
        """
        with open(path, mode='r', encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)
            destiny_data = [row for row in reader]
        return destiny_data

    def get_cities(self) -> list:
        """
        Devuelve las ciudades cargadas.

        Returns:
            list: lista de ciudades cargadas desde el archivo CSV.
        """
        return self._cities

    def get_destiny_data(self) -> list:
        """
        Devuelve los datos de destino cargados.

        Returns:
            list: lista de destinos cargados desde el archivo CSV.
        """
        return self._destiny_data


class DataManager:
    """
    Clase para manejar la instancia única de DataManager (Singleton).
    """
    _instance = None

    def __new__(cls):
        """
        Implementa el patrón Singleton para asegurarse de que sólo exista una instancia de DataManager.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize_managers()
        return cls._instance

    def _initialize_managers(self):
        """
        Inicializa los objetos de FileManager y DataCollector.
        """
        self.file_manager = FileManager()
        self.data_manager = DataCollector(self.file_manager)

    def get_file_manager(self) -> FileManager:
        """
        Retorna la instancia de FileManager.

        Returns:
            FileManager: Manejo de archivos.
        """
        return self.file_manager

    def get_data_collector(self) -> DataCollector:
        """
        Retorna la instancia de DataCollector.

        Returns:
            DataCollector: Recolector de datos.
        """
        return self.data_manager
