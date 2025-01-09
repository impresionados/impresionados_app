import flet as ft

def main(page: ft.Page):
    page.title = "Inicio de Sesión"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Valores para los campos de texto
    email_value = ft.TextField(label="Correo Electrónico", prefix_icon=ft.icons.EMAIL)
    password_value = ft.TextField(label="Contraseña", password=True, prefix_icon=ft.icons.LOCK)

    def login_click(e):
        # Lógica para iniciar sesión
        email = email_value.value
        password = password_value.value
        filtro_login(email,password)
        print(f"Email: {email}, Password: {password}")

    def forgot_password_click(e):
        # Lógica para recuperar contraseña
        print("Recuperar contraseña")

    def sign_up_click(e):
        # Lógica para registrarse
        print("Registrarse")



    def filtro_login(email,password):
        if email!= "" and password!= "" and "@" in email: #para ser más filtrado faltaria poner que detras de un @ haya algo, al igual que por delante, para que sea un correo real

            #Poner la conexión a la base de datos y preguntar por este usuario. Si la respuesta es True, proceder con el inicio correcto de el usuario.
            
            pass
    

    page.add(
        ft.Container(
            width=350,
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
                    email_value,
                    password_value,
                    ft.ElevatedButton(
                        text="Iniciar Sesión",
                        on_click=login_click,
                        width=200,
                    ),
                    ft.TextButton(
                        text="¿Olvidaste tu contraseña?",
                        on_click=forgot_password_click,
                    ),
                    ft.TextButton(
                        text="¿No tienes cuenta? Regístrate",
                        on_click=sign_up_click,
                    ),
                ],
            ),
        )
    )
ft.app(target=main)
