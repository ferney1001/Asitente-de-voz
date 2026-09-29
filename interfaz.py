import flet as ft
from voz import escuchar
from comandos import procesar_comando
from google import genai
from dotenv import load_dotenv
import os


# =========================
# CONFIGURACIÓN GEMINI
# =========================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


# =========================
# INTERFAZ PRINCIPAL
# =========================

def main(page: ft.Page):

    page.title = "NOVA 🤖"
    page.window.maximized = True
    page.theme_mode = ft.ThemeMode.DARK

    modo_voz = False

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
        spacing=15,
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )

    def agregar_mensaje(mensaje):

        historial.controls.append(
            ft.Text(
                mensaje,
                size=18,
                selectable=True
            )
        )
        page.update()

    # =========================
    # PROCESAR TEXTO
    # =========================

    def procesar_texto(texto):

        if not texto:
            return

        texto = texto.strip()

        if not texto:
            return

        # Mostrar lo que dijo/escribió el usuario

        agregar_mensaje(
            "Tú: " + texto
        )

        # =========================
        # REVISAR COMANDOS
        # =========================

        respuesta_comando = procesar_comando(texto)

        if respuesta_comando:

            agregar_mensaje(
                "Nova: " + respuesta_comando
            )

            estado.value = "🟢 Estoy lista para ayudarte."
            page.update()

            return

        # =========================
        # GEMINI
        # =========================

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
    # BOTÓN DEL MICRÓFONO
    # =========================

    def iniciar_voz(e):

        nonlocal modo_voz

        if modo_voz:

            modo_voz = False

            boton_microfono.content = "🎤"

            estado.value = "🔴 Modo voz detenido."

            page.update()

            return

        modo_voz = True

        boton_microfono.content = "🔴"

        estado.value = "🟢 Modo voz activado."

        page.update()

        page.run_thread(ciclo_voz)

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

        modo_voz = False

        estado.value = "🔴 Cerrando NOVA..."

        page.update()

        await page.window.close()

    # =========================
    # CAMPO DE TEXTO
    # =========================

    campo_texto = ft.TextField(
        hint_text="Escribe un mensaje...",
        expand=True,
        on_submit=presionar_enter
    )

    # =========================
    # BOTÓN MICRÓFONO
    # =========================

    boton_microfono = ft.Button(
        content="🎤",
        width=60,
        height=50,
        on_click=iniciar_voz
    )

    # =========================
    # BOTÓN ENVIAR
    # =========================

    boton_enviar = ft.Button(
        content="➤",
        width=60,
        height=50,
        on_click=enviar_mensaje
    )

    # =========================
    # BOTÓN SALIR
    # =========================

    boton_salir = ft.Button(
        content="❌ Salir",
        width=120,
        height=40,
        on_click=cerrar_ventana
    )

    # =========================
    # BARRA DE MENSAJE
    # =========================

    barra_mensaje = ft.Row(
        controls=[
            campo_texto,
            boton_microfono,
            boton_enviar
        ],
        spacing=10
    )

    # =========================
    # INTERFAZ
    # =========================

    page.add(

        ft.Column(

            controls=[

                # Título

                titulo,

                ft.Container(
                    height=20
                ),

                # Estado

                estado,

                ft.Container(
                    height=15
                ),

                # Conversación

                ft.Container(
                    content=historial,
                    expand=True,
                    width=900
                ),

                ft.Container(
                    height=15
                ),

                # Barra para escribir

                ft.Container(
                    content=barra_mensaje,
                    width=900
                ),

                ft.Container(
                    height=15
                ),

                # Salir

                boton_salir
            ],

            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

            expand=True
        )
    )


ft.run(main)