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

    # Cargar los datos de vuelo desde el archivo CSV
    flight_data = weather.load_flight_data(flight_data_file_path)

    #Solicitud a la web se obtienen los datos enviados a través del formulario HTML
    if request.method == 'POST':
        city = request.form.get('city')
        iata_code = request.form.get('iata_code')
        flight_number = request.form.get('flight_number')
        #Por numero de vuelo
        if flight_number:
            flight_info = gatherer.buscar_vuelo(flight_number)
            if isinstance(flight_info, dict):  # Asegúrate de que es un diccionario
                departure = flight_info['departure']
                arrival = flight_info['arrival']               
            else:
                weather_data['error']= flight_info  # Mensaje de error si no se encontró el vuelo
            
            #Busca si la llegada o la salida es la ubicacion distinta de mexico
            if departure == "MEX":
                city=gatherer.get_city(departure)
            else:
                city=gatherer.get_city(arrival)
            
            weather_data['city']=weather.get_weather(city)
               
        #Por ciudad
        elif city:
            weather_data['city'] = weather.get_weather(city)
        #Por IATA
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

