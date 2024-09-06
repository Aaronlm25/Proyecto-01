import weather_manager
from cache import Cache
from flask import Flask, render_template, request

weather_cache = Cache('./weather_app/static/json/cache.json')
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def home():
    weather_results = []
    error_message = None
    if request.method == 'POST':
        city = request.form.get('city')
        iata_code = request.form.get('iata_code')
        flight_number = request.form.get('flight_number')
        try:
            if flight_number:
                flight_weather = weather_manager.search_by_id(flight_number, weather_cache.get_data())
                weather_results.append(flight_weather[0])
                weather_results.append(flight_weather[1])
            elif city:
                city_weather = weather_manager.search_by_city(city, weather_cache.get_data())
                weather_results.append(city_weather)
            elif iata_code:
                iata_weather = weather_manager.search_by_iata(iata_code, weather_cache.get_data())
                weather_results.append(iata_weather)
        except ValueError as e:
            print(e)
        try:
            for weather in weather_results:
                weather_cache.update(weather)
        except AttributeError as e:
            print(f"Error al actualizar la caché: {str(e)}")
    return render_template('index.html', weather_data=weather_results[0] if weather_results else {}, error=error_message)

if __name__ == '__main__':
    weather_cache.start()
    app.run(debug=True)
    weather_cache.stop()

