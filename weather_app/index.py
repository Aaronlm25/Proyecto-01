import weather_manager
from cache import Cache
from flask import Flask, render_template, request

weather_cache = Cache('./weather_app/static/json/cache.json')
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def home():
    weather = None
    #Solicitud a la web se obtienen los datos enviados a través del formulario HTML
    if request.method == 'POST':
        city = request.form.get('city')
        iata_code = request.form.get('iata_code')
        flight_number = request.form.get('flight_number')
        if flight_number:
            weather = weather_manager.search_by_id(flight_number) 
        elif city:
            weather = weather_manager.search_by_city(city)
        elif iata_code:
            weather = weather_manager.search_by_iata(iata_code)
        try:
            weather_cache.update(weather.json_data)
        except AttributeError as e:
            print(f"Caught an AttributeError: {e}")
    return render_template('index.html', weather_data={'city' : weather.json_data, 'error' : ''} if weather else {})

if __name__ == '__main__':
    weather_cache.start()
    app.run(debug=True)
    weather_cache.stop()

