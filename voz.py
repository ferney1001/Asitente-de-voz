
import speech_recognition as sr


def escuchar():
    reconocedor = sr.Recognizer()

    with sr.Microphone() as microfono:
        print("Habla...")
        audio = reconocedor.listen(microfono)

    try:
        texto = reconocedor.recognize_google(
            audio,
            language="es-CO"
        )

        return texto

    except sr.UnknownValueError:
        print("No pude entender lo que dijiste")
        return ""

    except sr.RequestError:
        print("No se pudo conectar con el servicio de reconocimiento")
        return ""

