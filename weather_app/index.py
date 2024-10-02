import weather_manager
import sys
import signal
from cache import Cache
from flask import Flask, render_template, request
from static.python.data_manager import DataManager
from autocorrect import revise
from weather_exceptions import (CityNotFoundError, 
                                IATANotFoundError, 
                                FlightNotFoundError, 
                                WeatherRequestError)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    template = 'home.html'
    departure_weather = None
    arrival_weather = None
    error_message = None
    datalist_options = data_collector.get_cities()
    city = ''
    suggestion = ''
    suggestions = []
    if request.method == 'POST':
        city = None
        iata_code = None
        flight_number = None
        option = get_option()
        try:
            if option == 'SEARCH_BY_FLIGHT':
                flight_number = str(request.form.get('flight_number', '')).strip()
                template = 'flight.html'
                if flight_number:
                    flight_weather = weather_manager.search_by_id(flight_number, weather_cache.get_data())
                    departure_weather = flight_weather[0]
                    arrival_weather = flight_weather[1]
            elif option == 'SEARCH_BY_CITY':
                city = str(request.form.get('city', '')).strip()
                template = 'city.html'
                if city:
                    suggestions = revise(city, data_collector.get_cities())
                    departure_weather = weather_manager.search_by_city(city, weather_cache.get_data())
            elif option == 'SEARCH_BY_IATA':
                iata_code = str(request.form.get('iata_code', '')).strip().upper()
                template = 'iata.html'
                if iata_code:
                    departure_weather = weather_manager.search_by_iata(iata_code, weather_cache.get_data())
            if departure_weather:
                weather_cache.update(departure_weather)
            if arrival_weather:
                weather_cache.update(arrival_weather)
        except CityNotFoundError:
            if len(suggestions) == 0:
                error_message = 'Asegurate que has escrito la ciudad correctamente.'
            else:
                suggestion = suggestions[0]
        except IATANotFoundError:
            error_message = 'No se encontró el código IATA especificado.'
        except FlightNotFoundError:
            error_message = 'No se encontraron los datos esperados, una disculpa.'
        except WeatherRequestError:
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

def get_option():
    option = request.form.get('option')
    if option == 'flight_number' or 'flight_number' in request.form:
        return 'SEARCH_BY_FLIGHT'
    elif option == 'city' or 'city' in request.form:
        return 'SEARCH_BY_CITY'
    elif option == 'iata_code' or 'iata_code' in request.form:
        return 'SEARCH_BY_IATA'
    return 'UNKNOWN_OPTION'

@app.route('/correct', methods=['GET'])
def correct():
    city = request.args.get('city')
    departure_weather = weather_manager.search_by_city(city, weather_cache.get_data())
    return render_template('city.html', city=city ,departure_weather=departure_weather)

if __name__ == '__main__':
    data_collector = DataManager().get_data_collector()
    weather_cache = Cache('./weather_app/static/json/cache.json', data_collector.get_cities())
    weather_cache.start()
    safe_stop = lambda signal, frame: (weather_cache.stop(), sys.exit(0))
    signal.signal(signal.SIGINT, safe_stop)
    app.run()
    if weather_cache.is_active():
        weather_cache.stop()