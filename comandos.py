import os


def abrir_brave():
    os.startfile("brave.exe")

def procesar_comando(pregunta):

    pregunta = pregunta.lower()

    if "brave" in pregunta or "navegador" in pregunta:
        abrir_brave()
        return "Abriendo Brave..."

    return None