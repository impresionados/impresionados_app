import flet as ft
import os

def header(page, shopping_cart):
    # Crear el contador de la cesta y almacenarlo en la página
    page.cart_count_text = ft.Text(f"Cesta ({len(shopping_cart)})", style="bodyLarge")

    # Botón de inicio
    home_button = ft.ElevatedButton(
        "Inicio",
        width=150,
        height=35,
        on_click=lambda e: page.go("/")
    )

    # Botón de cesta
    cart_button = ft.ElevatedButton(
        "Cesta",
        width=150,
        height=35,
        on_click=lambda e: [page.go("/cesta"), update_cart_count(page, shopping_cart)]
    )

    # Botón de perfil
    user_button = ft.ElevatedButton(
        text="Perfil",
        icon=ft.icons.PERSON,
        on_click=lambda e: page.go("/login") if not os.path.isfile('user/user_data.json') else page.go("/user_data"),
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=ft.colors.GREEN if os.path.isfile("user/user_data.json") else ft.colors.RED_600,
        ),
    )

    # Retornar el layout del header
    return ft.Row(
        controls=[
            # Sección izquierda
            ft.Row(
                controls=[
                    ft.Image(src="https://i.postimg.cc/QxtvMJLm/sinfondoo.png", width=30, height=30),
                    ft.Text(
                        "Tienda 3D",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.BLUE_800,
                        text_align=ft.TextAlign.LEFT,
                    ),
                ],
                spacing=5,
                expand=1,
            ),
            # Sección central
            ft.Row(
                controls=[home_button, cart_button],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=50,
                expand=1,
            ),
            # Sección derecha
            ft.Row(
                controls=[page.cart_count_text, user_button],
                alignment=ft.MainAxisAlignment.END,
                expand=1,
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )


# Función para actualizar el contador del carrito
def update_cart_count(page, shopping_cart):
    page.cart_count_text.value = f"Cesta ({len(shopping_cart)})"
    page.cart_count_text.update()
