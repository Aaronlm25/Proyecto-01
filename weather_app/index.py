import autocorrect
import cache
import weather_manager as weather
import static.python.gather as gatherer
from threading import Thread
from flask import Flask, render_template, request

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def home():
    weather_data = {}
    if request.method == 'POST':
        city = request.form.get('city')
        iata_code = request.form.get('iata_code')
        flight_number = request.form.get('flight_number')
        if flight_number:
            flight_info = gatherer.get_flight_info(flight_number)
            if flight_info:
                departure_city = gatherer.get_city(flight_info['departure'])
                arrival_city = gatherer.get_city(flight_info['arrival'])
                departure_weather = weather.get_weather(departure_city) if departure_city else None
                arrival_weather = weather.get_weather(arrival_city) if arrival_city else None
                if departure_weather and arrival_weather:
                    weather_data['departure'] = departure_weather
                    weather_data['arrival'] = arrival_weather
                else:
                    weather_data['error'] = "No se pudo obtener el clima para una o ambas ciudades. Por favor, verifica el número de vuelo."
            else:
                weather_data['error'] = "Número de vuelo no válido."
        else:
            if city:
                weather_data['city'] = weather.get_weather(autocorrect.correct(city))
            elif iata_code:
                city = gatherer.get_city(iata_code)
                if city:
                    weather_data['city'] = weather.get_weather(city)
                else:
                    weather_data['error'] = "Código IATA no válido."
        cache.update('./weather-app/static/json/cache.json', weather_data['city'])
    return render_template('index.html', weather_data=weather_data)

if __name__ == '__main__':
    data = gatherer.get_destiny_data('./weather-app/static/datalist/datos_destinos.csv')
    # Actualiza constantemente las temperaturas de todos los destinos
    thread = Thread(target=weather.update_weather, args=[data])
    thread.start()
    app.run(debug=True)
    # Detiene al hilo que actualiza las temperaturas de los destinos
    weather.STOP_EVENT.set()
