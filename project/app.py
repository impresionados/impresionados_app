import flet as ft
import time

# Importar las vistas
from project.views.home_view import home_view
from project.views.header import header
from project.views.cesta_view import cesta_view
from project.views.login_view import login_view
from project.views.compra_view import compra_view
from project.views.user_view import user_view

shopping_cart = []


def splash_screen(page: ft.Page):
    # Configuración de la pantalla de splash
    page.bgcolor = ft.colors.WHITE  # Fondo blanco

    logo = ft.Image(src="https://i.postimg.cc/QxtvMJLm/sinfondoo.png", width=300, height=300)

    # Usar un Container para que ocupe el 100% del ancho y alto de la página
    container = ft.Container(
        width=page.width,
        height=page.height,
        alignment=ft.alignment.center,  # Centrado en ambos ejes
        content=logo
    )

    # Agregar el contenedor con la imagen
    page.add(container)
    page.update()

    # Hacer un lerp de opacidad suave
    steps = 100  # Más pasos para una transición más suave
    for i in range(steps):
        # Cambiar la opacidad de 1 a 0 en pasos pequeños
        logo.opacity = 1 - (i / steps)  # De 1 (opacidad completa) a 0 (transparente)
        page.update()  # Actualizar la página en cada paso
        time.sleep(0.05)  # Tiempo más corto entre cada actualización para suavizar la animación

    page.clean()  # Limpiar la pantalla después del splash
    page.update()



def main(page: ft.Page):
    page.title = "Tienda 3D"
    page.theme_mode = ft.ThemeMode.LIGHT

    # Llamar a la pantalla de splash antes de cargar la app principal
    splash_screen(page)

    # Después del splash, continuar con la carga de las vistas
    page.update()

    # Manejo de las rutas
    def on_route_change(route):
        page.controls.clear()
        page.add(header(page, shopping_cart))

        if route.route == "/":
            page.add(home_view(page, shopping_cart))
        elif route.route == "/cesta":
            page.add(cesta_view(page, shopping_cart))
        elif route.route == "/login":
            page.add(login_view(page))
        elif route.route == "/compra":
            page.add(compra_view(page, shopping_cart))
        else:
            page.add(user_view(page))

        page.update()

    page.on_route_change = on_route_change
    page.go("/")

ft.app(target=main)