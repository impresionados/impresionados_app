import flet as ft
from project.database.crud_entero import get_product, obtener_imagen_producto_id

# Obtener los productos desde la base de datos
items = get_product()
max_text_len = 40

def home_view(page, shopping_cart, update_cart_count):
    """
    Genera la vista principal de productos, mostrando cada uno con su imagen y permitiendo añadirlos al carrito.
    """
    products = [i for i in items]

    def add_to_cart(e):
        product = e.control.data

        if len(shopping_cart) == 0:
            shopping_cart.append([product, 1])
        else:
            for item in shopping_cart:
                if item[0].id == product.id:
                    item[1] += 1
                    break
            else:
                shopping_cart.append([product, 1])

        update_cart_count()
        page.snack_bar = ft.SnackBar(ft.Text(f"{product.name} añadido a la cesta"))
        page.snack_bar.open = True
        page.update()

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

    product_cards = [
        ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Image(src=obtener_imagen_producto_id(product.id), width=180, height=180),
                        ft.Text(
                            f"{product.name[:20]}..." if len(product.name) > 20 else product.name,
                            style="titleSmall",
                            color=ft.colors.BLUE_GREY_800
                        ),
                        ft.Text(
                            f"{product.description[:max_text_len]}..." if len(product.description) > max_text_len else product.description,
                            max_lines=3,
                            overflow=ft.TextOverflow.ELLIPSIS,
                            style="bodyMedium",
                            color=ft.colors.GREY_600
                        ),
                        ft.Text(
                            f"{product.price}€",
                            style="bodyLarge",
                            color=ft.colors.GREEN_700,
                            weight=ft.FontWeight.BOLD
                        ),
                        ft.Row(
                            controls=[
                                ft.ElevatedButton("Añadir a la cesta", on_click=add_to_cart, data=product),
                                ft.TextButton("Ver más", on_click=open_product_details, data=product)
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15
                ),
                padding=15,
                alignment=ft.alignment.center,
                border_radius=10,
                bgcolor=ft.colors.WHITE
            ),
            elevation=10,
            margin=10
        )
        for product in products
    ]

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Catálogo de productos", style="headlineLarge", color=ft.colors.BLUE_GREY_900),
                ft.GridView(
                    controls=product_cards,
                    runs_count=3,
                    spacing=20,
                    run_spacing=20,
                    max_extent=450,
                    expand=1
                )
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO
        ),
        padding=20
    )
