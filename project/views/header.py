import flet as ft

def header(page, shopping_cart, cart_count_text):
    # Actualizar el contador de productos directamente desde app.py
    home_button = ft.ElevatedButton("Inicio", on_click=lambda e: page.go("/"))
    cart_button = ft.ElevatedButton("Cesta", on_click=lambda e: page.go("/cesta"))
    login_button = ft.ElevatedButton("Login", on_click=lambda e: page.go("/login"))

    return ft.Row(
        controls=[
            ft.Text("Tienda 3D", style="headlineMedium"),
            home_button,
            cart_button,
            login_button,
            cart_count_text
        ]
    )
