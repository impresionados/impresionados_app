import flet as ft
from project.database.crud_entero import get_product, obtener_imagen_producto_id

# Obtener los productos desde la base de datos
items = get_product()
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

    # Abrir ventana de detalles del producto
    def open_product_details(e):
        product = e.control.data

        def close_window(e):
            page.dialog.open = False
            page.update()

        page.dialog = ft.AlertDialog(
            title=ft.Text(product.name, style="headlineMedium"),
            content=ft.Column(
                controls=[
                    ft.Image(src=obtener_imagen_producto_id(product.id), width=300, height=300),
                    ft.Text(f"Descripción: {product.description}", style="bodyLarge"),
                    ft.Text(f"Precio: {product.price}€", style="bodyLarge"),
                    ft.ElevatedButton("Añadir a la cesta", on_click=add_to_cart, data=product),
                    ft.ElevatedButton("Cerrar", on_click=close_window)
                ],
                spacing=10
            ),
            open=True
        )
        page.update()

    # Crear una lista de tarjetas (grid) para los productos
    product_cards = [
        ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Image(src=obtener_imagen_producto_id(product.id), width=150, height=150),
                        ft.Text(
                            f"{product.name}\n{product.description}\n{product.price}€",
                            max_lines=2,
                            overflow=ft.TextOverflow.ELLIPSIS,
                            style="bodySmall"
                        ),
                        ft.Row(
                            controls=[
                                ft.ElevatedButton("Añadir a la cesta", on_click=add_to_cart, data=product),
                                ft.TextButton("Ver más", on_click=open_product_details, data=product)
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10
                ),
                padding=10,
                width=250,
                height=400,
                alignment=ft.alignment.center
            ),
            elevation=5
        ) for product in products
    ]

    # Uso de GridView para mostrar los productos con scroll
    return ft.Column(
        controls=[
            ft.Text("Catálogo de productos", style="headlineMedium"),
            ft.GridView(
                controls=product_cards,
                runs_count=3,
                spacing=10,
                run_spacing=10,
                max_extent=300,
                expand=1
            )
        ]
    )
