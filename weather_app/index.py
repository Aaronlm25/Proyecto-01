import weather_manager
from cache import Cache
from flask import Flask, render_template, request

weather_cache = Cache('./weather_app/static/json/cache.json')
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def home():
    weather_records = []
    #Solicitud a la web se obtienen los datos enviados a través del formulario HTML
    if request.method == 'POST':
        city = request.form.get('city')
        iata_code = request.form.get('iata_code')
        flight_number = request.form.get('flight_number')
        if flight_number:
            flight_weather = weather_manager.search_by_id(flight_number, weather_cache) 
            weather_records.append(flight_weather[0])
            weather_records.append(flight_weather[1])
        elif city:
            weather_records.append(weather_manager.search_by_city(city, weather_cache))
        elif iata_code:
            weather_records.append(weather_manager.search_by_iata(iata_code, weather_cache))
        try:
            for weather in weather_records:
                weather_cache.update(weather)
        except AttributeError as e:
            print(f"Caught an AttributeError: {e}")
    # todavia no se manejan los climas de vuelo por lo siempre se considera solo un clima
    return render_template('index.html', weather_data=weather_records[0] if len(weather_records) != 0 else {})

if __name__ == '__main__':
    weather_cache.start()
    app.run(debug=True)
    weather_cache.stop()

