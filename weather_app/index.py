import weather_manager
import sys
import signal
from cache import Cache
from flask import Flask, render_template, request
from requests.exceptions import RequestException, HTTPError
from static.python.data_manager import DataCollector
from static.python.path_manager import FileManager, FileNotFound

FILE_MANAGER = FileManager()
try:
    DATA_MANAGER = DataCollector(FILE_MANAGER)
except FileNotFound as e:
    print(f"Error: {e}")
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    departure_weather = None
    arrival_weather = None
    error_message = None
    datalist_options = DATA_MANAGER.get_cities()
    if request.method == 'POST':
        city = request.form.get('city')
        iata_code = request.form.get('iata_code')
        flight_number = request.form.get('flight_number')
        try:
            if flight_number:
                flight_weather = weather_manager.search_by_id(flight_number, weather_cache.get_data())
                departure_weather = flight_weather[0]
                arrival_weather = flight_weather[1]
            elif city:
                city_weather = weather_manager.search_by_city(city, weather_cache.get_data())
                departure_weather = city_weather
            elif iata_code:
                iata_weather = weather_manager.search_by_iata(iata_code, weather_cache.get_data())
                departure_weather = iata_weather
            if departure_weather:
                weather_cache.update(departure_weather)
            if arrival_weather:
                weather_cache.update(arrival_weather)
        except ValueError as e:
            error_message = str(e)
        except RequestException as e:
            error_message = str(e)
        except AttributeError as e:
            print(f"Error al actualizar la caché: {e}")
        except HTTPError as e:
            print('No se encontró el URL')
        except TypeError as e:
            error_message = str(e)
    return render_template(
        'index.html',
        departure_weather=departure_weather,
        arrival_weather=arrival_weather,
        error=error_message,
        datalist_options=datalist_options
    )

if __name__ == '__main__':
    weather_cache = Cache('./weather_app/static/json/cache.json')
    weather_cache.start()
    safe_stop = lambda signal, frame: (weather_cache.stop(), sys.exit(0))
    signal.signal(signal.SIGINT, safe_stop)
    app.run()
    if weather_cache.is_active():
        weather_cache.stop()