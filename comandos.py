import os
from aplicaciones import APLICACIONES


def abrir_aplicacion(nombre):
    programa = APLICACIONES.get(nombre)

    if programa:
        os.startfile(programa)
        return f"Abriendo {nombre}..."

    return None


def procesar_comando(pregunta):

    pregunta = pregunta.lower()

    # Buscar aplicación para abrir
    for nombre in APLICACIONES:

        if f"abre {nombre}" in pregunta or f"abrir {nombre}" in pregunta:
            return abrir_aplicacion(nombre)

    return None