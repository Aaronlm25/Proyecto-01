import csv
from static.python.path_manager import FileManager

class DataCollector:
    _instance = None

    def __new__(cls, file_manager: FileManager):
        """
        Implementación del patrón Singleton. Carga los archivos solo una vez.

        Args:
            file_manager (FileManager): Instancia de FileManager para obtener las rutas de los archivos.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            flight_path = file_manager.get_flight_path()
            iata_path = file_manager.get_iata_path()
            location_path = file_manager.get_location_path()
            cities_path = file_manager.get_cities_path()
            
            destiny_path=file_manager.get_destiny_path()

            cls._instance._flight_data = cls.load_flight_data(flight_path)
            cls._instance.iata_data = cls.load_iata_data(iata_path)
            cls._instance._location_data = cls.load_location_data(location_path)
            cls._instance._cities = cls.load_cities(cities_path)
            cls._instance._destiny_data=cls.load_destiny_data(destiny_path)
            
        return cls._instance

    @staticmethod
    def load_flight_data(path):
        """
        Carga los datos de vuelos desde un archivo CSV.
        """
        flight_data = {}
        try:
            with open(path, mode='r') as file:
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
    def load_iata_data(path):
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
            with open(path, mode='r') as file:
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
    def load_location_data(path):
        """
        Carga los datos de latitud y longitud de origen y destino desde un archivo CSV.

        El archivo CSV debe tener el siguiente formato:
        origin,destination,origin_latitude,origin_longitude,destination_latitude,destination_longitude

        Args:
            path (str): Ruta del archivo CSV que contiene los datos de ubicaciones.

        Returns:
            dict: Un diccionario donde las claves son los códigos IATA de las ciudades,
                y los valores son diccionarios con la latitud y longitud.
        """
        location_data = {}
        try:
            with open(path, mode='r') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    origin = row[0]
                    destination = row[1]
                    origin_latitude = float(row[2])
                    origin_longitude = float(row[3])
                    destination_latitude = float(row[4])
                    destination_longitude = float(row[5])
                    if origin not in location_data:
                        location_data[origin] = {'latitude': origin_latitude, 'longitude': origin_longitude}
                    if destination not in location_data:
                        location_data[destination] = {'latitude': destination_latitude, 'longitude': destination_longitude}
        except FileNotFoundError:
            print(f"Error: El archivo {path} no se encuentra.")
        return location_data

    @staticmethod
    def load_cities(path):
        """
        Carga los datos de las ciudades

        Args:
            path (str): Ruta del archivo CSV que contiene los datos de ciudades.

        Returns:
            list: lista con las ciudades ordenadas
        """
        ciudades = []
        with open(path, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                ciudades.extend([ciudad for ciudad in row if ciudad.strip()])
        cities = sorted(ciudades, key=lambda x: x.lower())
        return cities
    
    @staticmethod
    def load_destiny_data(path):

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
            next(reader)
            destiny_data = [row[0] for row in list(reader)]
        return destiny_data
 
    def get_destiny_data(self):
        """
        Devuelve los datos de destino cargados.

        Returns:
            list: Lista de destinos cargados desde el archivo CSV.
        """
        return self._destiny_data
    
    def get_cities(self):
        """
        Devuelve las ciudades cargadas.

        Returns:
            list: Lista de ciudades cargadas desde el archivo CSV.
        """
        return self._cities
    
    def get_city(self, iata_airport):
        """
        Obtiene el nombre de la ciudad basado en el código IATA del aeropuerto.

        Args:
        iata_airport (str): Código IATA del aeropuerto.

        Returns:
            str: Nombre de la ciudad correspondiente al código IATA del aeropuerto, o None si no se encuentra.
        """
        try:
            return self.iata_data[iata_airport]
        except KeyError:
            return None

    def search_flight(self, ticket):
        """
        Busca la información del vuelo basado en el número de ticket.
        
        Args:
            ticket (str): Número del ticket de vuelo.
        
        Returns:
            dict or str: Un diccionario con la información del vuelo (salida y llegada)
                         o un mensaje indicando que no se encontró información.
        """
        return self._flight_data.get(ticket, f"No se encontró información para el ticket: {ticket}")

