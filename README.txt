Requisitos
Python 3.x
pip para instalar dependencias de Python
requests para realizar solicitudes HTTP
Flask para el servidor web
autocorrect para sugerir correcciones en nombres de ciudades
python-Levenshtein para calcular la similitud entre cadenas

Instalación
Sige estos pasos para instalar y ejecutar la aplicación:

1. Clonar el Repositorio
Clone el repositorio de la aplicación desde el control de versiones, en este caso GitHub:
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_REPOSITORIO>

2. Crear un Entorno Virtual (opcional, pero recomendado)
Crear un entorno virtual ayuda a mantener las dependencias seguras.

python3 -m venv venv
Activar el entorno virtual:

En Ubuntu y Fedora: source venv/bin/activate

3. Instalar Dependencias
Instale las dependencias necesarias utilizando pip. Asegúrese de que el entorno virtual esté activado si lo está utilizando. En la carpeta debe de existir un archivo llamado requirements.txt En el se encuentra todas las dependencias necesarias para el uso de la pagina web.

Instale las dependencias con:

pip install -r requirements.txt

4.Configuración de Archivos
Asegúrese de que los archivos necesarios para el funcionamiento de la aplicación estén en los directorios correctos. Debe tener la siguiente estructura:

weather_app/
    weather_exceptions.py (contiene las excepciones usadas en weather_manager)
    weather_manager.py (archivo con la lógica del manejo del clima)
    index.html (plantilla HTML para la aplicación)
    cache.py (archivo con la clase Cache)
    autocorrect.py (archivo para el autocorrector de la pagina web)
    static/
        js/
            scripts.js (Contiene el script para usar el datalist)
            show_more.js (Contiene el scrpt para mostrar u ocultar contenido del HTML)
        json/
            cache.json (archivo vacío o con datos iniciales)
        datalist/
            destiny_data.csv (Contiene los nombres de ciudades y el IATA de su aeropuerto)
            vuelos.csv (Contiene los numeros de vuelo y el IATA del aeropuerto de salida y de llegada)
        python/
            data_manager.py (Recolecta los datos de los archivos en datalist con ayuda de path_manager.py)
            path_manager.py (Maneja las rutas de los archivos en datalist)
        style/
            styles.css (Contiene el diseño de las plantillas HTML)
            stars.png
        svg/
            (Iconos de clima)
        test/
            test_autocorrect.py
            test_cache.py
            temp/
                cache.json
    templates/
            index.html
            home.html
            iata.html
            flight.html
            city.html
    __pycache__/
            (genera archivos .pyc)

5. Obtener API Key.
Para poder obtener tu propia API Key sigue estos pasos:
	1.- Visita la pagina oficial de OpenWeather: https://openweathermap.org/
	2.- Selecciona la opción Sign in que se encuentra entre las opciones de la parte superior de la página.
	3.- Inicia sesión o crea una cuenta según sea el caso.
	4.- Una vez iniciaste sesión da clic en tu nombre de usuario que se encuentra en las opciones de la parte superior.
	5.- Lo anterior desplegará un menú contextual; selecciona la opción My API Keys.
	6.- Copia el texto que está debajo de la palabra: Key.
	7.- Listo, esa es tu API Key, no la pierdas pues la necesitarás en el siguiente paso.
    
6. Agregar API Key.
Para poder hacer uso del programa es necesario crear un archivo .env dentro de weather app a la par de index.py; dentro de este archivo deberás escribir textualmente la palabra: KEY=(aquí debes escribir tu API Key, omite los paréntesis), ejemplo:
KEY=11c1bc65947aef112141a221f2dd111

7. Ejecutar la Aplicación
Ejecute la pagina web con el siguiente comando:

python3 weather_app/index.py
La aplicación estará disponible en http://127.0.0.1:5000/ por defecto. Puede acceder a esta URL en su navegador para utilizar la aplicación.

8. Detener la Aplicación
Para detener la aplicación Flask, presione Ctrl+C en la terminal donde está ejecutando la aplicación.


