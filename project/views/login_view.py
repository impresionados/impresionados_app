import flet as ft
from project.utils.autenticar_usr import autenticar
from project.database.crud_entero import update_user, create_user
from mongoengine import get_db


def login_view(page):
    # Campos de entrada para email y contraseña
    email_field = ft.TextField(label="Correo Electrónico", prefix_icon=ft.icons.EMAIL)
    password_field = ft.TextField(label="Contraseña", password=True, prefix_icon=ft.icons.LOCK)

    # Mensaje de error o éxito
    message_text = ft.Text("", size=14, color=ft.colors.RED)

    # Función para manejar el clic en "Iniciar Sesión"
    def login_click(e):
        email = email_field.value
        password = password_field.value

        if not email or not password:
            message_text.value = "Por favor, complete todos los campos."
            message_text.color = ft.colors.RED
        elif "@" not in email:
            message_text.value = "El correo electrónico no es válido."
            message_text.color = ft.colors.RED
        else:
            # Llamar a la función de autenticación
            autenticar_usr = autenticar([email, password])
            if autenticar_usr:
                message_text.value = "Inicio de sesión exitoso."
                message_text.color = ft.colors.GREEN
                page.go("/")  # Redirigir a la página principal
                # Mostrar SnackBar de éxito al iniciar sesión
                page.snack_bar = ft.SnackBar(
                    ft.Text("Inicio de sesión exitoso", size=16, color=ft.colors.WHITE), bgcolor=ft.colors.GREEN
                )
                page.snack_bar.open = True
            else:
                message_text.value = "Correo o contraseña incorrectos."
                message_text.color = ft.colors.RED

        message_text.update()

    # Función para abrir la ventana de registro
    def open_register_view(e):
        # Campos para el registro
        username_field = ft.TextField(label="Nombre de usuario", prefix_icon=ft.icons.PERSON)
        register_email = ft.TextField(label="Correo Electrónico", prefix_icon=ft.icons.EMAIL)
        register_password = ft.TextField(label="Contraseña", password=True, prefix_icon=ft.icons.LOCK)
        confirm_password = ft.TextField(label="Confirmar Contraseña", password=True, prefix_icon=ft.icons.LOCK)
        register_message = ft.Text("", size=14, color=ft.colors.RED)

        # Función para manejar el registro
        def register_click(e):
            username = username_field.value
            email = register_email.value
            password = register_password.value
            confirm = confirm_password.value

            if not username or not email or not password or not confirm:
                register_message.value = "Por favor, complete todos los campos."
                register_message.color = ft.colors.RED
            elif "@" not in email:
                register_message.value = "El correo electrónico no es válido."
                register_message.color = ft.colors.RED
            elif password != confirm:
                register_message.value = "Las contraseñas no coinciden."
                register_message.color = ft.colors.RED
            else:
                # Llamar a la función de registro
                if create_user(username, email, password):
                    register_message.value = "Registro exitoso. Ahora puede iniciar sesión."
                    register_message.color = ft.colors.GREEN
                    close_register_view()  # Cerrar el modal tras el registro exitoso
                    # Mostrar SnackBar de éxito al registrar
                    page.snack_bar = ft.SnackBar(
                        ft.Text("Registro exitoso. Ahora puede iniciar sesión", size=16, color=ft.colors.WHITE),
                        bgcolor=ft.colors.GREEN
                    )
                    page.snack_bar.open = True
                else:
                    register_message.value = "Error al registrar. Inténtelo de nuevo."
                    register_message.color = ft.colors.RED

            register_message.update()

        # Función para cerrar el modal de registro
        def close_register_view():
            page.dialog.open = False  # Cerrar el modal
            page.update()  # Actualizar la página para reflejar los cambios

        # Crear y mostrar la ventana modal
        page.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Registro"),
            content=ft.Container(
                width=350,
                padding=20,
                content=ft.Column(
                    controls=[
                        username_field,
                        register_email,
                        register_password,
                        confirm_password,
                        register_message,
                        ft.ElevatedButton(
                            text="Registrar",
                            width=200,
                            on_click=register_click,  # Llamar a la función de registro
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ),
            actions=[
                ft.TextButton(
                    text="Cerrar",
                    on_click=lambda e: close_register_view(),  # Llamar a la función para cerrar el modal
                ),
            ],
        )
        page.dialog.open = True
        page.update()

    # Función para abrir la ventana de restablecimiento de contraseña
    def open_password_reset_dialog(e):
        # Campo para ingresar el email
        email_input = ft.TextField(label="Correo Electrónico", prefix_icon=ft.icons.EMAIL)
        message_text = ft.Text("", size=14, color=ft.colors.RED)

        # Función para manejar el envío del email
        def send_reset_email(e):
            email = email_input.value

            if not email:
                message_text.value = "Por favor, complete el correo electrónico."
                message_text.color = ft.colors.RED
                message_text.update()
                return
            users_collection = get_db()['users']

            user = users_collection.find_one({
                "email": str(email),
            })
            print("User encontrado")
            if not user:
                message_text.value = "Correo no registrado."
                message_text.color = ft.colors.RED
            else:
                # Abrir la ventana de nueva contraseña
                open_new_password_dialog(email)

            message_text.update()

        # Crear y mostrar la ventana modal para ingresar el email
        page.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Restablecer Contraseña"),
            content=ft.Container(
                width=350,
                padding=20,
                content=ft.Column(
                    controls=[
                        email_input,
                        ft.ElevatedButton("Enviar", on_click=send_reset_email),
                        message_text,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: close_dialog()),
            ],
        )
        page.dialog.open = True
        page.update()

    # Función para abrir la ventana de nueva contraseña
    def open_new_password_dialog(email):
        new_password_field = ft.TextField(label="Nueva Contraseña", password=True, prefix_icon=ft.icons.LOCK)
        confirm_password_field = ft.TextField(label="Confirmar Contraseña", password=True, prefix_icon=ft.icons.LOCK)
        message_text = ft.Text("", size=14, color=ft.colors.RED)

        # Función para manejar el cambio de contraseña
        def change_password(e):
            new_password = new_password_field.value
            confirm_password = confirm_password_field.value

            if not new_password or not confirm_password:
                message_text.value = "Por favor, complete ambos campos."
                message_text.color = ft.colors.RED
            elif new_password != confirm_password:
                message_text.value = "Las contraseñas no coinciden."
                message_text.color = ft.colors.RED
            else:
                # Actualizar la contraseña en la base de datos
                update_user(email, password=new_password)
                message_text.value = "Contraseña cambiada exitosamente."
                message_text.color = ft.colors.GREEN
                page.go("/login")

            message_text.update()

        # Crear y mostrar la ventana modal para nueva contraseña
        page.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Nueva Contraseña"),
            content=ft.Container(
                width=350,
                padding=20,
                content=ft.Column(
                    controls=[
                        new_password_field,
                        confirm_password_field,
                        message_text,
                        ft.ElevatedButton("Cambiar Contraseña", on_click=change_password),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: close_dialog()),
            ],
        )
        page.dialog.open = True
        page.update()

    # Función para cerrar el diálogo
    def close_dialog():
        if page.dialog:
            page.dialog.open = False
            page.update()

    # Contenedor para toda la vista
    return ft.Container(
        expand=True,
        alignment=ft.alignment.center,
        content=ft.Container(
            width=350,
            height=400,
            padding=20,
            alignment=ft.alignment.center,
            border_radius=10,
            bgcolor=ft.colors.WHITE,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Iniciar Sesión", size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                    email_field,
                    password_field,
                    ft.ElevatedButton("Iniciar Sesión", width=200, on_click=login_click),
                    message_text,
                    ft.TextButton("¿Olvidaste tu contraseña?", on_click=open_password_reset_dialog),
                    ft.TextButton("¿No tienes cuenta? Regístrate", on_click=open_register_view),
                ],
            ),
        ),
    )
