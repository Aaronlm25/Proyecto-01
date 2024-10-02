class CityNotFoundError(Exception):
    """
    Clase de excepción que se lanza cuando no se encuentra la ciudad especificada.

    Args:
        message (str): Mensaje de error que describe la excepción.
    """
    def __init__(self, message: str):
        super().__init__(message)

class IATANotFoundError(Exception):
    """
    Clase de excepción que se lanza cuando no se encuentra el código IATA especificado.

    Args:
        message (str): Mensaje de error que describe la excepción.
    """
    def __init__(self, message: str):
        super().__init__(message)

class FlightNotFoundError(Exception):
    """
    Clase de excepción que se lanza cuando no se encuentra la información del vuelo.

    Args:
        message (str): Mensaje de error que describe la excepción.
    """
    def __init__(self, message: str):
        super().__init__(message)

class WeatherRequestError(Exception):
    """
    Clase de excepción que se lanza cuando ocurre un error en la solicitud del clima.

    Args:
        message (str): Mensaje de error que describe la excepción.
    """
    def __init__(self, message: str):
        super().__init__(message)