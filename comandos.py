import subprocess
import shutil
from pathlib import Path

from aplicaciones import APLICACIONES


def buscar_aplicacion(programa):
    # 1. Buscar en las variables PATH de Windows
    ruta = shutil.which(programa)

    if ruta:
        return ruta

    # 2. Buscar en carpetas comunes de instalación
    carpetas = [
        Path(r"C:\Program Files"),
        Path(r"C:\Program Files (x86)"),
        Path.home() / "AppData" / "Local"
    ]

    for carpeta in carpetas:

        if not carpeta.exists():
            continue

        try:
            for archivo in carpeta.rglob(programa):

                if archivo.is_file():
                    return str(archivo)

        except PermissionError:
            continue

    return None


def abrir_aplicacion(nombre):

    programa = APLICACIONES.get(nombre)

    if not programa:
        return f"No tengo registrada la aplicación {nombre}."

    ruta = buscar_aplicacion(programa)

    if ruta:
        try:
            subprocess.Popen(
                [ruta],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )

            return f"Abriendo {nombre}..."

        except Exception as e:
            return f"No pude abrir {nombre}. Error: {e}"

    return f"No encontré el archivo de {nombre}."


def cerrar_aplicacion(nombre):

    programa = APLICACIONES.get(nombre)

    if not programa:
        return f"No tengo registrada la aplicación {nombre}."

    procesos_cierre = {
        "calculadora": "CalculatorApp.exe"
    }

    proceso = procesos_cierre.get(nombre, programa)

    try:
        resultado = subprocess.run(
            ["taskkill", "/IM", proceso, "/F"],
            capture_output=True,
            text=True
        )

        if resultado.returncode == 0:
            return f"Cerrando {nombre}..."

        return f"La aplicación {nombre} no está abierta."

    except Exception as e:
        return f"No pude cerrar {nombre}. Error: {e}"


def procesar_comando(pregunta):

    pregunta = pregunta.lower().strip()

    # Revisar aplicaciones que ya conocemos para abrir
    for nombre in APLICACIONES:

        if (
            f"abre {nombre}" in pregunta
            or f"abrir {nombre}" in pregunta
            or f"abre la {nombre}" in pregunta
            or f"abrir la {nombre}" in pregunta
            or f"puedes abrir {nombre}" in pregunta
            or f"puedes abrir el {nombre}" in pregunta
        ):
            return abrir_aplicacion(nombre)

    # Revisar aplicaciones que ya conocemos para cerrar
    for nombre in APLICACIONES:

        if (
            f"cierra {nombre}" in pregunta
            or f"cerrar {nombre}" in pregunta
            or f"puedes cerrar {nombre}" in pregunta
            or f"puedes cerrar el {nombre}" in pregunta
            or f"quiero cerrar {nombre}" in pregunta
        ):
            return cerrar_aplicacion(nombre)

    # Detectar una aplicación que no está en el diccionario para abrir
    frases_abrir = [
        "abre ",
        "abrir ",
        "abre la ",
        "abrir la ",
        "puedes abrir ",
        "quiero abrir "
    ]

    for frase in frases_abrir:

        if pregunta.startswith(frase):

            nombre = pregunta[len(frase):].strip()

            if nombre:
                programa = nombre + ".exe"

                ruta = buscar_aplicacion(programa)

                if ruta:
                    try:
                        subprocess.Popen(
                            [ruta],
                            stdin=subprocess.DEVNULL,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
                        )

                        return f"Abriendo {nombre}..."

                    except Exception as e:
                        return f"No pude abrir {nombre}. Error: {e}"

                return f"No encontré la aplicación {nombre}."

    # Detectar una aplicación que no está en el diccionario para cerrar
    frases_cerrar = [
        "cierra ",
        "cerrar ",
        "puedes cerrar ",
        "quiero cerrar "
    ]

    for frase in frases_cerrar:

        if pregunta.startswith(frase):

            nombre = pregunta[len(frase):].strip()

            if nombre:
                programa = nombre + ".exe"

                resultado = subprocess.run(
                    ["taskkill", "/IM", programa, "/F"],
                    capture_output=True,
                    text=True
                )

                if resultado.returncode == 0:
                    return f"Cerrando {nombre}..."

                return f"La aplicación {nombre} no está abierta."

    return None