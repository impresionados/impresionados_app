import flet as ft

def home_view(page, shopping_cart):
    products = [
        {"name": "Figura Dragón", "price": 15.0},
        {"name": "Vasija Decorativa", "price": 12.5},
        {"name": "Llaveros Geométricos", "price": 5.0}
    ]

    # Agregar productos a la cesta
    def add_to_cart(e):
        product = e.control.data
        shopping_cart.append(product)
        page.snack_bar = ft.SnackBar(ft.Text(f"{product['name']} añadido a la cesta"))
        page.snack_bar.open = True
        page.update()

    # Crear una tarjeta para cada producto
    product_cards = [
        ft.Card(
            content=ft.Column(
                controls=[
                    ft.Text(f"{product['name']} - {product['price']}€"),
                    ft.ElevatedButton("Añadir a la cesta", on_click=add_to_cart, data=product)
                ]
            )
        ) for product in products
    ]

    return ft.Column(
        controls=[
            ft.Text("Catálogo de productos", style="headlineMedium"),
            *product_cards
        ]
    )
