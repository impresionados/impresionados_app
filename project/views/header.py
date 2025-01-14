import flet as ft
import os


cart_count_text = ft.Text(f"Cesta (0)", style="bodyLarge")
def update_cart_count(shopping_cart):
    cart_count_text.value = f"Cesta ({len(shopping_cart)})"
    cart_count_text.update()
def header(page, shopping_cart):

    # Actualizar el contador de productos


    home_button = ft.ElevatedButton("Inicio",
                                    width=150,  # Ajusta el ancho del botón
                                    height=35,  # Ajusta la altura del botón
                                    on_click=lambda e: page.go("/"),)
    cart_button = ft.ElevatedButton("Cesta",
                                    width=150,  # Ajusta el ancho del botón
                                    height=35,  # Ajusta la altura del botón
                                    on_click=lambda e: [page.go("/cesta"), update_cart_count(shopping_cart)])
    user_button = ft.ElevatedButton(
        text="Perfil",
        icon=ft.icons.PERSON,
        on_click=lambda e: page.go("/login") if not os.path.isfile('user/user_data.json') else page.go("/user_data"),
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=ft.colors.GREEN if os.path.isfile("user/user_data.json") else ft.colors.RED_600,
        ),
    )

    return ft.Row(
    controls=[
        # Sección izquierda: Icono y texto "Tienda 3D"
        ft.Row(
            controls=[
                ft.Icon(ft.icons.STORE, size=30, color=ft.colors.BLUE_GREY),
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

        # Sección central: Botones "Inicio" y "Cesta"
        ft.Row(
            controls=[
                home_button,
                cart_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=50,
            expand=1,
        ),

        # Sección derecha: Contador de cesta y botón de perfil
        ft.Row(
            controls=[
                cart_count_text,
                user_button,
            ],
            alignment=ft.MainAxisAlignment.END,
            expand=1,
        ),
    ],
    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
)

