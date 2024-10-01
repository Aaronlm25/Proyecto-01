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
    weather_manager.py (archivo con la lógica del manejo del clima)
    index.html (plantilla HTML para la aplicación)
    cache.py (archivo con la clase Cache)
    autocorrect.py (archivo para el autocorrector de la pagina web)
    static/
        js/
            script.js 
        json/
            cache.json (archivo vacío o con datos iniciales)
        datalist/
            vuelos.csv (archivo CSV con datos de vuelos)
            datos_destinos.csv (archivo CSV con datos de destinos)
            ciudades.csv (archivo CSV con datos de ciudades)
            datos_destinos_viajes.csv ( archivo csv con datos de origen y llegada de viajes)
        python/
            gather.py
            __pycache__/
                    (archivos .pyc)
        style/
            styles.css
        svg/
            (Iconos de clima)
        test/
            test_autocorrect.py
            test_cache.py
            temp/
                cache.json
    templates/
            index.html
            svg/
                (Iconos de clima)
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


