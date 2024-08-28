import os
import sys 
sys.path.append(os.path.abspath("./weather_app"))
import pytest
import random
import json
import cache

dir = './temp/cache.json'

def test_get_data_empty_file():
    data = cache.get_data(dir)
    assert data == {}

def test_update_empty_file():
    size = random.randint(1, 10)
    remove_cache()
    data = example_data(size)
    for json_object in data:
            cache.update(json_object)
    written_data = cache.get_data(dir)
    assert len(written_data) == size


def remove_cache():
    if os.path.exists(dir):
         os.remove(dir)

def example_data(size):
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
    data = []
    for x in range(size):
       data.append(json.loads(example_json))
    return data
    
    