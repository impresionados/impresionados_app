import flet as ft
from project.database.crud_entero import get_product, obtener_imagen_producto_id, get_category
from project.views.header import update_cart_count

# Obtener los productos desde la base de datos
items = get_product()
max_text_len = 40

# Lista global para almacenar las categorías seleccionadas
selected_categories = []

# Función para la vista principal
def home_view(page, shopping_cart):
    products = [i for i in items]  # Lista de productos obtenidos

    # Crear una lista reactiva para los productos
    product_cards = ft.GridView(
        spacing=10,  # Espaciado entre productos
        run_spacing=15,  # Espaciado entre filas
        max_extent=450,  # Ancho máximo de cada producto (ajusta según diseño)
        expand=True,  # Expandir dinámicamente
    )

    # Actualizar la vista del grid con los productos filtrados
    def update_product_grid(product_list):
        product_cards.controls.clear()

        for product in product_list:
            is_in_cart = any(p[0] == product for p in shopping_cart)  # Verificar si el producto está en la cesta
            button_color_add_cart = ft.colors.GREEN_600 if is_in_cart else ft.colors.RED_600  # Color dinámico

            product_cards.controls.append(ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(
                                content=ft.Image(
                                    src=obtener_imagen_producto_id(product.id),
                                    fit=ft.ImageFit.CONTAIN,
                                ),
                                height=page.window_height * 0.25,  # Imagen ocupa 20% de la altura de la ventana
                                alignment=ft.alignment.center,
                                expand=True),
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Text(
                                            f"{product.name[:20]}..." if len(product.name) > 20 else product.name,
                                            style="titleSmall",
                                            color=ft.colors.BLUE_GREY_800
                                        ),
                                        ft.Text(
                                            f"{product.description[:max_text_len]}..." if len(
                                                product.description) > max_text_len else product.description,
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
                                                ft.ElevatedButton(
                                                    text="Añadir a la cesta" if not is_in_cart else "En la cesta",
                                                    icon=ft.icons.ADD_SHOPPING_CART,
                                                    style=ft.ButtonStyle(
                                                        bgcolor=button_color_add_cart,
                                                        color=ft.colors.WHITE,
                                                        shape=ft.RoundedRectangleBorder(radius=8)
                                                    ),
                                                    on_click=add_to_cart,
                                                    data=product
                                                ),
                                                ft.TextButton(
                                                    text="Ver más",
                                                    icon=ft.icons.ARROW_FORWARD,
                                                    style=ft.ButtonStyle(
                                                        bgcolor=ft.colors.BLUE_GREY_100,
                                                        color=ft.colors.BLUE_GREY_800,
                                                        shape=ft.RoundedRectangleBorder(radius=6),
                                                        overlay_color=ft.colors.BLUE_GREY_200,
                                                    ),
                                                    on_click=open_product_details,
                                                    data=product
                                                )
                                            ],
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            spacing=10
                                        )
                                    ],
                                    spacing=10,
                                    alignment=ft.MainAxisAlignment.START
                                ),
                                padding=15,
                                alignment=ft.alignment.center,
                                border_radius=10,
                                bgcolor=ft.colors.WHITE
                            )

                        ],
                        spacing=10,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                    ),
                    padding=10,
                    bgcolor=ft.colors.WHITE,
                    border_radius=10,
                    alignment=ft.alignment.center,
                ),
                elevation=10,
                margin=10
            ))
        page.update()

    # Función para aplicar filtro
    def apply_filter_name(e):
        filter_text = search_field.value.lower()
        filtered_products = [p for p in items if filter_text in p.name.lower() or filter_text in p.category]
        apply_filter_name(filtered_products)
        update_product_grid(filtered_products)

    # Función para aplicar el filtro por categorías seleccionadas
    def apply_filter_category(e, category_list):
        global selected_categories
        selected_categories = [
            cb.label for cb in category_list.controls if isinstance(cb, ft.Checkbox) and cb.value
        ]
        filtered_products = [p for p in items if any(cat in p.category for cat in selected_categories)]
        update_product_grid(filtered_products)
        page.dialog.open = False
        page.update()

    # Función para manejar la selección/deselección de categorías
    def toggle_category_selection(e, category):
        if e.control.value:
            if category not in selected_categories:
                selected_categories.append(category)
        else:
            if category in selected_categories:
                selected_categories.remove(category)

    def deselect_all_categories(category_list):
        global selected_categories
        selected_categories = []
        for cb in category_list.controls:
            if isinstance(cb, ft.Checkbox):
                cb.value = False
        page.update()

    # Función para abrir el diálogo de categorías
    def open_category_dialog(e):
        categories = list(set(get_category()))

        # Crear una nueva lista de checkboxes con las categorías seleccionadas previamente
        category_list = ft.ListView(
            controls=[
                ft.Checkbox(
                    label=cat,
                    value=cat in selected_categories,  # Marcar las categorías seleccionadas previamente
                    on_change=lambda e, cat=cat: toggle_category_selection(e, cat)
                )
                for cat in categories
            ],
            spacing=10,
            height=page.window_height * 0.85,  # Establece el 85% de la altura de la ventana principal
        )

        # Crear el diálogo
        category_dialog = ft.AlertDialog(
            title=ft.Text("Seleccionar categorías"),
            content=ft.Container(
                content=category_list,
                height=400,
                width=300,
                padding=10
            ),
            actions=[
                ft.TextButton("Deseleccionar todo", on_click=lambda e: deselect_all_categories(category_list)),
                ft.TextButton("Aplicar", on_click=lambda e: apply_filter_category(e, category_list)),
                ft.TextButton("Cerrar", on_click=lambda e: close_window(e))
            ]
        )

        # Asignar y abrir el diálogo
        page.dialog = category_dialog
        page.dialog.open = True
        page.update()

    # Función para cerrar el diálogo
    def close_window(e):
        page.dialog.open = False
        page.update()

    # Función para añadir productos a la cesta
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

        # Mostrar notificación
        page.snack_bar = ft.SnackBar(ft.Text(f"{product.name} añadido a la cesta"))
        page.snack_bar.open = True

        update_product_grid(products)

    # Abrir detalles del producto
    def open_product_details(e ):
        product = e.control.data
        is_in_cart = any(p[0] == product for p in shopping_cart)  # Verificar si el producto está en la cesta
        button_color_add_cart = ft.colors.GREEN_600 if is_in_cart else ft.colors.RED_600  # Color dinámico

        page.dialog = ft.AlertDialog(
            title=ft.Text(product.name, style="headlineMedium", color=ft.colors.BLUE_GREY_900),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Container(
                                content=ft.Image(
                                    src=obtener_imagen_producto_id(product.id),
                                    fit=ft.ImageFit.CONTAIN
                                ),
                                alignment=ft.alignment.center,
                                width=300,

                                height=page.window_height * 0.35,  # Tamaño dinámico para la altura
                                border_radius=ft.border_radius.all(10),
                            ),
                            alignment=ft.alignment.center,  # Centrar la imagen
                        ),
                        ft.Text(
                            "Descripción",
                            style="titleMedium",
                            color=ft.colors.BLUE_GREY_800
                        ),
                        ft.Text(
                            product.description,
                            style="bodyMedium",
                            max_lines=None,
                            color=ft.colors.GREY_700,
                            # overflow=ft.TextOverflow.WRAP
                        ),
                        ft.Text(
                            "Categorías",
                            style="titleMedium",
                            color=ft.colors.BLUE_GREY_800,
                            weight=ft.FontWeight.BOLD
                        ),
                        ft.Text(
                            ", ".join(product.category),
                            style="bodyMedium",
                            color=ft.colors.GREY_700
                        ),
                        ft.Text(
                            f"Precio: {product.price}€",
                            style="titleLarge",
                            color=ft.colors.GREEN_700,
                            weight=ft.FontWeight.BOLD
                        ),
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    text="Añadir a la cesta" if not is_in_cart else "En la cesta",
                                    icon=ft.icons.ADD_SHOPPING_CART,
                                    style=ft.ButtonStyle(
                                        bgcolor=button_color_add_cart,
                                        color=ft.colors.WHITE,
                                        shape=ft.RoundedRectangleBorder(radius=8)
                                    ),
                                    on_click=add_to_cart,
                                    data=product
                                ),
                                ft.TextButton(
                                    text="Cerrar",
                                    icon=ft.icons.CLOSE,
                                    style=ft.ButtonStyle(
                                        color=ft.colors.RED_600,
                                        overlay_color=ft.colors.RED_100
                                    ),
                                    on_click=close_window
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10
                        )
                    ],
                    spacing=15,
                    alignment=ft.MainAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.ALWAYS  # Habilitar el scroll para el contenido
                ),
                padding=20,
                width=page.window_width * 0.40,
                border_radius=ft.border_radius.all(12),
                bgcolor=ft.colors.WHITE,
            ),
            actions_alignment=ft.MainAxisAlignment.CENTER,
            open=True
        )

        page.update()

    # Campo de búsqueda y grid
    search_field = ft.TextField(
        label="Buscar productos...",
        on_change=apply_filter_name,
        height=50,  # Altura del campo
        text_style=ft.TextStyle(
            size=16,  # Tamaño del texto
            color=ft.colors.BLUE_GREY_800,  # Color inicial del texto
        ),
        border_color=ft.colors.BLUE_GREY_200,  # Borde suave
        border_radius=8,  # Esquinas redondeadas
        bgcolor=ft.colors.BLUE_GREY_100,
    )

    # update_product_grid(products)

    # Campo de filtrado por categoría
    category_button = ft.ElevatedButton(
        text="Filtrar por categoría",
        icon=ft.icons.FILTER_LIST,  # Icono de filtro
        style=ft.ButtonStyle(
            bgcolor=ft.colors.BLUE_GREY_100,
            color=ft.colors.BLUE_GREY_800,  # Color inicial del texto
            shape=ft.RoundedRectangleBorder(radius=8),  # Esquinas redondeadas
            overlay_color=ft.colors.BLUE_GREY_200,
            elevation={"pressed": 2, "default": 4},  # Elevación dinámica
        ),
        height=50,  # Altura igual al campo de texto
        on_click=open_category_dialog,
    )



    def apply_filter_name(e):
        filter_text = search_field.value.lower()
        filtered_products = [p for p in items if filter_text in p.name.lower() or filter_text in p.category]

        # Cambiar el color del texto dinámicamente según los resultados
        if filtered_products:
            search_field.text_style.color = ft.colors.GREEN_600  # Texto verde si hay resultados
        else:
            search_field.text_style.color = ft.colors.RED_600  # Texto rojo si no hay resultados

        search_field.update()  # Actualizar el campo de texto
        update_product_grid(filtered_products)

    update_product_grid(products)

    # Vista principal
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Catálogo de productos", style="headlineLarge", color=ft.colors.BLUE_GREY_900),
                ft.Row(
                    controls=[
                        search_field,  # Campo de búsqueda a la izquierda
                        category_button,  # Botón a la derecha
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  # Coloca los elementos en los extremos
                    spacing=0,  # Sin espacio adicional entre los controles
                ),

                product_cards,
            ],
            spacing=20,
        ),
        expand=True,
        # scroll=ft.ScrollMode.ALWAYS,  # Habilita el scroll
        padding=20,
    )
