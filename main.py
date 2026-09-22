from google import genai
from dotenv import load_dotenv
import os

# Cargar las variables del archivo .env
load_dotenv()

# Obtener la API Key
api_key = os.getenv("GEMINI_API_KEY")

# Crear conexión con Gemini
client = genai.Client(api_key=api_key)

# Enviar una pregunta
respuesta = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="Hola, me llamo Nova. Preséntate brevemente."
)

# Mostrar la respuesta
print(respuesta.text)