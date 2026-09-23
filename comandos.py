import os
from aplicaciones import APLICACIONES
# hasta aqui por hoy


def abrir_aplicacion(nombre):
    programa = APLICACIONES.get(nombre)

    if programa:
        os.startfile(programa)
        return f"Abriendo {nombre}..."

    return None
