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
dir = './weather_app/static/test/temp/'

@pytest.fixture
def sample_cache():
    """
    Fixture para obtener un objeto cache.
    
    Returns:
        (Cache) : Un objeto cache.
    """
    return Cache(path)

@pytest.fixture
def clean():
    """
    Fixture para quitar todos los archivos del directorio temp.
    """
    for file in os.listdir(dir):
        file_path = os.path.join(dir, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

def json_file() -> json:
    """
    Permite obtener la lista de objetos json del archivo en el path especificado.

    Returns:
        json_file (json) : los datos del archivo.json.
    """
    json_file = []
    with open(path, 'r') as file:
        if os.path.getsize(path) != 0:
            json_file = json.load(file)
    return json_file

def to_json(weather_records : dict) -> json:
    """
    Permite obtener una lista de objetos json dado un diccionario cuyos valores son
    objetos json.

    Returns:
        json (json) : lista de objetos json.
    """
    json = []
    for value in weather_records.values():
        json.append(value)
    return json

def sample_data_adjoint(size : int) -> list:
    """
    Permite obtener un ejemplo de una lista de objetos json con duplicados
    dado un tamano.
    Los objetos json solo tienen una variable 'name' con un valor x que va de
    0 a size - 1.

    Args:
        size (int) : el tamano de la lista

    Returns:
        data (list) : lista de objetos json
    """
    data = []
    for x in range(size):
       data.append({"name": x})
       data.append({"name": x})
    return data

def sample_data_disjoint(size : int) -> list:
    """
    Permite obtener un ejemplo de una lista de objetos json sin duplicados
    dado un tamano.
    Los objetos json solo tienen una variable 'name' con un valor x que va de
    0 a size - 1.

    Args:
        size (int) : el tamano de la lista

    Returns:
        data (list) : lista de objetos json
    """
    data = []
    for x in range(size):
       data.append({"name": x})
    return data

@pytest.mark.dependency()
def test_stop(clean, sample_cache : Cache):
    """
    Test para ver que el hilo de ejecucion del cache se detine correctamente.

    Args:
        clean : borra todos los archivos en el directorio temp
        sample_cache (Cache)
    """
    sample_cache.start()
    time.sleep(2)
    sample_cache.stop()
    assert threading.active_count() == 1

@pytest.mark.dependency(depends=["test_stop"])
def test_start(clean, sample_cache : Cache):
    """
    Test (depende del test_stop) para ver que el hilo de ejecucion se crea
    correctamente.
    
    Args:
        clean : borra todos los archivos en el directorio temp
        sample_cache (Cache)
    """
    sample_cache.start()
    assert sample_cache.is_active()
    assert threading.active_count() == 2
    sample_cache.start()
    assert sample_cache.is_active()
    assert threading.active_count() == 2
    names = [thread.name for thread in threading.enumerate()]
    assert 'cache' in names
    sample_cache.stop()
    assert json_file() == to_json(sample_cache.weather_records)

def test_invalid_cache(clean):
    """
    Test para ver que se lanza la excepcion apropiada
    para un archivo cache con extension invalida.

    Args:
        clean : borra todos los archivos en el directorio temp
    """
    with pytest.raises(InvalidCacheFileException):
        invalid_cache = Cache('./weather_app/static/test/temp/cache')
    with pytest.raises(InvalidCacheFileException):
        invalid_cache = Cache('./weather_app/static/test/temp/cache.xd')

def test_get_data_empty_file(clean, sample_cache : Cache):
    """
    Test para ver que no se esta escribiendo nada extra.

    Args:
        clean : borra todos los archivos en el directorio temp
        sample_cache (Cache)
    """
    sample_cache.stop()
    assert sample_cache.weather_records == {}
    assert json_file() == [] 

def test_update_empty_file(clean, sample_cache : Cache):
    """
    Test para ver que un archivo json vacio se llena correctamente aun con
    datos repetidos.
        
    Args:
        clean : borra todos los archivos en el directorio temp
        sample_cache (Cache)
    """
    size = random.randint(1, 10)
    data_types = (sample_data_adjoint(size) , sample_data_disjoint(size))
    for data in data_types:
        for json_object in data:
            sample_cache.update(json_object)
        written_data = sample_cache.weather_records
        assert len(written_data) == size
    sample_cache.stop()
    assert json_file() == to_json(sample_cache.weather_records)

def test_update_large(clean, sample_cache : Cache):
    """
    Test para ver que un archivo json vacio se llena correctamente aun con
    datos repetidos y en gran cantidad.
        
    Args:
        clean : borra todos los archivos en el directorio temp
        sample_cache (Cache)
    """
    size = random.randint(100, 1000)
    data_types = (sample_data_adjoint(size) , sample_data_disjoint(size))
    for data in data_types:
        for json_object in data:
            sample_cache.update(json_object)
        written_data = sample_cache.weather_records
        assert len(written_data) == size
    sample_cache.stop()
    assert json_file() == to_json(sample_cache.weather_records)

def test_directory_creation(clean, sample_cache : Cache):
    """   
    Test para ver que un objeto json crea su archivo en el directorio especificado.
        
    Args:
        clean : borra todos los archivos en el directorio temp
        sample_cache (Cache)
    """
    assert os.path.exists(path)

def test_get_data_reading(clean):
    """
    Test para ver que los datos se leen correctamente desde el archivo json.

    Args:
        clean : borra todos los archivos en el directorio temp
        sample_cache (Cache)
    """
    sample_data = [
        {"name": "x", "temp": 20, "humidity": 50},
        {"name": "y", "temp": 25, "humidity": 60}
    ]
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(sample_data, file, indent=4, ensure_ascii=False)
    sample_cache = Cache(path)
    weather_records = sample_cache.weather_records
    assert len(weather_records) == 2
    assert weather_records["x"]["temp"] == 20
    assert weather_records["x"]["humidity"] == 50
    assert weather_records["y"]["temp"] == 25
    assert weather_records["y"]["humidity"] == 60