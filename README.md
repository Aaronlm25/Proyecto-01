# 🌤️ Aplicación de Clima

Aplicación web que permite consultar el clima de una **ciudad**, un **código IATA**
de aeropuerto o un **número de vuelo**, usando la API de OpenWeather. Construida
con Flask, incluye autocorrección de búsquedas, autocompletado y almacenamiento
en caché para reducir llamadas a la API.

> Proyecto académico. Enfocado en el consumo de APIs externas y el procesamiento
> y presentación de los datos recibidos.

## ✨ Características

- Consulta del clima por **ciudad**, **código IATA** o **número de vuelo**.
- **Autocorrector** de búsquedas (distancia de Levenshtein) para tolerar errores de escritura.
- **Autocompletado** con listas de ciudades, aeropuertos y vuelos.
- **Caché en JSON**: guarda resultados recientes para no repetir llamadas a la API.
- Interfaz web con vistas separadas por tipo de búsqueda.

## 🛠️ Tecnologías

- Python 3 · Flask
- `requests` — solicitudes HTTP a la API
- `python-Levenshtein` — similitud entre cadenas (autocorrector)
- API de [OpenWeather](https://openweathermap.org/)

## 🚀 Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/Aaronlm25/app-clima.git
cd app-clima

# 2. Crear y activar un entorno virtual (recomendado)
python3 -m venv venv
source venv/bin/activate        # Linux

# 3. Instalar dependencias
pip install -r requirements.txt
```

## 🔑 Configurar la API Key

La aplicación necesita una API Key gratuita de OpenWeather:

1. Crea una cuenta en [openweathermap.org](https://openweathermap.org/).
2. Entra a tu perfil → **My API Keys** y copia tu clave.
3. Crea un archivo `.env` dentro de `weather_app/` (junto a `index.py`) con:

```
KEY=tu_api_key_aqui
```

> El archivo `.env` no se sube al repositorio (contiene tu clave personal).

## 💻 Uso

```bash
python3 weather_app/index.py
```

La aplicación quedará disponible en `http://127.0.0.1:5000/`.
Para detenerla, presiona `Ctrl + C` en la terminal.

## 📁 Estructura del proyecto

```
weather_app/
├── index.py              # Punto de entrada (servidor Flask)
├── weather_manager.py    # Lógica del manejo del clima
├── weather_exceptions.py # Excepciones propias
├── cache.py              # Manejo de caché
├── autocorrect.py        # Autocorrector de búsquedas
├── static/
│   ├── js/               # Scripts (datalist, mostrar/ocultar contenido)
│   ├── json/             # cache.json
│   ├── datalist/         # CSV de ciudades, aeropuertos y vuelos
│   ├── python/           # Gestión de datos y rutas
│   ├── style/            # CSS e imágenes
│   └── svg/              # Iconos de clima
└── templates/            # Vistas HTML (home, city, iata, flight)
```
