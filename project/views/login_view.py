import flet as ft

def login_view():
    # Función de inicio de sesión simulada
    def on_login(e):
        username = username_input.value
        password = password_input.value

        if username == "admin" and password == "admin":
            login_status.value = "Inicio de sesión exitoso!"
        else:
            login_status.value = "Usuario o contraseña incorrectos."

        login_status.update()

    username_input = ft.TextField(label="Usuario", autofocus=True)
    password_input = ft.TextField(label="Contraseña", password=True)
    login_button = ft.ElevatedButton("Iniciar sesión", on_click=on_login)
    login_status = ft.Text("", style="bodyMedium")

    return ft.Column(
        controls=[
            username_input,
            password_input,
            login_button,
            login_status,
        ]
    )
