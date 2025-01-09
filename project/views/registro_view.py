import flet as ft
from project.utils.autenticar_usr import autenticar

def login_view(page):
    # Contenedor para toda la vista
    return ft.Container(
        expand=True,
        alignment=ft.alignment.center,
        content=ft.Container(
            width=350,
            height=400,  # Altura limitada
            padding=20,
            alignment=ft.alignment.center,
            border_radius=10,
            bgcolor=ft.colors.WHITE,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        "Iniciar Sesión",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.TextField(label="Correo Electrónico", prefix_icon=ft.icons.EMAIL),
                    ft.TextField(label="Contraseña", password=True, prefix_icon=ft.icons.LOCK),
                    ft.ElevatedButton(
                        text="Iniciar Sesión",
                        width=200,
                        on_click=lambda e: print("Iniciando sesión..."),
                    ),
                    ft.TextButton(
                        text="¿Olvidaste tu contraseña?",
                        on_click=lambda e: print("Recuperar contraseña"),
                    ),
                    ft.TextButton(
                        text="¿No tienes cuenta? Regístrate",
                        on_click=lambda e: print("Registrarse"),
                    ),
                ],
            ),
        )
    )
