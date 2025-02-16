# Análisis de Precios de Propiedades Comerciales cerca de Paradas de Autobús

Este proyecto desarrolla un backend en Python que analiza y calcula el precio promedio de propiedades comerciales ubicadas cerca de paradas de autobús en Valladolid, España.

## 🎯 Descripción

El sistema procesa datos de ubicaciones de paradas de autobús utilizando la API de Google Maps y los combina con información de propiedades comerciales para generar análisis de precios por proximidad.

## ⚙️ Requisitos del Sistema

-   Python 3.10 o superior
-   Conexión a Internet (para API de Google Maps)
-   Archivo de datos `idealista_data.csv`

### Dependencias Principales

-   `googlemaps`: Para interactuar con la API de Google Maps
-   `python-dotenv`: Para gestión de variables de entorno
-   `pandas`: Para procesamiento de datos CSV

## 🚀 Instalación

1. Clona el repositorio:

```bash
git clone [URL_DEL_REPOSITORIO]
cd [NOMBRE_DEL_DIRECTORIO]
```

2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

3. Configura las variables de entorno:
    - Crea un archivo `.env` en la raíz del proyecto
    - Añade tu API key de Google Maps:
        ```
        GOOGLE_MAPS_API_KEY=tu_api_key_aquí
        ```

## 📁 Estructura del Proyecto

```
project_root/
├── main.py              # Script principal
├── idealista_data.csv   # Datos de propiedades
├── .env                 # Variables de entorno
└── README.md           # Documentación
```

## 💻 Uso

1. Asegúrate de tener el archivo `idealista_data.csv` en el directorio del proyecto
2. Ejecuta el script principal:

```bash
python main.py
```

## 📊 Formato de Datos

### Entrada (idealista_data.csv)

El archivo CSV de entrada debe contener los siguientes campos:

-   floor: Planta del inmueble
-   price: Precio en euros
-   size: Tamaño en metros cuadrados
-   exterior: Booleano (True/False)
-   rooms: Número de habitaciones
-   bathrooms: Número de baños
-   latitude: Latitud
-   longitude: Longitud
-   showAddress: Booleano (True/False)
-   url: URL del inmueble
-   distance: Distancia en metros
-   priceByArea: Precio por metro cuadrado

### Salida

Se generará un archivo CSV con:

-   Ubicación de la parada de autobús
-   Precios promedio por rangos de distancia

## 🔒 Seguridad

-   No compartas tu archivo `.env` ni expongas las API keys
-   Mantén actualizada la versión de Python y las dependencias

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, asegúrate de:

1. Hacer fork del repositorio
2. Crear una rama para tu feature
3. Seguir las convenciones de código existentes
4. Documentar los cambios
5. Enviar un Pull Request

## 📝 Notas Adicionales

-   Este proyecto está en su primera versión y utiliza datos pre-existentes en CSV
-   Futuras versiones podrían incluir integración directa con la API de Idealista
-   Se recomienda consultar la documentación completa en `instructions.md`
