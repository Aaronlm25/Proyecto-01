class Weather:
    def __init__(self, temperature: float, weather_id: int):
        self.temperature = temperature
        self.weather_id = weather_id
        self.icon = self._determine_icon()

    def _determine_icon(self):
        """
        Determina el icono basado en el ID del clima.
        """
        if 200 <= self.weather_id <= 232:
            return "storm_icon.svg"  # Tormenta
        elif 300 <= self.weather_id <= 321:
            return "light_rain_icon.svg"  # Lluvia ligera
        elif 500 <= self.weather_id <= 504:
            return "rain_icon.svg"  # Lluvia
        elif self.weather_id == 511:
            return "snow_icon.svg"  # Nieve
        elif 520 <= self.weather_id <= 531:
            return "rain_icon.svg"  # Lluvia
        elif 600 <= self.weather_id <= 622:
            return "snow_icon.svg"  # Nieve
        elif 701 <= self.weather_id <= 781:
            return "fog_icon.svg"  # Neblina
        elif self.weather_id == 800:
            return "clear_icon.svg"  # Despejado
        elif self.weather_id == 801:
            return "partly_cloudy_icon.svg"  # Algunas nubes
        elif self.weather_id == 802:
            return "clouds_icon.svg"  # Nubes
        elif 803 <= self.weather_id <= 804:
            return "cloudy_icon.svg"  # Nublado
        else:
            return "default_icon.svg"  # Icono por defecto si el ID no se encuentra en los rangos especificados

    def __str__(self):
        return f"Weather ID: {self.weather_id}, Temperature: {self.temperature}°C, Icon: {self.icon}"
