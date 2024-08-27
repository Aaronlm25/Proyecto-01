import json

class Weather:
    def __init__(self, json_data):
        self.json_data = json_data
        
        # Coordenadas
        self.lat = self.json_data['coord']['lat']
        self.lon = self.json_data['coord']['lon']
        
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
    
    #getters
    #cords
    def get_lat(self):
        return self.lat
    
    def get_lon(self):
        return self.lon
    
    #clima
    def get_weather_id(self):
        return self.weather_id
    
    def get_main_weather(self):
        return self.main_weather
    
    def get_description(self):
        return self.description
    
    def get_icon(self):
        return self.icon
    
    #stats
    def get_temp(self):
        return self.temp
    
    def get_feels_like(self):
        return self.feels_like
    
    def get_temp_max(self):
        return self.temp_max
    
    def get_temp_min(self):
        return self.temp_min
    
    def get_pressure(self):
        return self.pressure
    
    def get_humidity(self):
        return self.humidity
    
    #visibilidad
    def get_visibility(self):
        return self.visibility
    
    #viento
    def get_wind_speed(self):
        return self.wind_speed
    
    def get_wind_deg(self):
        return self.wind_deg
    
    def get_wind_gust(self):
        return self.icon
        
    #nubes
    def get_cloudiness(self):
        return self.cloudiness
    
    #pais
    def get_country(self):
        return self.country
    
    def get_sunrise(self):
        return self.sunrise
    
    def get_sunset(self):
        return self.sunset
    
    def get_name(self):
        return self.name
    
    def get_timezone(self):
        return self.timezone
    
    def get_id(self):
        return self.id
    
    def get_cod(self):
        return self.cod
    
    
    def __str__(self):
        return (f"Weather in {self.name} ({self.country}):\n"
                f"Coordinates: lat {self.lat}, lon {self.lon}\n"
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
