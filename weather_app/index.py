import weather_manager
from cache import Cache
from flask import Flask, render_template, request

weather_cache = Cache('./weather_app/static/json/cache.json')
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def home():
    weather_records = []
    error_message = None

    if request.method == 'POST':
        city = request.form.get('city')
        iata_code = request.form.get('iata_code')
        flight_number = request.form.get('flight_number')

        if flight_number:
            try:
                flight_weather = weather_manager.search_by_id(flight_number, weather_cache)
                if flight_weather[0] and flight_weather[1]:
                    weather_records.append(flight_weather[0])
                    weather_records.append(flight_weather[1])
                else:
                    error_message = "No se encontró información para el número de vuelo proporcionado."
            except Exception as e:
                error_message = f"Error al buscar el vuelo: {str(e)}"
        elif city:
            try:
                city_weather = weather_manager.search_by_city(city, weather_cache)
                if city_weather:
                    weather_records.append(city_weather)
                else:
                    error_message = "No se encontró información para la ciudad proporcionada."
            except Exception as e:
                error_message = f"Error al buscar la ciudad: {str(e)}"
        elif iata_code:
            try:
                iata_weather = weather_manager.search_by_iata(iata_code, weather_cache)
                if iata_weather:
                    weather_records.append(iata_weather)
                else:
                    error_message = "No se encontró información para el código IATA proporcionado."
            except Exception as e:
                error_message = f"Error al buscar el código IATA: {str(e)}"

        try:
            for weather in weather_records:
                weather_cache.update(weather)
        except AttributeError as e:
            error_message = f"Error al actualizar la caché: {str(e)}"

    return render_template('index.html', weather_data=weather_records[0] if weather_records else {}, error=error_message)

if __name__ == '__main__':
    weather_cache.start()
    app.run(debug=True)
    weather_cache.stop()

