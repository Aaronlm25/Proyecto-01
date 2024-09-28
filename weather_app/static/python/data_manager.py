import csv
from static.python.path_manager import FileManager, FileNotFound

class DataCollector:
    """
    Clase para recolectar datos desde archivos CSV.

    Args:
        file_manager (FileManager): Instancia de FileManager para obtener las rutas de los archivos.
    """
    
    def __init__(self, file_manager: FileManager):
        """
        Inicializa la clase DataCollector cargando los datos desde los archivos.

        Args:
            file_manager (FileManager): Instancia de FileManager para obtener las rutas de los archivos.
        """
        flight_path = file_manager.get_flight_path()
        destiny_path = file_manager.get_destiny_path()
        self._flight_data = self.load_flight_data(flight_path)
        self._iata_data = self.load_iata_data(destiny_path)
        self._cities = self.load_cities(destiny_path)
        self._destiny_data = self.load_destiny_data(destiny_path)

    @staticmethod
    def load_flight_data(path: str) -> dict:
        """
        Carga los datos de vuelos desde un archivo CSV.

        Args:
            path (str): Ruta del archivo CSV que contiene los datos de vuelos.

        Returns:
            dict: Un diccionario con los datos de los vuelos.
        """
        flight_data = {}
        try:
            with open(path, mode='r', encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    flight_number = row[0]
                    departure_iata = row[1]
                    arrival_iata = row[2]
                    flight_data[flight_number] = {'departure': departure_iata, 'arrival': arrival_iata}
        except FileNotFoundError:
            print(f"Error: El archivo {path} no se encuentra.")
        return flight_data

    @staticmethod
    def load_iata_data(path: str) -> dict:
        """
        Carga los datos de ciudades e IATA desde un archivo CSV.

        El archivo CSV debe tener el siguiente formato:
        Ciudades,IATA,Aeropuerto

        Args:
            path (str): Ruta del archivo CSV que contiene los datos.

        Returns:
            dict: Un diccionario donde las claves son los códigos IATA del aeropuerto,
                  y los valores son diccionarios con la información de la ciudad y el aeropuerto.
        """
        iata_data = {}
        try:
            with open(path, mode='r', encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    city = row[0]
                    iata_code = row[2]
                    iata_data[iata_code] = city
        except FileNotFoundError:
            print(f"Error: El archivo {path} no se encuentra.")
        return iata_data

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
        destiny_data = []
        with open(path, mode='r', encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)
            destiny_data = [row[0] for row in list(reader)]
        return destiny_data
 
    def get_destiny_data(self) -> list:
        """
        Devuelve los datos de destino cargados.

        Returns:
            list: lista de destinos cargados desde el archivo CSV.
        """
        return self._destiny_data
    
    def get_cities(self) -> list:
        """
        Devuelve las ciudades cargadas.

        Returns:
            list: lista de ciudades cargadas desde el archivo CSV.
        """
        return self._cities
    
    def get_city(self, iata_airport: str) -> str:
        """
        Obtiene el nombre de la ciudad basado en el código IATA del aeropuerto.

        Args:
            iata_airport (str): Código IATA del aeropuerto.

        Returns:
            str: Nombre de la ciudad correspondiente al código IATA del aeropuerto, o None si no se encuentra.
        """
        return self._iata_data.get(iata_airport)

    def search_flight(self, ticket: str) -> dict:
        """
        Busca la información del vuelo basado en el número de ticket.
        
        Args:
            ticket (str): Número del ticket de vuelo.
        
        Returns:
            dict: Un diccionario con la información del vuelo (salida y llegada).
        """
        return self._flight_data.get(ticket)

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
        Maneja excepciones si los archivos no son encontrados.

        Raises:
            FileNotFound: Si el archivo no existe.
        """
        self.file_manager = FileManager()
        try:
            self.data_manager = DataCollector(self.file_manager)
        except FileNotFound as e:
            print(f"Error: {e}")
            self.data_manager = None

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