from pathlib import Path

class FileNotFound(Exception):
    """Excepción personalizada cuando un archivo no se encuentra."""
    def __init__(self, archivo):
        super().__init__(f"File {archivo} does not exist.")

class FileManager:
    def __init__(self, base_dir='./weather_app/static/datalist'):
        self.base_dir = Path(base_dir)
    
    def get_path(self, file_name):
        """Devuelve la ruta completa del archivo en el directorio base."""
        return self.base_dir / file_name

    def check_existence(self, file_name):
        """
        Verifica si el archivo existe. Lanza una excepción si no existe.
        Raises:
            FileNotFound: Si el archivo no existe
        """
        file_path = self.get_path(file_name)
        if not file_path.exists():
            raise FileNotFound(file_path)
        return file_path

    def get_flight_path(self):
        """Devuelve la ruta de vuelos.csv y verifica su existencia."""
        return self.check_existence('vuelos.csv')

    def get_destiny_path(self):
        """Devuelve la ruta de destiny_data.csv y verifica su existencia."""
        return self.check_existence('destiny_data.csv')

    def get_location_path(self):
        """Devuelve la ruta de datos_destinos_viajes.csv y verifica su existencia."""
        return self.check_existence('datos_destinos_viajes.csv')