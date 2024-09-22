import os
import sys 
import json
import pytest
import random
import threading
import time
sys.path.append(os.path.abspath("./weather_app"))
from cache import Cache, InvalidCacheFileException

path = './weather_app/static/test/temp/cache.json'

@pytest.fixture
def sample_cache():
    return Cache(path)

@pytest.fixture
def clean():
    if os.path.exists(path):
         os.remove(path)

def json_file():
    json_file = []
    with open(path, 'r') as file:
        if os.path.getsize(path) != 0:
            json_file = json.load(file)
    return json_file

def to_json(weather_records):
    json_file = []
    for value in weather_records.values():
        json_file.append(value)
    return json_file

def sample_data_adjoint(size):
    data = []
    for x in range(size):
       data.append({"name": x})
       data.append({"name": x})
    return data

def sample_data_disjoint(size):
    data = []
    for x in range(size):
       data.append({"name": x})
    return data

@pytest.mark.dependency()
def test_stop(clean, sample_cache):
    sample_cache.start()
    time.sleep(3)
    sample_cache.stop()
    assert threading.active_count() == 1

@pytest.mark.dependency(depends=["test_stop"])
def test_start(clean, sample_cache):
    sample_cache.start()
    assert sample_cache.is_active()
    assert threading.active_count() == 2
    sample_cache.start()
    assert sample_cache.is_active()
    assert threading.active_count() == 2
    names = [thread.name for thread in threading.enumerate()]
    assert 'cache' in names
    sample_cache.stop()

def test_invalid_cache(clean):
    with pytest.raises(InvalidCacheFileException):
        invalid_cache = Cache('./weather_app/static/test/temp/cachegads')
    with pytest.raises(InvalidCacheFileException):
        invalid_cache = Cache('./weather_app/static/test/temp/cache.xd')
    clean
    os.mkdir('./weather_app/static/test/temp')
    with open(path, 'x') as invalid_cache_file:
        invalid_cache_file.write(
            
        )
def test_get_data_empty_file(clean, sample_cache):
    sample_cache.stop()
    assert sample_cache.weather_records == {}
    assert json_file() == [] 

def test_update_empty_file(clean, sample_cache):
    size = random.randint(1, 10)
    data_types = (sample_data_adjoint(size) , sample_data_disjoint(size))
    for data in data_types:
        for json_object in data:
            sample_cache.update(json_object)
        written_data = sample_cache.weather_records
        assert len(written_data) == size
    sample_cache.stop()
    assert json_file() == to_json(sample_cache.weather_records)

def test_update_large(clean, sample_cache):
    size = random.randint(100, 1000)
    data_types = (sample_data_adjoint(size) , sample_data_disjoint(size))
    for data in data_types:
        for json_object in data:
            sample_cache.update(json_object)
        written_data = sample_cache.weather_records
        assert len(written_data) == size
    sample_cache.stop()
    assert json_file() == to_json(sample_cache.weather_records)

def test_directory_creation(clean, sample_cache):
    assert os.path.exists(path)