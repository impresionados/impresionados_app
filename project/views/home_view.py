import flet as ft
from project.database.crud_entero import get_product, obtener_imagen_producto_id, get_category
from project.views.header import update_cart_count

# Obtener los productos desde la base de datos
items = get_product()
max_text_len = 40

# Función para la vista principal
def home_view(page, shopping_cart):
    products = [i for i in items]  # Lista de productos obtenidos

    # Crear una lista reactiva para los productos
    product_cards = ft.GridView(runs_count=3, spacing=20, run_spacing=20, max_extent=390, expand=1)

    # Actualizar la vista del grid con los productos filtrados
    def update_product_grid(product_list):
        product_cards.controls.clear()
        for product in product_list:
            product_cards.controls.append(ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(
                                content=ft.Image(
                                    src=obtener_imagen_producto_id(product.id),
                                    fit=ft.ImageFit.CONTAIN
                                ),
                                expand=True,
                                alignment=ft.alignment.top_center,
                                height=page.window_height * 0.25  # Ocupa el 50% de la altura disponible
                            ),
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

    # Función para aplicar filtro
    def apply_filter_name(e):
        filter_text = search_field.value.lower()
        filtered_products = [p for p in items if filter_text in p.name.lower() or filter_text in p.category]
        update_product_grid(filtered_products)

    def apply_filter_category(e, category_list):
        selected_categories = [
            cb.label for cb in category_list.controls if isinstance(cb, ft.Checkbox) and cb.value
        ]
        filtered_products = [p for p in items if any(cat in p.category for cat in selected_categories)]
        update_product_grid(filtered_products)
        page.dialog.open = False
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

    def close_window(e):
        page.dialog.open = False
        page.update()

    def open_category_dialog(e):
        categories = list(set(get_category()))

        # Crear una nueva lista de checkboxes
        category_list = ft.Column(
            controls=[ft.Checkbox(label=cat) for cat in categories],
            spacing=10
        )

        # Crear un nuevo diálogo cada vez que se abra
        category_dialog = ft.AlertDialog(
            title=ft.Text("Seleccionar categorías"),
            content=ft.Container(
                content=category_list,
                height=400,
                width=300,
                padding=10
            ),
            actions=[
                ft.TextButton("Aplicar", on_click=lambda e: apply_filter_category(e, category_list)),
                ft.TextButton("Cerrar", on_click=lambda e: close_window(e))
            ]
        )

        # Asignar el nuevo diálogo a la página y abrirlo
        page.dialog = category_dialog
        page.dialog.open = True
        page.update()

    # Campo de búsqueda y grid
    search_field = ft.TextField(label="Buscar productos...", on_change=apply_filter_name)
    update_product_grid(products)

    # Campo de filtrado por categoría
    category_button = ft.ElevatedButton("Filtrar por categoría", on_click=open_category_dialog)
    update_product_grid(products)


    # Vista principal
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Catálogo de productos", style="headlineLarge", color=ft.colors.BLUE_GREY_900),
                search_field,
                category_button,
                product_cards
            ],
            height=page.window_width*50/100,
            spacing=20,
            expand=True,
            scroll=ft.ScrollMode.ALWAYS
        ),
        padding=20,
    )
