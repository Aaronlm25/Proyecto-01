import weather_manager
import sys
import signal
from cache import Cache
from flask import Flask, render_template, request
from requests.exceptions import RequestException, HTTPError
from static.python.data_manager import DataManager
from autocorrect import revise

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    template = 'home.html'
    departure_weather = None
    arrival_weather = None
    error_message = None
    datalist_options = data_collector.get_cities()
    city = ''
    suggestion= ''
    if request.method == 'POST':
        city = str(request.form.get('city', '')).strip()
        iata_code = str(request.form.get('iata_code', '')).strip()
        flight_number = str(request.form.get('flight_number', '')).strip()
        option = request.form.get('option')
        try:
            if option == 'flight_number':
                template = 'flight.html'
            elif option == 'city':
                template = 'city.html'
            elif option == 'iata_code':
                template = 'iata.html'
            if flight_number:
                flight_weather = weather_manager.search_by_id(flight_number, weather_cache.get_data())
                departure_weather = flight_weather[0]
                arrival_weather = flight_weather[1]
                template = 'flight.html'
            elif city:
                suggestions = revise(city, data_collector.get_cities())
                if suggestions[0].lower() == city.lower():
                    departure_weather = weather_manager.search_by_city(city, weather_cache.get_data())
                else:
                    suggestion = suggestions[0]
                template = 'city.html'
            elif iata_code:
                iata_upper = iata_code.upper()
                departure_weather = weather_manager.search_by_iata(iata_upper, weather_cache.get_data())
                template = 'iata.html'
            if departure_weather:
                weather_cache.update(departure_weather)
            if arrival_weather:
                weather_cache.update(arrival_weather)
        except (ValueError, AttributeError, IndexError):
            error_message = 'Asegúrate de que todas las palabras estén escritas correctamente.'
        except (RequestException, HTTPError):
            error_message = 'No se encontraron los datos esperados, una disculpa.'
        except TypeError:
            error_message = 'No se pudo obtener los datos esperados, una disculpa.'
    return render_template(
        template,
        departure_weather=departure_weather,
        arrival_weather=arrival_weather,
        error=error_message,
        datalist_options=datalist_options,
        suggestion=suggestion,
        city=city
    )

@app.route('/correct', methods=['GET'])
def correct():
    city = request.args.get('city')
    departure_weather = weather_manager.search_by_city(city, weather_cache.get_data())
    return render_template('city.html', departure_weather=departure_weather)

if __name__ == '__main__':
    data_collector = DataManager().get_data_collector()
    weather_cache = Cache('./weather_app/static/json/cache.json', data_collector.get_cities())
    weather_cache.start()
    safe_stop = lambda signal, frame: (weather_cache.stop(), sys.exit(0))
    signal.signal(signal.SIGINT, safe_stop)
    app.run()
    if weather_cache.is_active():
        weather_cache.stop()