import os
import json
import flet as ft

# Función para mostrar los datos del usuario
def user_view(page):
    # Leer los datos del usuario desde el archivo JSON
    user_data = {}
    if os.path.isfile("user/user_data.json"):
        try:
            with open("user/user_data.json", "r") as file:
                user_data = json.load(file)
        except json.JSONDecodeError:
            print("Error al leer el archivo JSON.")
        except Exception as e:
            print(f"Se produjo un error: {e}")

    # Crear los campos para mostrar los datos
    user_field = ft.TextField(
        label="Usuario",
        value=user_data.get("usuario", "N/A"),
        read_only=True,
        prefix_icon=ft.icons.PERSON,
    )
    email_field = ft.TextField(
        label="Correo Electrónico",
        value=user_data.get("email", "N/A"),
        read_only=True,
        prefix_icon=ft.icons.EMAIL,
    )
    password_visible = False
    # Función para alternar la visibilidad de la contraseña
    def toggle_password_visibility(e):
        nonlocal password_visible
        password_visible = not password_visible
        password_field.password = not password_visible
        password_field.suffix.icon = ft.icons.VISIBILITY if password_visible else ft.icons.VISIBILITY_OFF
        page.update()

    password_field = ft.TextField(
        label="Contraseña",
        value=user_data.get("password", "N/A"),
        password=True,
        read_only=True,
        expand=True,
        suffix=ft.IconButton(
            icon=ft.icons.VISIBILITY_OFF,
            on_click=toggle_password_visibility,
        ),
    )

    # Contenedor para toda la vista
    return ft.Container(
        expand=True,
        alignment=ft.alignment.center,
        content=ft.Container(
            width=500,
            height=400,
            padding=20,
            alignment=ft.alignment.center,
            border_radius=10,
            bgcolor=ft.colors.WHITE,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        "Datos del Usuario",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    user_field,
                    email_field,
                    ft.Row(
                        controls=[
                            password_field,

                        ],
                        alignment=ft.MainAxisAlignment.END,
                    )
                ],
            ),
        )
    )