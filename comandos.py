import subprocess
from aplicaciones import APLICACIONES


def abrir_aplicacion(nombre):
    programa = APLICACIONES.get(nombre)

    if programa:
        subprocess.Popen(
            [programa],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )

        return f"Abriendo {nombre}..."


    return None


def procesar_comando(pregunta):

    pregunta = pregunta.lower()

    for nombre in APLICACIONES:

        if f"abre {nombre}" in pregunta or f"abrir {nombre}" in pregunta:
            return abrir_aplicacion(nombre)

    return None