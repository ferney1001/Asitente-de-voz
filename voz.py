import speech_recognition as sr


def escuchar():

    reconocedor = sr.Recognizer()

    reconocedor.energy_threshold = 300
    reconocedor.dynamic_energy_threshold = True
    reconocedor.pause_threshold = 2
    reconocedor.phrase_threshold = 0.3
    reconocedor.non_speaking_duration = 0.8

    with sr.Microphone() as microfono:

        print("Habla...")

        try:

            audio = reconocedor.listen(
                microfono,
                timeout=5,
                phrase_time_limit=10
            )

        except sr.WaitTimeoutError:

            print("Tiempo de espera agotado")

            return ""

    try:

        texto = reconocedor.recognize_google(
            audio,
            language="es-CO"
        )

        print("Tú dijiste:", texto)

        return texto

    except sr.UnknownValueError:

        print("No pude entender lo que dijiste")

        return ""

    except sr.RequestError:

        print("No se pudo conectar con el servicio de reconocimiento")

        return ""