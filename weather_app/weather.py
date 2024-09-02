import json

class Weather:
    """
        Representa la información meteorológica para una ubicación específica.

        Attributes:
            json_data (dict): Datos meteorológicos en formato JSON.
            latitude (float): Latitud de la ubicación.
            longitude (float): Longitud de la ubicación.
            weather_id (int): ID del clima.
            main_weather (str): Descripción principal del clima.
            description (str): Descripción detallada del clima.
            icon (str): Nombre del archivo del icono asociado con el clima.
            temp (float): Temperatura actual en grados Celsius.
            feels_like (float): Sensación térmica en grados Celsius.
            temp_min (float): Temperatura mínima en grados Celsius.
            temp_max (float): Temperatura máxima en grados Celsius.
            pressure (int): Presión atmosférica en hPa.
            humidity (int): Humedad relativa en porcentaje.
            visibility (int or None): Visibilidad en metros, o None si no está disponible.
            wind_speed (float): Velocidad del viento en m/s.
            wind_deg (int): Dirección del viento en grados.
            wind_gust (float or None): Ráfagas del viento en m/s, o None si no está disponible.
            cloudiness (int): Porcentaje de nubosidad.
            country (str): Código del país.
            sunrise (int): Hora del amanecer en formato de timestamp.
            sunset (int): Hora del atardecer en formato de timestamp.
            name (str): Nombre de la ciudad.
            timezone (int or None): Desfase horario en segundos desde GMT, o None si no está disponible.
            id (int or None): ID de la ciudad, o None si no está disponible.
            cod (int or None): Código de respuesta del API, o None si no está disponible.
        """
        
    def __init__(self, json_data):
        """
        Inicializa la instancia de la clase Weather con datos meteorológicos.

        Args:
            json_data (dict): Datos meteorológicos en formato JSON.
        """
    
        self.json_data = json_data
        
        # Coordenadas
        self.latitude = self.json_data['coord']['lat']
        self.longitude = self.json_data['coord']['lon']
        
        # Información del clima
        self.weather_id = self.json_data['weather'][0]['id']
        self.main_weather = self.json_data['weather'][0]['main']
        self.description = self.json_data['weather'][0]['description']
        self.icon = self._determine_icon()
        
        # Información principal
        self.temp = self.json_data['main']['temp']
        self.feels_like = self.json_data['main']['feels_like']
        self.temp_min = self.json_data['main']['temp_min']
        self.temp_max = self.json_data['main']['temp_max']
        self.pressure = self.json_data['main']['pressure']
        self.humidity = self.json_data['main']['humidity']
        
        # Visibilidad
        self.visibility = self.json_data.get('visibility', None)
        
        # Información del viento
        self.wind_speed = self.json_data['wind']['speed']
        self.wind_deg = self.json_data['wind']['deg']
        self.wind_gust = self.json_data['wind'].get('gust', None)
        
        # Información de las nubes
        self.cloudiness = self.json_data['clouds']['all']
        
        # Información del sistema (país, amanecer, atardecer)
        self.country = self.json_data['sys']['country']
        self.sunrise = self.json_data['sys']['sunrise']
        self.sunset = self.json_data['sys']['sunset']
        
        # Información general
        self.name = self.json_data['name']
        self.timezone = self.json_data.get('timezone', None)
        self.id = self.json_data.get('id', None)
        self.cod = self.json_data.get('cod', None)

    def _determine_icon(self):
        """
        Determina el icono basado en el ID del clima.

        Utiliza un diccionario que mapea los IDs de clima a los nombres de archivo de iconos correspondientes.
        
        Returns:
            str: Nombre del archivo del icono asociado con el clima.
        """
        icon_map = {
            range(200, 233): "storm_icon.svg",         # Tormenta
            range(300, 322): "light_rain_icon.svg",    # Lluvia ligera
            range(500, 505): "rain_icon.svg",          # Lluvia
            511: "snow_icon.svg",                      # Nieve
            range(520, 532): "rain_icon.svg",          # Lluvia
            range(600, 623): "snow_icon.svg",          # Nieve
            range(701, 782): "fog_icon.svg",           # Neblina
            800: "clear_icon.svg",                     # Despejado
            801: "partly_cloudy_icon.svg",             # Algunas nubes
            802: "clouds_icon.svg",                    # Nubes
            range(803, 805): "cloudy_icon.svg"         # Nublado
        }

        for key, icon in icon_map.items():
            if isinstance(key, range) and self.weather_id in key:
                return icon
            elif self.weather_id == key:
                return icon

        return "default_icon.svg"  # Por si no se encuentra un icono correspondiente
    
    def __str__(self):
        """
        Devuelve una representación en cadena de la instancia de la clase Weather.

        Returns:
            str: Información completa del clima en formato legible.
        """
        return (f"Weather in {self.name} ({self.country}):\n"
                f"Coordinates: lat {self.latitude}, lon {self.longitude}\n"
                f"Weather ID: {self.weather_id}, Main: {self.main_weather}, Description: {self.description}\n"
                f"Weather icon: {self.icon}\n"
                f"Temperature: {self.temp}°C (Feels like: {self.feels_like}°C)\n"
                f"Min Temp: {self.temp_min}°C, Max Temp: {self.temp_max}°C\n"
                f"Pressure: {self.pressure} hPa, Humidity: {self.humidity}%\n"
                f"Visibility: {self.visibility} m\n"
                f"Wind: {self.wind_speed} m/s, Direction: {self.wind_deg}°, Gusts: {self.wind_gust} m/s\n"
                f"Cloudiness: {self.cloudiness}%\n"
                f"Sunrise: {self.sunrise}, Sunset: {self.sunset}\n"
                f"Timezone: {self.timezone}, City ID: {self.id}, Response Code: {self.cod}")
        