import flet as ft
from project.tests.get_user_db import get_user_by_id  # Función para obtener el usuario de MongoDB

# Obtener los datos del usuario por su ID
def usuario_view(user_id: int):
    # Obtener los datos del usuario desde MongoDB
    user_data = get_user_by_id(user_id)  # Esta función debe devolver un documento con los datos del usuario

    if not user_data:
        return ft.Text("No se encontraron datos de usuario.", style="headlineMedium")

    # Mostrar los datos del usuario
    return ft.Column(
        controls=[
            ft.Text(f"Nombre: {user_data.user_name}", style="headlineMedium"),
            ft.Text(f"Correo electrónico: {user_data.email}", style="bodyMedium"),
            ft.Text(f"Fecha de registro: {user_data.registration_date.strftime('%Y-%m-%d %H:%M:%S')}", style="bodyMedium"),
            # Asumimos que el campo 'profile_picture_url' no está en el modelo, si lo estuvieras usando, añadiríamos la imagen aquí
            # ft.Image(src=user_data.profile_picture_url, width=150, height=150),  # Imagen de perfil
            ft.ElevatedButton("Volver a la tienda", on_click=lambda e: e.page.go("/")),
        ]
    )
