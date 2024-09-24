import weather_manager
import sys
import signal
from cache import Cache
from flask import Flask, render_template, request
from requests.exceptions import RequestException, HTTPError
from static.python.data_manager import DataCollector
from static.python.path_manager import FileManager, FileNotFound
from autocorrect import revise
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
        city = str(request.form.get('city', '')).strip()
        iata_code = str(request.form.get('iata_code', '')).strip()
        flight_number = str(request.form.get('flight_number', '')).strip()
        
        try:
            if city and not city.replace(" ", "").isalpha():
                error_message = 'El nombre de la ciudad debe contener solo letras.'
            elif iata_code and not iata_code.isalpha():
                error_message = 'El código IATA debe contener solo letras.'
            elif flight_number and not flight_number.replace(" ", "").isalnum():
                error_message = 'El número de vuelo debe contener solo letras y números, sin símbolos.'
            else:
                if flight_number:
                    flight_weather = weather_manager.search_by_id(flight_number, weather_cache.get_data())
                    departure_weather = flight_weather[0]
                    arrival_weather = flight_weather[1]
                elif city:
                    suggestions = revise(city)
                    if len(suggestions):
                        error_message = 'Asegurate de que has escrito bien el nombre.'
                    else:
                        similar = suggestions[0]
                        departure_weather = weather_manager.search_by_city(similar, weather_cache.get_data())
                elif iata_code:
                    departure_weather = weather_manager.search_by_iata(iata_code, weather_cache.get_data())
                if departure_weather:
                    weather_cache.update(departure_weather)
                if arrival_weather:
                    weather_cache.update(arrival_weather)

        except (ValueError, AttributeError, HTTPError):
            error_message = "Error al actualizar y/o datos, una disculpa."
        except RequestException:
            error_message = "No se encontraron los datos esperados, una disculpa."
        except TypeError:
            error_message = "No se pudo obtener los datos esperados, una disculpa."
    
    return render_template(
        'index.html',
        departure_weather=departure_weather,
        arrival_weather=arrival_weather,
        error=error_message,
        datalist_options=datalist_options,
        suggestion = suggestion,
        city = city
    )

if __name__ == '__main__':
    weather_cache = Cache('./weather_app/static/json/cache.json')
    weather_cache.start()
    safe_stop = lambda signal, frame: (weather_cache.stop(), sys.exit(0))
    signal.signal(signal.SIGINT, safe_stop)
    app.run()
    if weather_cache.is_active():
        weather_cache.stop()