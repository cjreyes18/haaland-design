import pyttsx3
from datetime import date, datetime
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Inicializar pyttsx3 y configurar la voz
robot_mouth = pyttsx3.init()
voices = robot_mouth.getProperty('voices')

# Buscar una voz en español y configurarla
for voice in voices:
    if "spanish" in voice.name.lower():
        robot_mouth.setProperty('voice', voice.id)
        break

robot_mouth.setProperty('rate', 150)  # Configura la velocidad de la voz

# API Key y URL de OpenWeatherMap
API_KEY = "d27ed3c0714d009ea32b06fe45abb034"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Credenciales de Spotify
SPOTIPY_CLIENT_ID = "f5a45f48ad56404084b1daf62559ae12"
SPOTIPY_CLIENT_SECRET = "327160c095b948e49c08c629ba21225f"
SPOTIPY_REDIRECT_URI = "http://localhost:8888/callback"  # Redirect URI que configuraste en Spotify

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI))

def get_weather(city):
    try:
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric',
            'lang': 'es'
        }
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        print(f"Respuesta de la API: {data}")  # Añadir esta línea para depuración

        if data["cod"] != 200:
            return f"No se pudo obtener la información del clima. Código de error: {data['cod']}, Mensaje: {data.get('message', 'No especificado')}"

        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        return (
            f"El clima en {city} es {weather_description}.\n"
            f"Temperatura: {temperature}°C, se siente como {feels_like}°C.\n"
            f"Humedad: {humidity}%.\n"
            f"Velocidad del viento: {wind_speed} m/s."
        )
    except Exception as e:
        return f"Ocurrió un error al obtener la información del clima: {e}"

def play_music(track_name):
    try:
        results = sp.search(q=track_name, limit=1)
        print(f"Resultados de la búsqueda: {results}")  # Añadir esta línea para depuración
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            track_name = track['name']
            track_url = track['external_urls']['spotify']
            return f"Puedes reproducir '{track_name}' en Spotify con este enlace: {track_url}"
        else:
            return "No se encontró ninguna canción con ese nombre."
    except Exception as e:
        return f"No se pudo encontrar la canción: {e}"

while True:
    # Solicitar la entrada del usuario por texto
    you = input("Escribe tu consulta: ")

    print("tú: " + you)

    robot_brain = ""

    if you == "":
        robot_brain = "No puedo oírte, por favor intenta nuevamente."
    elif "hola" in you.lower():
        robot_brain = "¡Hola! ¿Cómo puedo ayudarte hoy?"
    elif "hora" in you.lower():
        robot_brain = f"La hora actual es {datetime.now().strftime('%H:%M:%S')}."
    elif "fecha" in you.lower():
        robot_brain = f"La fecha de hoy es {date.today().strftime('%d de %B de %Y')}."
    elif "clima" in you.lower():
        city = input("¿En qué ciudad estás interesado en el clima?: ")
        robot_brain = get_weather(city)
    elif "música" in you.lower():
        track_name = input("¿Qué canción te gustaría escuchar?: ")
        robot_brain = play_music(track_name)
    else:
        robot_brain = "No estoy seguro de cómo responder a eso. Por favor, intenta nuevamente."

    # Para hablar la respuesta en español
    robot_mouth.say(robot_brain)
    robot_mouth.runAndWait()
