import csv
import autocorrect
import cache
from threading import Thread
import weather_manager as weather
from flask import Flask, render_template, request

# Obtiene los datos de los destinos, de un archivo
# .csv, el cual contiene por cada destino 3 datos:
# ciudad, iata, aeropuerto
def get_destiny_data(route):
    destiny_data = []
    with open(route, mode='r') as file:
        reader = csv.reader(file)
        data = list(reader)
    for row in data:
        destiny_data.append(row)
    return destiny_data

data = get_destiny_data('./weather-app/datalist/datos_destinos.csv')

# Recibe una lista de listas con 3 elementos los
# cuales son: ciudad, iata, aeropuerto
def get_city(iata):
    for list in data:
        if list[1] == iata:
            return list[0]
    return None

def get_flight_info(flight_number):
    flight_data = {
        'AA123': {'departure': 'JFK', 'arrival': 'LAX'},
        'DL456': {'departure': 'ORD', 'arrival': 'ATL'},
    }
    return flight_data.get(flight_number.upper(), None)

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def home():
    weather_data = {}
    if request.method == 'POST':
        city = request.form.get('city')
        iata_code = request.form.get('iata_code')
        flight_number = request.form.get('flight_number')
        if flight_number:
            flight_info = get_flight_info(flight_number)
            if flight_info:
                departure_city = get_city(flight_info['departure'])
                arrival_city = get_city(flight_info['arrival'])
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
                city = get_city(iata_code)
                if city:
                    weather_data['city'] = weather.get_weather(city)
                else:
                    weather_data['error'] = "Código IATA no válido."
        cache.update('./cache.json', weather_data['city'])
    return render_template('index.html', weather_data=weather_data)

if __name__ == '__main__':
    # Actualiza constantemente las temperaturas de todos los destinos
    thread = Thread(target=weather.update_weather, args=[data])
    thread.start()
    app.run(debug=True)
    weather.STOP_FLAG = False
