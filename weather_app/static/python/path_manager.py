from pathlib import Path

class FileNotFound(Exception):
    """
    Excepción personalizada cuando un archivo no se encuentra.

    Args:
        archivo (str): Nombre del archivo que no se encuentra.
    """
    def __init__(self, archivo : str):
        super().__init__(f"File {archivo} does not exist.")

class FileManager:
    """
    Clase para manejar las rutas de los archivos en el directorio base.

    Args:
        base_dir (str): Directorio base donde se encuentran los archivos. Por defecto es './weather_app/static/datalist'.
    """
    def __init__(self, base_dir='./weather_app/static/datalist'):
        self.base_dir = Path(base_dir)
    
    def get_path(self, file_name : str) -> Path:
        """
        Devuelve la ruta completa del archivo en el directorio base.

        Args:
            file_name (str): Nombre del archivo.

        Returns:
            Path: Ruta completa del archivo.
        """
        return self.base_dir / file_name

    def check_existence(self, file_name : str) -> Path:
        """
        Verifica si el archivo existe. Lanza una excepción si no existe.

        Args:
            file_name (str): Nombre del archivo.

        Raises:
            FileNotFound: Si el archivo no existe.

        Returns:
            Path: Ruta completa del archivo si existe.
        """
        file_path = self.get_path(file_name)
        if not file_path.exists():
            raise FileNotFound(file_path)
        return file_path

    def get_flight_path(self) -> Path:
        """
        Devuelve la ruta de 'vuelos.csv' y verifica su existencia.

        Returns:
            Path: Ruta completa del archivo 'vuelos.csv'.

        Raises:
            FileNotFound: Si el archivo 'vuelos.csv' no existe.
        """
        return self.check_existence('vuelos.csv')

    def get_destiny_path(self) -> Path:
        """
        Devuelve la ruta de 'destiny_data.csv' y verifica su existencia.

        Returns:
            Path: Ruta completa del archivo 'destiny_data.csv'.

        Raises:
            FileNotFound: Si el archivo 'destiny_data.csv' no existe.
        """
        return self.check_existence('destiny_data.csv')

    def get_location_path(self) -> Path:
        """
        Devuelve la ruta de 'datos_destinos_viajes.csv' y verifica su existencia.

        Returns:
            Path: Ruta completa del archivo 'datos_destinos_viajes.csv'.

        Raises:
            FileNotFound: Si el archivo 'datos_destinos_viajes.csv' no existe.
        """
        return self.check_existence('datos_destinos_viajes.csv')