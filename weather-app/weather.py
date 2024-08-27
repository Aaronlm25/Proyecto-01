import json

class WeatherData:
    def __init__(self, json_data):
        self.json_data = json_data
        self.coord = self.json_data['coord']
        self.weather = self.json_data['weather'][0]  # Asume que siempre hay al menos un elemento en la lista
        self.main = self.json_data['main']
        self.wind = self.json_data['wind']
        self.clouds = self.json_data['clouds']
        self.sys = self.json_data['sys']
        self.name = self.json_data['name']
        self.visibility = self.json_data.get('visibility', None)
        self.timezone = self.json_data.get('timezone', None)
        self.id = self.json_data.get('id', None)
        self.cod = self.json_data.get('cod', None)

    def get_weather_id(self):
        return self.weather['id']

    def get_temperature(self):
        return self.main['temp']

    def get_weather_description(self):
        return self.weather['description']

    def __str__(self):
        return (f"Weather in {self.name}:\n"
                f"Temperature: {self.get_temperature()}°C\n"
                f"Description: {self.get_weather_description()}\n"
                f"Weather ID: {self.get_weather_id()}\n"
                f"Coordinates: {self.coord}\n"
                f"Wind: {self.wind}\n"
                f"Clouds: {self.clouds['all']}%\n"
                f"Sunrise: {self.sys['sunrise']}\n"
                f"Sunset: {self.sys['sunset']}\n")

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
    weather_data = WeatherData(json.loads(example_json))
    print(weather_data)