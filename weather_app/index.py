import autocorrect
import weather_manager as weather
import static.python.gather as gatherer
from weather import Weather
from cache import Cache
from flask import Flask, render_template, request

weather_cache = Cache('./weather_app/static/json/cache.json')
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def home():
    weather_data = {}

    # Definir las rutas de los archivos
    flight_data_file_path = './weather_app/static/datalist/datos_destinos_viajes.csv'
    tickets_txt_file_path = './weather_app/static/tickets/tickets.txt'

    # Cargar los datos de vuelo desde el archivo CSV
    flight_data = weather.load_flight_data(flight_data_file_path)
    # Guardar los datos de vuelo en el archivo TXT
    weather.save_flight_data_to_txt(flight_data, tickets_txt_file_path)

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
        elif city:
            weather_data['city'] = weather.get_weather(autocorrect.correct(city))
        elif iata_code:
            city = gatherer.get_city(iata_code)
            if city:
                weather_data['city'] = weather.get_weather(city)
            else:
                weather_data['error'] = "Código IATA no válido."
        weather_cache.update(weather_data['city'])
    
    return render_template('index.html', weather_data=weather_data)

if __name__ == '__main__':
    weather_cache.start()
    app.run(debug=True)
    weather_cache.stop()

