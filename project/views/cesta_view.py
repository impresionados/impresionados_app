import flet as ft
from project.views.header import header
from project.database.crud_entero import obtener_imagen_producto_id
import os

def cesta_view(page, shopping_cart):
    """
    Vista de la cesta de compras que muestra los productos agregados,
    permite ajustar cantidades y ver detalles de cada producto.
    """

    # Actualizar la vista de la cesta
    def update_cart_view():
        page.controls.clear()
        page.add(header(page, shopping_cart))

        # Contenedor principal con título y productos
        page.add(
            ft.Container(
                content=ft.Column(
                    controls=[
                        # Título de la cesta
                        ft.Text(
                            "🛒 Cesta de Compras",
                            style="headlineLarge",
                            color=ft.colors.BLUE_GREY_900,
                            weight=ft.FontWeight.BOLD,
                        ),
                        # Si hay productos en la cesta
                        ft.GridView(
                            controls=[
                                ft.Card(
                                    content=ft.Container(
                                        content=ft.Column(
                                            controls=[
                                                ft.Image(
                                                    src=obtener_imagen_producto_id(item[0].id),
                                                    width=150,
                                                    height=150,
                                                    fit=ft.ImageFit.CONTAIN,
                                                ),
                                                ft.Text(item[0].name, weight="bold"),
                                                ft.Text(f"Precio: {item[0].price}€"),
                                                ft.Text(f"Cantidad: {item[1]}", style="bodySmall", color=ft.colors.BLUE_500),
                                                ft.Text(
                                                    f"Precio total: {float(item[0].price) * item[1]}€",
                                                    color=ft.colors.RED_600,
                                                    weight="bold",
                                                ),
                                                ft.ElevatedButton(
                                                    "Ver detalles",
                                                    on_click=lambda e, product=item: open_product_details(page, product),
                                                ),
                                            ],
                                            spacing=10,
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        ),
                                        padding=15,
                                        alignment=ft.alignment.center,
                                        border_radius=10,
                                        bgcolor=ft.colors.WHITE,
                                    ),
                                    elevation=3,
                                    margin=10,
                                )
                                for item in shopping_cart
                            ],
                            runs_count=2,
                            spacing=20,
                            run_spacing=20,
                            max_extent=450,
                            expand=1,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                padding=20,
            )
        )

        # Si la cesta está vacía
        if not shopping_cart:
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

        # Botones "Comprar ahora" y "Vaciar cesta"
        if shopping_cart:
            page.add(
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            "Comprar ahora",
                            icon=ft.icons.SHOPPING_CART,
                            color=ft.colors.WHITE,
                            bgcolor=ft.colors.GREEN_700,
                            on_click=lambda e: page.go("/compra") if os.path.isfile(
                                "user/user_data.json") else registrate() or page.go("/login")                        ),
                        ft.ElevatedButton(
                            "Vaciar cesta",
                            icon=ft.icons.DELETE,
                            color=ft.colors.WHITE,
                            bgcolor=ft.colors.RED_600,
                            on_click=clear_cart,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                )
            )

        page.update()

    def registrate():
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Debe iniciar sesión para realizar la compra."),
            bgcolor=ft.colors.RED_600,
            duration=3000  # El toast desaparece después de 3 segundos
        )
        page.snack_bar.open = True

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
        quantity = product_list[1]  # Cantidad inicial
        product = product_list[0]

        def add_to_cart_with_quantity(e):
            product_list[1] = quantity
            page.snack_bar = ft.SnackBar(ft.Text(f"{quantity} x {product.name} añadido(s) a la cesta"))
            page.snack_bar.open = True
            dialog.update()
            update_cart_view()  # Actualiza la vista del carrito
        # Actualizar la cantidad mostrada
        def update_quantity_display():
            quantity_display.value = str(quantity)
            quantity_display.update()

        # Aumentar la cantidad
        def increment_quantity(e):
            nonlocal quantity
            if check_stock():
                quantity += 1
                add_to_cart_with_quantity(e)
                update_quantity_display()
            else:
                dialog.open = False
                page.snack_bar = ft.SnackBar(
                    ft.Text(f"No hay más unidades de {product.name} disponibles en stock."),
                    bgcolor=ft.colors.RED,
                )
                page.snack_bar.open = True
                dialog.update()
            page.update()

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
            print(quantity)
            print(stock_in_db)
            return quantity < stock_in_db

        # Mostrar la cantidad
        quantity_display = ft.Text(value=str(quantity), size=20, weight="bold")

        # Crear el diálogo
        dialog = ft.AlertDialog(
            title=ft.Text(
                product.name,
                style="headlineMedium",
                color=ft.colors.BLUE_GREY_900,
                weight=ft.FontWeight.BOLD
            ),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Image(
                                src=obtener_imagen_producto_id(product.id),
                                fit=ft.ImageFit.CONTAIN
                            ),
                            width=300,
                            height=250,
                            alignment=ft.alignment.center,
                            border_radius=ft.border_radius.all(12),
                            bgcolor=ft.colors.BLUE_GREY_50,
                            padding=10
                        ),
                        ft.Text(
                            "Descripción:",
                            style="titleMedium",
                            color=ft.colors.BLUE_GREY_800,
                            weight=ft.FontWeight.BOLD
                        ),
                        ft.Text(
                            product.description,
                            style="bodyMedium",
                            color=ft.colors.GREY_700
                        ),
                        ft.Text(
                            f"Precio: {product.price}€",
                            style="titleLarge",
                            color=ft.colors.GREEN_700,
                            weight=ft.FontWeight.BOLD
                        ),
                        ft.Divider(height=20, thickness=1, color=ft.colors.BLUE_GREY_100),
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    text=" ",
                                    icon=ft.icons.REMOVE,
                                    on_click=decrement_quantity,
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.colors.RED_400,
                                        color=ft.colors.WHITE,
                                        shape=ft.RoundedRectangleBorder(radius=10),
                                    ),
                                ),
                                quantity_display,
                                ft.ElevatedButton(
                                    text=" ",
                                    icon=ft.icons.ADD,
                                    on_click=increment_quantity,
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.colors.GREEN_400,
                                        color=ft.colors.WHITE,
                                        shape=ft.RoundedRectangleBorder(radius=10),
                                    ),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=20
                        ),
                        ft.Container(
                            content=ft.ElevatedButton(
                                text="Cerrar",
                                icon=ft.icons.CLOSE,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.colors.BLUE_GREY_200,
                                    color=ft.colors.BLUE_GREY_900,
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                ),
                                on_click=lambda e: close_dialog()
                            ),
                            alignment=ft.alignment.center
                        )
                    ],
                    spacing=15,
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                padding=20,
                border_radius=ft.border_radius.all(12),
                bgcolor=ft.colors.WHITE,
            ),
            actions_alignment=ft.MainAxisAlignment.END,
            open=True
        )

        # Mostrar el diálogo usando page.show_dialog()
        page.show_dialog(dialog)

        def close_dialog():
            dialog.open = False
            dialog.update()

    # Inicializar la vista
    update_cart_view()
