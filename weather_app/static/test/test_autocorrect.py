import pytest
import os
import sys
import csv
import random
from itertools import combinations
sys.path.append(os.path.abspath("./weather_app"))
from autocorrect import revise

@pytest.fixture
def city_data():
    """
    Fixture que regresa los nombres de las ciudades.

    Returns:
        data (set) : Coleccion con los nomrbes de las ciudades/
    """
    path = './weather_app/static/datalist/datos_destinos.csv'
    data = set()
    with open(path, 'r') as file:
        csv_file = csv.reader(file)
        next(csv_file)
        for row in csv_file:
            data.add(row[0])
    return data

def test_order(city_data : list):
    """
    Test para ver que el arreglo con las 5 ciudades mas similares
    tenga como primer elemento a la ciudad escrita correctamente.
    
    Args:
        city_data (list) : lista con los nombres de las ciudades. 
    """
    for city in city_data:
        similar_cities = revise(city, 0.7)
        assert city == similar_cities[0]

def test_upper_case(city_data : list):
    """
    Test para ver que dada una ciudad bien escrita esta se modifique de tal modo
    que todas sus letras sean mayusculas, y que el arreglo con las 5 ciudades mas similares
    tenga como primer elemento a la ciudad sin modificar.

    Args:
        city_data (list) : lista con los nombres de las ciudades.
    """
    for city in city_data:
        similar_cities = revise(city.upper(), 0.9)
        assert similar_cities[0] == city 

def test_lower_case(city_data : list):
    """
    Test para ver que dada una ciudad bien escrita esta se modifique de tal modo
    que todas sus letras sean minusculas, y que el arreglo con las 5 ciudades mas similares
    tenga como primer elemento a la ciudad sin modificar.

    Args:
        city_data (list) : lista con los nombres de las ciudades.
    """
    for city in city_data:
        similar_cities = revise(city.lower(), 0.9)
        assert similar_cities[0] == city 

def test_mixed_upper_lower_case(city_data : list):
    """
    Test para ver que dada una ciudad bien escrita esta se modifique de tal modo
    que sus letras sean mayusculas y minusculas en un orden aleatorio, y que el arreglo
    con las 5 ciudades mas similares tenga como primer elemento a la ciudad sin modificar.

    Args:
        city_data (list) : lista con los nombres de las ciudades.
    """
    for city in city_data:
        mixed = ''.join(
            char.lower() if random.choice([True, False]) else char.upper()
            for char in city
        )
        similar_cities = revise(mixed, 0.7)
        assert similar_cities[0] == city 

def test_accuracy_basic(city_data : list):
    """
    Test para ver que dada una ciudad bien escrita esta se modifique de tal modo
    que se consideren dos cadenas una con un letra extra y otra con una letra faltante
    , y que el arreglo con las 5 ciudades mas similares tenga como primer elemento a la ciudad
    sin modificar en ambos casos, ademas se consideran algunas valores que no deberian de tener
    ninguna ciuadad similar.

    Args:
        city_data (list) : lista con los nombres de las ciudades.
    """
    for city in city_data:
        i = random.randint(1, len(city) - 2)
        missing_letter = city[0:i] + '' + city[i + 1:]   
        extra_letter = city[0:i] + '' + city[i:]
        distorted = [missing_letter, extra_letter]
        for distorted_city in distorted:
            similar = revise(distorted_city, 0.7)
            assert any(city in similar for city in city_data)
    special_characters = {'~', ':', "'", '+', '[', '\\', '@', '^', '{'}
    arbitrary_sets = []
    arbitrary_sets.extend(combinations(special_characters, 5))
    for character_set in arbitrary_sets:
        arbitrary_string = ''.join(map(str, character_set))
        assert revise(arbitrary_string, 0.7) == []
    assert revise('chine', 0.7) == []
    assert revise('afsdb', 0.5) == []
    assert revise('', 0.5) == []