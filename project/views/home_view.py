import flet as ft
from project.utils.obtener_productos import obtener_productos, obtener_imagen_producto_id

# Obtener los productos desde la base de datos
items = obtener_productos()
shopping_cart = []  # Lista para almacenar los productos añadidos
print(items)
# Función TEMPORAL para la vista principal
def home_view(page, shopping_cart):
    """
    Genera la vista principal de productos, mostrando cada uno con su imagen y permitiendo añadirlos al carrito.
    """
    products = [i for i in items]  # Lista de productos obtenidos

    # Agregar productos a la cesta
    def add_to_cart(e):
        product = e.control.data
        shopping_cart.append(product)
        page.snack_bar = ft.SnackBar(ft.Text(f"{product.name} añadido a la cesta"))
        page.snack_bar.open = True
        page.update()

    # Crear una lista de tarjetas (grid) para los productos
    product_cards = [
        ft.Card(
            content=ft.Column(
                controls=[
                    ft.Image(src=obtener_imagen_producto_id(product.id), width=150, height=150),
                    ft.Text(f"{product.name}\n{product.description}\n{product.price}€"),
                    ft.ElevatedButton("Añadir a la cesta", on_click=add_to_cart, data=product)
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER  # Centrar los elementos en la tarjeta
            ),
            elevation=5
        ) for product in products
    ]

    # Uso de GridView para mostrar los productos con scroll
    return ft.Column(
        controls=[
            ft.Text("Catálogo de productos", style="headlineMedium"),
            ft.GridView(  # Grid para las tarjetas
                controls=product_cards,
                runs_count=3,  # Número de columnas en la cuadrícula
                spacing=10,  # Espaciado entre los elementos
                run_spacing=10,
                max_extent=300,  # Ancho máximo de cada tarjeta
                expand=1  # Permite el scroll vertical automáticamente
            )
        ]
    )