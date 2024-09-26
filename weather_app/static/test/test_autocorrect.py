import pytest
import os
import sys
import csv
import random
from itertools import combinations
sys.path.append(os.path.abspath("./weather_app"))
from autocorrect import revise

@pytest.fixture(scope='session')
def city_data() -> list:
    """
    Fixture que regresa los nombres de las ciudades.

    Returns:
        data (list) : Coleccion con los nomrbes de las ciudades.
    """
    path = './weather_app/static/datalist/destiny_data.csv'
    data = []
    with open(path, 'r') as file:
        csv_file = csv.reader(file)
        next(csv_file)
        for row in csv_file:
            data.append(row[0])
    return data

def test_order(city_data : list):
    """
    Test para ver que el arreglo con las 5 ciudades mas similares
    tenga como primer elemento a la ciudad escrita correctamente.
    
    Args:
        city_data (list): lista con los nombres de las ciudades. 
    """
    for city in city_data:
        similar_cities = revise(city, city_data)
        assert city == similar_cities[0]

def test_upper_case(city_data : list):
    """
    Test para ver que dada una ciudad bien escrita esta se modifique de tal modo
    que todas sus letras sean mayusculas, y que el arreglo con las 5 ciudades mas similares
    tenga como primer elemento a la ciudad sin modificar.

    Args:
        city_data (list): lista con los nombres de las ciudades.
    """
    for city in city_data:
        similar_cities = revise(city.upper(), city_data)
        assert similar_cities[0] == city 

def test_lower_case(city_data : list):
    """
    Test para ver que dada una ciudad bien escrita esta se modifique de tal modo
    que todas sus letras sean minusculas, y que el arreglo con las 5 ciudades mas similares
    tenga como primer elemento a la ciudad sin modificar.

    Args:
        city_data (list): lista con los nombres de las ciudades.
    """
    for city in city_data:
        similar_cities = revise(city.lower(), city_data)
        assert similar_cities[0] == city 

def test_mixed_upper_lower_case(city_data : list):
    """
    Test para ver que dada una ciudad bien escrita esta se modifique de tal modo
    que sus letras sean mayusculas y minusculas en un orden aleatorio, y que el arreglo
    con las 5 ciudades mas similares tenga como primer elemento a la ciudad sin modificar.

    Args:
        city_data (list): lista con los nombres de las ciudades.
    """
    for city in city_data:
        mixed = ''.join(
            char.lower() if random.choice([True, False]) else char.upper()
            for char in city
        )
        similar_cities = revise(mixed, city_data)
        assert similar_cities[0] == city 

def test_accuracy_basic(city_data : list):
    """
    Test para ver que dada una ciudad bien escrita esta se modifique de tal modo
    que se consideren dos cadenas una con un letra extra y otra con una letra faltante
    , y que el arreglo con las 5 ciudades mas similares tenga como primer elemento a la ciudad
    sin modificar en ambos casos, ademas se consideran algunas valores que no deberian de tener
    ninguna ciuadad similar.

    Args:
        city_data (list): lista con los nombres de las ciudades.
    """
    for city in city_data:
        i = random.randint(1, len(city) - 2)
        missing_letter = city[0:i] + '' + city[i + 1:]   
        extra_letter = city[0:i] + '' + city[i:]
        distorted = [missing_letter, extra_letter]
        for distorted_city in distorted:
            similar = revise(distorted_city, city_data)
            assert city in similar
    special_characters = {'~', ':', "'", '+', '[', '\\', '@', '^', '{'}
    arbitrary_sets = []
    arbitrary_sets.extend(combinations(special_characters, 5))
    for character_set in arbitrary_sets:
        arbitrary_string = ''.join(map(str, character_set))
        assert revise(arbitrary_string, city_data) == []
    assert revise('', city_data) == []