"""
Inicializa la página, renderiza los templates correspondientes a los 
que solicita el usuario y permite que la información necesaria 
este disponible para los templates.
"""

import sys
import signal
from flask import Flask, render_template, request

import weather_manager
from cache import Cache
from static.python.data_manager import DataManager
from static.python.path_manager import FileManager
from autocorrect import revise
from weather_exceptions import (
    CityNotFoundError,
    WeatherRequestError
)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    template = 'home.html'
    departure_weather = None
    error_message = None

    datalist_options = data_collector.get_cities()
    city = ''
    suggestion = ''
    suggestions = []

    option = get_option()

    try:
        if option == 'SEARCH_BY_CITY':
            city = str(request.form.get('city', '')).strip()
            template = 'city.html'
            if city:
                suggestions = revise(city, datalist_options)
                departure_weather = weather_manager.search_by_city(
                    city, weather_cache.get_data()
                )

    except CityNotFoundError:
        if suggestions:
            suggestion = suggestions[0]
        else:
            error_message = 'Asegúrate de escribir correctamente la ciudad.'

    except WeatherRequestError:
        error_message = 'No se pudieron obtener los datos del clima.'

    except ValueError:
        error_message = 'Ocurrió un error inesperado.'

    return render_template(
        template,
        departure_weather=departure_weather,
        error=error_message,
        datalist_options=datalist_options,
        suggestion=suggestion,
        city=city
    )


def get_option():
    option = request.form.get('option')

    if option == 'city' or 'city' in request.form:
        return 'SEARCH_BY_CITY'


    return 'UNKNOWN_OPTION'


@app.route('/correct', methods=['GET'])
def correct():
    city = request.args.get('city')
    departure_weather = weather_manager.search_by_city(
        city, weather_cache.get_data()
    )

    return render_template(
        'city.html',
        city=city,
        datalist_options=data_collector.get_cities(),
    )


if __name__ == '__main__':
    data_collector = DataManager().get_data_collector()
    weather_cache = Cache(
        './weather_app/static/json/cache.json',
        data_collector.get_cities()
    )

    weather_cache.start()

    def safe_stop(signal, frame):
        weather_cache.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, safe_stop)
    app.run(debug=True)
