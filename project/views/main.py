import flet as ft

def main_page(page: ft.Page):
    # Configuración inicial de la página
    page.title = "Impresionados 3D"
    page.theme_mode = ft.ThemeMode.LIGHT  # Comienza en modo claro
    page.scroll = "adaptive"
    page.padding = 10
    # Encabezado
    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    ft.Image(src="logo.png", width=50),  # Reemplaza con tu logo
                    alignment=ft.alignment.center_left,
                    margin=ft.margin.only(right=10),
                ),
                ft.Text("IMPRESIONADOS 3D", size=20, weight=ft.FontWeight.BOLD, color="black"),
                ft.Container(
                    content=ft.TextField(
                        hint_text="Buscar...",
                        border_radius=ft.border_radius.all(20),
                        border_color="transparent",
                        filled=True,
                        fill_color="#AEEFFF",
                        content_padding=ft.Padding(15, 10, 15, 10),
                    ),
                    expand=True,
                    padding=ft.padding.only(left=15, right=15),
                ),
                ft.IconButton(ft.Icons.SEARCH, icon_size=20, tooltip="Buscar"),
                ft.Row(
                    controls=[
                        ft.ElevatedButton("Tienda", bgcolor="#AEEFFF", color="black"),
                        ft.ElevatedButton("Cesta", bgcolor="#AEEFFF", color="black"),
                        ft.ElevatedButton("Inicio sesión", bgcolor="#AEEFFF", color="black"),
                    ],
                    spacing=10,
                ),
            ],
            alignment="spaceBetween",
            height=80,
        ),
        bgcolor="#AEEFFF",  # Color de fondo del encabezado
        padding=ft.padding.symmetric(horizontal=15),
    )

    # Estructura principal de la página
    page.add(ft.Column(controls=[header], expand=True))

ft.app(target=main_page)
