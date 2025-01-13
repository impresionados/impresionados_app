import flet as ft
from project.views.home_view import home_view
from project.views.header import header
from project.views.cesta_view import cesta_view
from project.views.login_view import login_view
from project.views.compra_view import compra_view

shopping_cart = []

def main(page: ft.Page):
    page.title = "Tienda 3D"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.update()

    # Crear la cabecera y definir la función para actualizarla
    cart_count_text = ft.Text(f"Cesta ({len(shopping_cart)})")

    def update_cart_count():
        cart_count_text.value = f"Cesta ({len(shopping_cart)})"
        cart_count_text.update()

    def on_route_change(route):
        page.controls.clear()
        page.add(header(page, shopping_cart, cart_count_text))

        if route.route == "/":
            page.add(home_view(page, shopping_cart, update_cart_count))
        elif route.route == "/cesta":
            page.add(cesta_view(page, shopping_cart))
        elif route.route == "/login":
            page.add(login_view(page))
        elif route.route == "/compra":
            page.add(compra_view(page, shopping_cart))

        page.update()

    page.on_route_change = on_route_change
    page.go("/")

ft.app(target=main)
