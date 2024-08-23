import pdfplumber
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

KEY = 'a3117bc0d7c113aba1f25b2fb28748e1'

def load_iata_data(pdf_path):
    iata_to_city = {}
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:  # Itera sobre cada página del PDF
                table = page.extract_table()
                if table:
                    for row in table[1:]:  # Salta la fila de encabezados
                        city_name = row[0].strip()
                        iata_code = row[1].strip().upper()
                        airport_name = row[2].strip()  # Puedes usarlo si lo necesitas
                        iata_to_city[iata_code] = city_name
    except Exception as e:
        print(f"Error al leer el PDF: {e}")
    
    return iata_to_city

iata_to_city = load_iata_data('datalist/datos_ciudad.pdf')

def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={KEY}&units=metric&lang=es"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener datos: {e}")
        return None

def get_city_from_iata(iata):
    return iata_to_city.get(iata.upper(), None)

def get_flight_info(flight_number):
    flight_data = {
        'AA123': {'departure': 'JFK', 'arrival': 'LAX'},
        'DL456': {'departure': 'ORD', 'arrival': 'ATL'},
    }
    return flight_data.get(flight_number.upper(), None)

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
                weather_data['city'] = get_weather(city)
            elif iata_code:
                city = get_city_from_iata(iata_code)
                if city:
                    weather_data['city'] = get_weather(city)
                else:
                    weather_data['error'] = "Código IATA no válido."

    print("Weather Data:", weather_data)
    
    return render_template('index.html', weather_data=weather_data)

if __name__ == '__main__':
    app.run(debug=True)
