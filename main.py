
from google import genai
from dotenv import load_dotenv
from comandos import procesar_comando
from voz import escuchar
import os


# Cargar variables del archivo .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


print("==============================")
print("          NOVA 🤖")
print("==============================")
print("Di 'salir' para terminar.\n")


while True:

    # Escuchar lo que dice el usuario
    pregunta = escuchar()

    # Si no entendió lo que dijimos, volver a escuchar
    if not pregunta:
        continue

    # Comando para salir
    if pregunta.lower() == "salir":
        print("Nova: Hasta luego 👋")
        break

    # Revisar si es un comando de la computadora
    respuesta_comando = procesar_comando(pregunta)

    if respuesta_comando:
        print("Nova:", respuesta_comando)
        continue

    # Si no es un comando, preguntarle a Gemini
    respuesta = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=pregunta
    )

    print("Nova:", respuesta.text)

