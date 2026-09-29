import flet as ft
from voz import escuchar
from comandos import procesar_comando
from google import genai
from dotenv import load_dotenv
import os


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def main(page: ft.Page):

    page.title = "NOVA 🤖"
    page.window.maximized = True
    page.theme_mode = ft.ThemeMode.DARK

    modo_voz = False
    modo_teclado = False

    # =========================
    # TÍTULO
    # =========================

    titulo = ft.Text(
        "NOVA 🤖",
        size=32,
        weight=ft.FontWeight.BOLD
    )

    estado = ft.Text(
        "Estoy lista para ayudarte",
        size=18
    )

    # =========================
    # HISTORIAL
    # =========================

    historial = ft.Column(
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
        height=300
    )

    def agregar_mensaje(mensaje):

        historial.controls.append(
            ft.Text(
                mensaje,
                size=16
            )
        )

        page.update()

    # =========================
    # PROCESAR TEXTO
    # =========================

    def procesar_texto(texto):

        if not texto:
            return

        agregar_mensaje(
            "Tú: " + texto
        )

        # Primero revisamos si es un comando
        respuesta_comando = procesar_comando(texto)

        if respuesta_comando:

            agregar_mensaje(
                "Nova: " + respuesta_comando
            )

            return

        # Si no es un comando, usamos Gemini

        estado.value = "🧠 Pensando..."
        page.update()

        try:

            respuesta = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=texto
            )

            agregar_mensaje(
                "Nova: " + respuesta.text
            )

        except Exception as e:

            print("Error Gemini:", e)

            agregar_mensaje(
                "Nova: No pude conectarme con Gemini."
            )

        estado.value = "🟢 Estoy lista para ayudarte."
        page.update()

    # =========================
    # MODO VOZ
    # =========================

    def ciclo_voz():

        while modo_voz:

            estado.value = "🎤 Escuchando..."
            page.update()

            texto = escuchar()

            if not modo_voz:
                break

            if texto:

                procesar_texto(texto)

            else:

                if modo_voz:

                    estado.value = "No pude entenderte."
                    page.update()

    # =========================
    # ACTIVAR / DESACTIVAR VOZ
    # =========================

    def iniciar_voz(e):

        nonlocal modo_voz
        nonlocal modo_teclado

        if modo_voz:

            modo_voz = False

            boton_voz.content = "🎤 Modo Voz"

            estado.value = "🔴 Modo voz detenido."

            page.update()

            return

        modo_voz = True
        modo_teclado = False

        boton_voz.content = "🔴 Detener Voz"

        boton_teclado.content = "⌨️ Modo Teclado"

        campo_texto.visible = False
        boton_enviar.visible = False

        estado.value = "🟢 Modo voz activado."

        page.update()

        page.run_thread(ciclo_voz)

    # =========================
    # MODO TECLADO
    # =========================

    def activar_teclado(e):

        nonlocal modo_teclado
        nonlocal modo_voz

        if modo_teclado:

            modo_teclado = False

            campo_texto.visible = False
            boton_enviar.visible = False

            boton_teclado.content = "⌨️ Modo Teclado"

            estado.value = "🔴 Modo teclado detenido."

            page.update()

            return

        # Activamos teclado

        modo_teclado = True

        # Si estaba activo el modo voz,
        # lo detenemos

        modo_voz = False

        boton_voz.content = "🎤 Modo Voz"

        boton_teclado.content = "🔴 Detener Teclado"

        campo_texto.visible = True
        boton_enviar.visible = True

        estado.value = "⌨️ Modo teclado activado."

        campo_texto.focus()

        page.update()

    # =========================
    # ENVIAR MENSAJE
    # =========================

    def enviar_mensaje(e):

        texto = campo_texto.value.strip()

        if not texto:
            return

        campo_texto.value = ""

        page.update()

        procesar_texto(texto)

        campo_texto.focus()

    # =========================
    # ENTER PARA ENVIAR
    # =========================

    def presionar_enter(e):

        enviar_mensaje(e)

    # =========================
    # CERRAR NOVA
    # =========================

    async def cerrar_ventana(e):

        nonlocal modo_voz
        nonlocal modo_teclado

        modo_voz = False
        modo_teclado = False

        estado.value = "🔴 Cerrando NOVA..."

        page.update()

        await page.window.close()

    # =========================
    # CONTROLES
    # =========================

    boton_voz = ft.Button(
        content="🎤 Modo Voz",
        width=200,
        height=50,
        on_click=iniciar_voz
    )

    boton_teclado = ft.Button(
        content="⌨️ Modo Teclado",
        width=200,
        height=50,
        on_click=activar_teclado
    )
    campo_texto = ft.TextField(
        label="Escribe tu mensaje",
        hint_text="Ejemplo: ¿Qué es Python?",
        width=500,
        visible=False,
        on_submit=presionar_enter
    )

    boton_enviar = ft.Button(
        content="Enviar",
        width=120,
        height=45,
        on_click=enviar_mensaje,
        visible=False
    )

    boton_salir = ft.Button(
        content="❌ Salir",
        width=120,
        height=40,
        on_click=cerrar_ventana
    )

    # =========================
    # INTERFAZ
    # =========================

    page.add(

        ft.Column(

            controls=[

                titulo,

                ft.Container(
                    height=30
                ),

                ft.Container(
                    content=ft.Text(
                        "NOVA",
                        size=80
                    ),
                    alignment=ft.Alignment.CENTER,
                    height=150
                ),

                estado,

                ft.Container(
                    height=20
                ),

                historial,

                ft.Container(
                    height=20
                ),

                ft.Row(
                    controls=[
                        boton_voz,
                        boton_teclado
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20
                ),

                ft.Row(
                    controls=[
                        campo_texto,
                        boton_enviar
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),

                ft.Container(
                    height=20
                ),

                boton_salir
            ],

            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        )
    )


ft.run(main)