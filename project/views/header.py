import flet as ft
import os


cart_count_text = ft.Text(f"Cesta (0)", style="bodyLarge")
def update_cart_count(shopping_cart):
    cart_count_text.value = f"Cesta ({len(shopping_cart)})"
    cart_count_text.update()
def header(page, shopping_cart):

    # Actualizar el contador de productos


    home_button = ft.ElevatedButton("Inicio", on_click=lambda e: page.go("/"))
    cart_button = ft.ElevatedButton("Cesta", on_click=lambda e: [page.go("/cesta"), update_cart_count(shopping_cart)])
    user_button = ft.ElevatedButton(
        text="Perfil",
        icon=ft.icons.PERSON,
        on_click=lambda e: page.go("/login") if not os.path.isfile('user/user_data.json') else page.go("/user_data"),
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=ft.colors.BLUE,
        ),
    )

    return ft.Row(
        controls=[
            # "Tienda 3D" a la izquierda
            ft.Container(
                content=ft.Text("Tienda 3D", style="headlineMedium"),
                alignment=ft.alignment.center_left,
                expand=1,
            ),

            # Botones en el centro
            ft.Row(
                controls=[
                    home_button,
                    cart_button,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                expand=2,
            ),

            # Contador de la cesta y botón de perfil a la derecha
            ft.Row(
                controls=[
                    cart_count_text,  # Contador a la izquierda del perfil
                    user_button,  # Botón de perfil
                ],
                alignment=ft.MainAxisAlignment.END,
                expand=1,
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )
