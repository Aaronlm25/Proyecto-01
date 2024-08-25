import requests
import csv
import autocorrect
import json
import cache
from flask import Flask, render_template, request

app = Flask(__name__)

KEY = 'a3117bc0d7c113aba1f25b2fb28748e1'

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

def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={KEY}&units=metric&lang=es"
        response = requests.get(url)
        response.raise_for_status()
        print(json.dumps(response.json(), indent=4))
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener datos: {e}")
        return None

# Recibe una lista de listas con 3 elementos los
# cuales son: ciudad, iata, aeropuerto
def get_city_from_iata(iata):
    for list in get_destiny_data('./weather-app/datalist/datos_destinos.csv'):
        if list[1] == iata:
            return list[0]
    return None

def get_flight_info(flight_number):
    flight_data = {
        'AA123': {'departure': 'JFK', 'arrival': 'LAX'},
        'DL456': {'departure': 'ORD', 'arrival': 'ATL'},
    }
    return flight_data.get(flight_number.upper(), None)

@app.route('/', methods=['GET', 'POST'])
def home():
    data = cache.get_data('./cache.json')
    weather_data = {}
    if request.method == 'POST':
        city = request.form.get('city')
        iata_code = request.form.get('iata_code')
        flight_number = request.form.get('flight_number')
        if flight_number:
            flight_info = get_flight_info(flight_number)
            if flight_info:
                departure_city = get_city_from_iata(flight_info['departure'])
                arrival_city = get_city_from_iata(flight_info['arrival'])
                departure_weather = get_weather(departure_city) if departure_city else None
                arrival_weather = get_weather(arrival_city) if arrival_city else None
                if departure_weather and arrival_weather:
                    weather_data['departure'] = departure_weather
                    weather_data['arrival'] = arrival_weather
                else:
                    weather_data['error'] = "No se pudo obtener el clima para una o ambas ciudades. Por favor, verifica el número de vuelo."
            else:
                weather_data['error'] = "Número de vuelo no válido."
        else:
            if city:
                weather_data['city'] = get_weather(autocorrect.correct(city))
            elif iata_code:
                city = get_city_from_iata(iata_code)
                if city:
                    weather_data['city'] = get_weather(city)
                else:
                    weather_data['error'] = "Código IATA no válido."
        cache.update('./cache.json', weather_data['city'])
    return render_template('index.html', weather_data=weather_data)

if __name__ == '__main__':
    app.run(debug=True)
