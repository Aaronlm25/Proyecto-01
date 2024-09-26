import weather_manager
import sys
import signal
from cache import Cache
from flask import Flask, render_template, request
from requests.exceptions import RequestException, HTTPError
from static.python.data_manager import DataManager
from autocorrect import revise

DATA_MANAGER = DataManager()
DATA_COLLECTOR = DATA_MANAGER.get_data_collector()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    template = 'home.html'
    departure_weather = None
    arrival_weather = None
    error_message = None
    datalist_options = DATA_COLLECTOR.get_cities()
    city = ''
    suggestion= ''
    if request.method == 'POST':
        city = request.form.get('city')
        if city == None:
            city = ''
        iata_code = request.form.get('iata_code')
        flight_number = request.form.get('flight_number')
        option = request.form.get('option')
        try:
            if option == 'flight_number':
                template = 'flight.html'
            elif option in ['city']:
                template = 'city.html'
            if flight_number:
                flight_weather = weather_manager.search_by_id(flight_number, weather_cache.get_data())
                departure_weather = flight_weather[0]
                arrival_weather = flight_weather[1]
                template = 'flight.html'
            elif city:
                suggestions = revise(city)[0]
                if suggestion == []:
                    error_message = 'Asegúrate de que todas las palabras estén escritas correctamente.'
                elif suggestions.lower() == city.lower():
                    departure_weather = weather_manager.search_by_city(city, weather_cache.get_data())
                else:
                    suggestion = suggestions
                template = 'city.html'
            elif iata_code:
                iata_weather = weather_manager.search_by_iata(iata_code, weather_cache.get_data())
                departure_weather = iata_weather
                template = 'city.html'
            if departure_weather:
                weather_cache.update(departure_weather)
            if arrival_weather:
                weather_cache.update(arrival_weather)
        
        except (ValueError, AttributeError, HTTPError):
            error_message = "Error al actualizar datos, una disculpa."
        except RequestException:
            error_message = "No se encontraron los datos esperados, una disculpa."
        except TypeError:
            error_message = "No se pudo obtener los datos esperados, una disculpa."
            
    return render_template(
        template,
        departure_weather=departure_weather,
        arrival_weather=arrival_weather,
        error=error_message,
        datalist_options=datalist_options,
        suggestion=suggestion,
        city = city
    )

@app.route('/search', methods=['GET'])
def search():
    city = request.args.get('city')
    datalist_options = DATA_COLLECTOR.get_cities()
    departure_weather = weather_manager.search_by_city(city, weather_cache.get_data())
    return render_template(
        'city.html',
        city=city,
        departure_weather=departure_weather,
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