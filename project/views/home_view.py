import flet as ft
from project.database.crud_entero import get_product, obtener_imagen_producto_id
from project.views.header import update_cart_count

# Obtener los productos desde la base de datos
items = get_product()
max_text_len = 40

# Función para la vista principal
def home_view(page, shopping_cart):
    products = [i for i in items]  # Lista de productos obtenidos

    # Función para aplicar filtro
    def apply_filter(e):
        filter_text = search_field.value.lower()
        filtered_products = [p for p in items if filter_text in p.name.lower() or filter_text in p.category]
        update_product_grid(filtered_products)

    # Actualizar la vista del grid con los productos filtrados
    def update_product_grid(product_list):
        product_cards.clear()
        for product in product_list:
            product_cards.append(ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Image(src=obtener_imagen_producto_id(product.id), width=180, height=180),
                            ft.Text(f"{product.name[:20]}..." if len(product.name) > 20 else product.name,
                                    style="titleSmall", color=ft.colors.BLUE_GREY_800),
                            ft.Text(f"{product.description[:max_text_len]}..." if len(product.description) > max_text_len else product.description,
                                    max_lines=3, overflow=ft.TextOverflow.ELLIPSIS, style="bodyMedium", color=ft.colors.GREY_600),
                            ft.Text(f"{product.price}€", style="bodyLarge", color=ft.colors.GREEN_700, weight=ft.FontWeight.BOLD),
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
            ))
        page.update()

    # Agregar productos a la cesta
    def add_to_cart(e):
        product = e.control.data
        for product_in_cart in shopping_cart:
            if product_in_cart[0] == product:
                if not product_in_cart[1] == product_in_cart[0].stock:
                    product_in_cart[1] += 1
                    break
                else:
                    page.snack_bar = ft.SnackBar(
                        ft.Text(f"No hay más unidades de {product.name} disponibles en stock."),
                        bgcolor=ft.colors.RED,
                    )
                    page.snack_bar.open = True
                    page.update()
                    break
        else:
            shopping_cart.append([product, 1])
            update_cart_count(page, shopping_cart)
        page.snack_bar = ft.SnackBar(ft.Text(f"{product.name} añadido a la cesta"))
        page.snack_bar.open = True
        page.update()

    # Abrir detalles del producto
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

    # Campo de búsqueda y grid
    search_field = ft.TextField(label="Buscar productos...", on_change=apply_filter)
    product_cards = []
    update_product_grid(products)

    # Vista principal
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Catálogo de productos", style="headlineLarge", color=ft.colors.BLUE_GREY_900),
                search_field,
                ft.GridView(
                    controls=product_cards,
                    runs_count=3,
                    spacing=20,
                    run_spacing=20,
                    max_extent=450,
                    expand=1,
                )
            ],
            height=page.window_width*50/100,
            spacing=20,
            expand=True,
            scroll=ft.ScrollMode.ALWAYS
        ),
        padding=20,
    )
