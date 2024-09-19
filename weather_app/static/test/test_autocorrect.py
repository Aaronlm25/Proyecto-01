import pytest
import os
import sys
import random
import csv
sys.path.append(os.path.abspath("./weather_app"))
from autocorrect import revise

@pytest.fixture
def city_data():
    path = './weather_app/static/datalist/cities_2.csv'
    data = set()
    with open(path, 'r') as file:
        csv_file = csv.reader(file)
        next(csv_file)
        for row in csv_file:
            for word in row:
                data.add(word)
    return random.sample(sorted(data), 5)

def test_order(city_data):
    i = random.randint(0, 4)
    city = city_data[i]
    similar_cities = revise(city, 0.7)
    assert city == similar_cities[0]
            
def test_upper_case(city_data):
    for city in city_data:
        similar_cities = revise(city.upper(), 0.7)
        assert similar_cities[0] == city 

def test_lower_case(city_data):
    for city in city_data:
        similar_cities = revise(city.lower(), 0.7)
        assert similar_cities[0] == city 

def test_mixed_upper_lower_case(city_data):
    for city in city_data:
        mixed = ''
        for char in city:
            mixed += random.choice([char.lower(), char.upper()])
        similar_cities = revise(mixed, 0.7)
        assert similar_cities[0] == city 

def test_acurracy_basic(city_data):
    distorted = []
    for i in range(100):
        for city in city_data:
            i = random.randint(1,len(city) - 2)
            missing_letter = city[0:i] + '' + city[i + 1:]   
            extra_letter = city[0:i] + '' + city[i:]
            distorted.append(random.choice([missing_letter, extra_letter]))
        for x in range(5):
            similar = revise(distorted[x], 0.7)
            assert city_data[x] in similar
        distorted = []
    assert revise('chine', 0.9) == []
    assert revise('afsdb', 0.7) == []
    assert revise('', .9) == []
    
    
