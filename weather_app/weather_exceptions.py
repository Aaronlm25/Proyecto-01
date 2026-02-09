"""
Excepciones personalizadas para el manejo de clima.

Author: @pmoraf
Version: 1.0
"""
class CityNotFoundError(Exception):
    """
    Clase de excepción que se lanza cuando no se encuentra la ciudad especificada.
    """
    def __init__(self, message: str):
        """
        Args:
            message (str): Mensaje de error que describe la excepción.
        """
        super().__init__(message)

class IATANotFoundError(Exception):
    """
    Clase de excepción que se lanza cuando no se encuentra el código IATA especificado.
    """
    def __init__(self, message: str):
        """
        Args:
            message (str): Mensaje de error que describe la excepción.
        """
        super().__init__(message)

class FlightNotFoundError(Exception):
    """
    Clase de excepción que se lanza cuando no se encuentra la información del vuelo.
    """
    def __init__(self, message: str):
        """
        Args:
            message (str): Mensaje de error que describe la excepción.
        """
        super().__init__(message)

class WeatherRequestError(Exception):
    """
    Clase de excepción que se lanza cuando ocurre un error en la solicitud del clima.
    """
    def __init__(self, message: str):
        """
        Args:
            message (str): Mensaje de error que describe la excepción.
        """
        super().__init__(message)