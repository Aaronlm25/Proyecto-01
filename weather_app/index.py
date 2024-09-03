import autocorrect
import weather_manager as weather
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

    # Cargar los datos de vuelo desde el archivo CSV
    flight_data = weather.load_flight_data(flight_data_file_path)

    #Solicitud a la web se obtienen los datos enviados a través del formulario HTML
    if request.method == 'POST':
        city = request.form.get('city')
        iata_code = request.form.get('iata_code')
        flight_number = request.form.get('flight_number')
        
        #Por numero de vuelo
        if flight_number:
            weather_data=weather.seach_by_id(flight_number) 

        #Por ciudad
        elif city:
            weather_data= weather.seach_by_city(city)
        
        #Por IATA
        elif iata_code:
            weather_data=weather.seach_by_iata(iata_code)
        
        weather_cache.update(weather_data['city'])
    
    return render_template('index.html', weather_data=weather_data)

if __name__ == '__main__':
    weather_cache.start()
    app.run(debug=True)
    weather_cache.stop()

