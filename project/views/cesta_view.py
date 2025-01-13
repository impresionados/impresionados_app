import flet as ft
from project.views.header import header
from project.database.crud_entero import obtener_imagen_producto_id


def cesta_view(page, shopping_cart,update_cart_count):
    """
        Vista de la cesta de compras que muestra los productos agregados,
        permite ajustar cantidades y ver detalles de cada producto.
        """
    # Actualizar la vista de la cesta
    def update_cart_view():
        page.controls.clear()
        page.add(header(page, shopping_cart, update_cart_count))

        # Título de la cesta
        page.add(ft.Text("🛒 Cesta de Compras", style="headlineMedium", weight="bold"))

        # Si hay productos en la cesta
        if shopping_cart:
            product_cards = [
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Image(
                                    src=obtener_imagen_producto_id(item[0].id),
                                    width=150,
                                    height=50,
                                    fit=ft.ImageFit.CONTAIN,
                                ),
                                ft.Text(item[0].name, weight="bold"),
                                ft.Text(f"Precio: {item[0].price}€"),
                                ft.Text(f"Cantidad: {item[1]}", style="bodySmall", color=ft.colors.BLUE_500),
                                ft.ElevatedButton(
                                    "Ver detalles",
                                    on_click=lambda e, product=item: open_product_details(page, product),
                                ),
                                ft.Text(f"Precio total: {float(item[0].price) * item[1]}€", color=ft.colors.RED_600),
                            ],
                            spacing=5,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        padding=10,
                        width=200,
                        height=250,
                        alignment=ft.alignment.center,

                    ),
                    elevation=3,
                    margin=5,
                )
                for item in shopping_cart
            ]

            # Añadir los productos al GridView
            page.add(
                ft.GridView(
                    controls=product_cards,
                    runs_count=2,
                    spacing=10,
                    run_spacing=10,
                    max_extent=220,
                    expand=1,
                )
            )

            # Botón para proceder a la compra
            page.add(
                ft.ElevatedButton(
                    "Comprar ahora",
                    icon=ft.icons.SHOPPING_CART,
                    color=ft.colors.WHITE,
                    bgcolor=ft.colors.GREEN_700,
                    on_click=lambda e: page.go("/compra"),
                )
            )

            page.add(
                ft.ElevatedButton(
                    "Vaciar cesta",
                    icon=ft.icons.DELETE,
                    color=ft.colors.WHITE,
                    bgcolor=ft.colors.RED_600,
                    on_click=clear_cart,
                )
            )
        else:
            # Mensaje de cesta vacía
            page.add(
                ft.Container(
                    content=ft.Text(
                        "🫙 Tu cesta está vacía 🫙",
                        style="headlineLarge",
                        weight="bold",
                        color=ft.colors.RED_500,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    alignment=ft.alignment.center,
                    expand=True,
                )
            )

        # Botón para vaciar la cesta


        page.update()

    # Función para vaciar la cesta
    def clear_cart(e):
        shopping_cart.clear()
        page.snack_bar = ft.SnackBar(ft.Text("Cesta vaciada 🧹"))
        page.snack_bar.open = True
        update_cart_view()

    # Función para abrir el diálogo de detalles del producto
    def open_product_details(page, product_list):
        """
        Abre un diálogo emergente que permite ajustar la cantidad de un producto
        y añadirlo a la cesta con la cantidad seleccionada.
        """
        quantity = product_list[1] # Cantidad inicial
        product = product_list[0]

        # Actualizar la cantidad mostrada
        def update_quantity_display():
            quantity_display.value = str(quantity)
            quantity_display.update()  # Actualiza solo el control de cantidad

        # Aumentar la cantidad
        def increment_quantity(e):
            nonlocal quantity
            if check_stock():
                quantity += 1
                update_quantity_display()
                add_to_cart_with_quantity(e)
            else:
                dialog.open = False
                page.snack_bar = ft.SnackBar(
                    ft.Text(f"No hay más unidades de {product.name} disponibles en stock."),
                    bgcolor=ft.colors.RED,
                )
                page.snack_bar.open = True
                page.update()  # Actualiza la página para que el SnackBar se muestre


        # Disminuir la cantidad
        def decrement_quantity(e):
            nonlocal quantity
            if quantity > 1:
                quantity -= 1
                update_quantity_display()
            elif quantity == 1:
                quantity -= 1
                shopping_cart.remove(product_list)
                dialog.open = False
                update_quantity_display()

            add_to_cart_with_quantity(e)

        def check_stock() -> bool:
            stock_in_db = product.stock
            return quantity < stock_in_db

        # Añadir a la cesta con la cantidad seleccionada
        def add_to_cart_with_quantity(e):
            product_list[1] = quantity
            page.snack_bar = ft.SnackBar(ft.Text(f"{quantity} x {product.name} añadido(s) a la cesta"))
            page.snack_bar.open = True
            dialog.update()
            update_cart_view()  # Actualiza la vista del carrito

        # Mostrar la cantidad
        quantity_display = ft.Text(value=str(quantity), size=20, weight="bold")

        # Crear el diálogo
        dialog = ft.AlertDialog(
            title=ft.Text(product.name, style="headlineMedium"),
            content=ft.Column(
                controls=[
                    ft.Image(src=obtener_imagen_producto_id(product.id), width=300, height=300),
                    ft.Text(f"Descripción: {product.description}", style="bodyLarge"),
                    ft.Text(f"Precio: {product.price}€", style="bodyLarge"),
                    ft.Row(
                        controls=[
                            ft.ElevatedButton("-", on_click=decrement_quantity),
                            quantity_display,
                            ft.ElevatedButton("+", on_click=increment_quantity),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20,
                    ),
                    ft.ElevatedButton("Cerrar", on_click=lambda e: close_dialog()),
                ],
                spacing=10,
            ),
        )

        # Mostrar el diálogo usando page.show_dialog()
        page.show_dialog(dialog)

        def close_dialog():
            dialog.open = False  # Cierra el diálogo
            dialog.update()  # Actualiza solo el diálogo

    # Inicializar la vista
    update_cart_view()
