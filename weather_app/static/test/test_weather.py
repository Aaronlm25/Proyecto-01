import pytest
from weather import Weather

@pytest.fixture
def weather():
    json_data = {
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
    return Weather(json_data)

def test_initialization(weather):
    assert weather.latitude == 40.7128
    assert weather.longitude == -74.0060
    assert weather.weather_id == 800
    assert weather.main_weather == 'Clear'
    assert weather.description == 'clear sky'
    assert weather.icon == 'clear_icon.svg'
    assert weather.temp == 25.0
    assert weather.feels_like == 27.0
    assert weather.temp_min == 20.0
    assert weather.temp_max == 30.0
    assert weather.pressure == 1015
    assert weather.humidity == 60
    assert weather.visibility == 10000
    assert weather.wind_speed == 5.0
    assert weather.wind_deg == 270
    assert weather.wind_gust == 7.0
    assert weather.cloudiness == 0
    assert weather.country == 'US'
    assert weather.sunrise == 1633024800
    assert weather.sunset == 1633070400
    assert weather.name == 'New York'
    assert weather.timezone == -14400
    assert weather.id == 5128581
    assert weather.cod == 200

def test_determine_icon(weather):
    assert weather._determine_icon() == 'clear_icon.svg'

def test_str_method(weather):
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
    assert str(weather) == expected_str
