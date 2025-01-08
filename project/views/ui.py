import flet as ft
from project.views.home_view import home_view
def home_view():
    # return ft.Column(
    #     controls=[
    #         ft.Text("Bienvenido a la página principal")
    #     ]
    # )
    return home_view()

def cesta_view():
    return ft.Column(
        controls=[
            ft.Text("Esta es la cesta")
        ]
    )

def login_view():
    return ft.Column(
        controls=[
            ft.Text("Pantalla de login")
        ]
    )
def user_view():
    return ft.Column(
        controls=[
            ft.Text("Esta es la página de usuario")
        ]
    )
