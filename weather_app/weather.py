import json

class Weather:
    def __init__(self, json_data):
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
        

#Solo PARA DEPURAR (ELIMINAR PARA ENTREGA )
# Ejemplo de uso:
if __name__ == "__main__":
    # Simulación de un JSON obtenido de una API o archivo
    example_json = '''
    {
        "coord": {
            "lon": -69.1956,
            "lat": 9.5545
        },
        "weather": [
            {
                "id": 804,
                "main": "Clouds",
                "description": "nubes",
                "icon": "04d"
            }
        ],
        "base": "stations",
        "main": {
            "temp": 22.71,
            "feels_like": 23.6,
            "temp_min": 22.71,
            "temp_max": 22.71,
            "pressure": 1014,
            "humidity": 98,
            "sea_level": 1014,
            "grnd_level": 989
        },
        "visibility": 10000,
        "wind": {
            "speed": 1.7,
            "deg": 190,
            "gust": 3.7
        },
        "clouds": {
            "all": 100
        },
        "dt": 1724620125,
        "sys": {
            "country": "VE",
            "sunrise": 1724581701,
            "sunset": 1724626174
        },
        "timezone": -14400,
        "id": 3649833,
        "name": "Acarigua",
        "cod": 200
    }
    '''
    weather_data = Weather(json.loads(example_json))
    print(weather_data)
