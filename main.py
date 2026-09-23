from google import genai
from dotenv import load_dotenv
from comandos import procesar_comando
import os

# Cargar las variables del archivo .env
load_dotenv()

# Obtener la API Key
api_key = os.getenv("GEMINI_API_KEY")

# Crear conexión con Gemini
client = genai.Client(api_key=api_key)

print("==============================")
print("          NOVA 🤖")
print("==============================")
print("Escribe 'salir' para terminar.\n")

while True:

    pregunta = input("Tú: ")

    if pregunta.lower() == "salir":
        print("Nova: Hasta luego 👋")
        break

    if pregunta.lower() == "abre brave":
        abrir_brave()
        print("Nova: Abriendo Brave...")
        continue
    respuesta = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=pregunta
    )

    print("Nova:", respuesta.text)
    print()
    #asta aqui por hoy