import unittest
from weather import Weather

class TestWeather(unittest.TestCase):

    def setUp(self):
        # Datos de ejemplo para pruebas
        self.json_data = {
            'coord': {'lat': 40.7128, 'lon': -74.0060},
            'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky'}],
            'main': {'temp': 25.0, 'feels_like': 27.0, 'temp_min': 20.0, 'temp_max': 30.0, 'pressure': 1015, 'humidity': 60},
            'visibility': 10000,
            'wind': {'speed': 5.0, 'deg': 270, 'gust': 7.0},
            'clouds': {'all': 0},
            'sys': {'country': 'US', 'sunrise': 1633024800, 'sunset': 1633070400},
            'name': 'New York',
            'timezone': -14400,
            'id': 5128581,
            'cod': 200
        }
        self.weather = Weather(self.json_data)

    def test_initialization(self):
        self.assertEqual(self.weather.latitude, 40.7128)
        self.assertEqual(self.weather.longitude, -74.0060)
        self.assertEqual(self.weather.weather_id, 800)
        self.assertEqual(self.weather.main_weather, 'Clear')
        self.assertEqual(self.weather.description, 'clear sky')
        self.assertEqual(self.weather.icon, 'clear_icon.svg')
        self.assertEqual(self.weather.temp, 25.0)
        self.assertEqual(self.weather.feels_like, 27.0)
        self.assertEqual(self.weather.temp_min, 20.0)
        self.assertEqual(self.weather.temp_max, 30.0)
        self.assertEqual(self.weather.pressure, 1015)
        self.assertEqual(self.weather.humidity, 60)
        self.assertEqual(self.weather.visibility, 10000)
        self.assertEqual(self.weather.wind_speed, 5.0)
        self.assertEqual(self.weather.wind_deg, 270)
        self.assertEqual(self.weather.wind_gust, 7.0)
        self.assertEqual(self.weather.cloudiness, 0)
        self.assertEqual(self.weather.country, 'US')
        self.assertEqual(self.weather.sunrise, 1633024800)
        self.assertEqual(self.weather.sunset, 1633070400)
        self.assertEqual(self.weather.name, 'New York')
        self.assertEqual(self.weather.timezone, -14400)
        self.assertEqual(self.weather.id, 5128581)
        self.assertEqual(self.weather.cod, 200)

    def test_determine_icon(self):
        self.assertEqual(self.weather._determine_icon(), 'clear_icon.svg')

    def test_str_method(self):
        expected_str = ("Weather in New York (US):\n"
                        "Coordinates: lat 40.7128, lon -74.006\n"
                        "Weather ID: 800, Main: Clear, Description: clear sky\n"
                        "Weather icon: clear_icon.svg\n"
                        "Temperature: 25.0°C (Feels like: 27.0°C)\n"
                        "Min Temp: 20.0°C, Max Temp: 30.0°C\n"
                        "Pressure: 1015 hPa, Humidity: 60%\n"
                        "Visibility: 10000 m\n"
                        "Wind: 5.0 m/s, Direction: 270°, Gusts: 7.0 m/s\n"
                        "Cloudiness: 0%\n"
                        "Sunrise: 1633024800, Sunset: 1633070400\n"
                        "Timezone: -14400, City ID: 5128581, Response Code: 200")
        self.assertEqual(str(self.weather), expected_str)

if __name__ == '__main__':
    unittest.main()
