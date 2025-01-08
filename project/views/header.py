# import flet as ft
#
# def header():
#     return ft.Row(
#         controls=[
#             ft.Text("Mi App", style="headlineSmall"),
#             ft.ElevatedButton("Home", on_click=lambda e: e.page.go("/")),
#             ft.ElevatedButton("Cesta", on_click=lambda e: e.page.go("/cesta")),
#             ft.ElevatedButton("Login", on_click=lambda e: e.page.go("/login")),
#             ft.ElevatedButton("Usuario", on_click=lambda e: e.page.go("/user")),
#         ]
#     )
import flet as ft

def header(page, shopping_cart):
    cart_count_text = ft.Text(f"Cesta ({len(shopping_cart)})")

    # Actualizar el contador de productos
    def update_cart_count():
        cart_count_text.value = f"Cesta ({len(shopping_cart)})"
        cart_count_text.update()

    home_button = ft.ElevatedButton("Inicio", on_click=lambda e: page.go("/"))
    cart_button = ft.ElevatedButton("Cesta", on_click=lambda e: [page.go("/cesta"), update_cart_count()])
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
