import flet as ft
from voz import escuchar
from comandos import procesar_comando


def main(page: ft.Page):

    page.title = "NOVA 🤖"
    page.window.width = 600
    page.window.height = 700
    page.theme_mode = ft.ThemeMode.DARK

    modo_voz = False

    titulo = ft.Text(
        "NOVA 🤖",
        size=32,
        weight=ft.FontWeight.BOLD
    )

    estado = ft.Text(
        "Estoy lista para ayudarte",
        size=18
    )

    historial = ft.Column(
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
        height=200
    )

    def agregar_mensaje(mensaje):

        historial.controls.append(
            ft.Text(
                mensaje,
                size=16
            )
        )

        page.update()

    def ciclo_voz():

        while modo_voz:

            estado.value = "🎤 Escuchando..."
            page.update()

            texto = escuchar()

            if not modo_voz:
                break

            if texto:

                agregar_mensaje(
                    "Tú: " + texto
                )

                respuesta_comando = procesar_comando(texto)

                if respuesta_comando:

                    agregar_mensaje(
                        "Nova: " + respuesta_comando
                    )

                estado.value = "🟢 Estoy lista para escucharte."

                page.update()

            else:

                estado.value = "No pude entenderte."

                page.update()

    def iniciar_voz(e):

        nonlocal modo_voz

        if modo_voz:

            modo_voz = False

            boton_voz.content = "🎤 Modo Voz"

            estado.value = "🔴 Modo voz detenido."

            page.update()

        else:

            modo_voz = True

            boton_voz.content = "🔴 Detener Voz"

            estado.value = "🟢 Modo voz activado."

            page.update()

            page.run_thread(ciclo_voz)

    async def cerrar_ventana(e):

        nonlocal modo_voz

        modo_voz = False

        await page.window.close()

    boton_voz = ft.Button(
        content="🎤 Modo Voz",
        width=200,
        height=50,
        on_click=iniciar_voz
    )

    boton_teclado = ft.Button(
        content="⌨️ Modo Teclado",
        width=200,
        height=50
    )

    boton_salir = ft.Button(
        content="❌ Salir",
        width=120,
        height=40,
        on_click=cerrar_ventana
    )

    page.add(
        ft.Column(
            controls=[
                titulo,

                ft.Container(height=30),

                ft.Container(
                    content=ft.Text(
                        "NOVA",
                        size=80
                    ),
                    alignment=ft.Alignment.CENTER,
                    height=150
                ),

                estado,

                ft.Container(height=20),

                historial,

                ft.Container(height=20),

                boton_voz,
                boton_teclado,

                ft.Container(height=20),

                boton_salir
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        )
    )


ft.run(main)