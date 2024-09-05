# README para la Aplicación de Clima

Esta aplicación permite consultar el clima de una ciudad, un código IATA o un número de vuelo utilizando una API de clima. La aplicación está construida con Flask y maneja el almacenamiento en caché de los datos del clima en un archivo JSON.

![climas](https://github.com/user-attachments/assets/fe2e13a0-985d-4f88-be52-64b1e39ae19f)

## Requisitos

- Python 3.x
- `pip` para instalar dependencias de Python
- `requests` para realizar solicitudes HTTP
- `Flask` para el servidor web
- `autocorrect` para sugerir correcciones en nombres de ciudades
- `python-Levenshtein` para calcular la similitud entre cadenas

## Instalación

Sige estos pasos para instalar y ejecutar la aplicación:

### 1. Clonar el Repositorio

Clone el repositorio de la aplicación desde el control de versiones, en este caso GitHub:

```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_REPOSITORIO>
```

### 2. Crear un Entorno Virtual (opcional, pero recomendado)


Crear un entorno virtual ayuda a mantener las dependencias seguras.
```bash
python3 -m venv venv
```

Activar el entorno virtual:

En Ubuntu y Fedora:
    ```bash
    source venv/bin/activate
    ```

### 3. Instalar Dependencias

Instale las dependencias necesarias utilizando pip. Asegúrese de que el entorno virtual esté activado si lo está utilizando.
En la carpeta debe de existir un archivo llamado requirements.txt
En el se encuentra todas las dependencias necesarias para el uso de la pagina web.

Instale las dependencias con:
```bash
pip install -r requirements.txt
```

### 4.Configuración de Archivos

Asegúrese de que los archivos necesarios para el funcionamiento de la aplicación estén en los directorios correctos.
Debe tener la siguiente estructura:
```bash
weather_app/

    static/
        json/
            cache.json (archivo vacío o con datos iniciales)
        datalist/
            vuelos.csv (archivo CSV con datos de vuelos)
            datos_destinos.csv (archivo CSV con datos de destinos)
            ciudades.csv (archivo CSV con datos de ciudades)
    templates/
        index.html (plantilla HTML para la aplicación)
    app.py (archivo con el código de la aplicación Flask)
    weather_manager.py (archivo con la lógica del manejo del clima)
    cache.py (archivo con la clase Cache)
```
###  5. Ejecutar la Aplicación

Ejecute la pagina web con el siguiente comando:

```bash
python3 weather_app/index.py
```

La aplicación estará disponible en http://127.0.0.1:5000/ por defecto.
Puede acceder a esta URL en su navegador para utilizar la aplicación.

### 6. Detener la Aplicación

Para detener la aplicación Flask, presione Ctrl+C en la terminal donde está ejecutando la aplicación.





cd <NOMBRE_DEL_REPOSITORIO>
