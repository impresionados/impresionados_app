from main import main_page
import flet as ft
def shop(page: ft.Page):
    items_list = []  # Lista para guardar los datos de los objetos
    header = main_page(ft.Page)
    # Función para manejar el clic en el botón de cada ítem
    def add_item_clicked(e):
        if e.control.text == "+":
            e.control.text = "-"
            e.control.bgcolor = ft.Colors.RED
            e.control.update()
            items_list.append("Datos del objeto")
        else:
            e.control.text = "+"
            e.control.bgcolor = ft.Colors.TEAL
            e.control.update()
            if items_list:
                items_list.pop()

        print(items_list)

    # Función para crear un ítem
    def create_item():
        return ft.Container(
            padding=ft.padding.all(10),
            bgcolor=ft.Colors.CYAN,
            border_radius=10,
            content=ft.Column(
                [
                    ft.Container(
                        height=100,
                        content=ft.Icon(
                            ft.Icons.IMAGE_OUTLINED, size=50, color=ft.Colors.BLACK
                        ),
                        alignment=ft.alignment.center,
                    ),
                    ft.Text(
                        "Descripción corta corta corta corta corta...",
                        color=ft.Colors.BLACK,
                        weight=ft.FontWeight.W_500,
                        size=12,
                    ),
                    ft.Container(
                        height=40,
                        content=ft.ElevatedButton(
                            text="+",
                            bgcolor=ft.Colors.TEAL,
                            color=ft.Colors.WHITE,
                            on_click=add_item_clicked,
                        ),
                        alignment=ft.alignment.center,
                    ),
                ]
            ),
        )

    # Crear una lista de ítems
    items = [create_item() for _ in range(20)]  # Generar 20 ítems para prueba

    # Uso de `GridView` para diseño responsivo
    grid = ft.GridView(
        expand=True,
        max_extent=250,  # Tamaño máximo de cada ítem
        spacing=10,  # Espaciado entre ítems
        run_spacing=10,  # Espaciado entre filas
        controls=items,  # Los ítems generados
    )
    page.add(ft.Column(controls=[header, grid], expand=True))

if __name__ == "__main__":
    ft.app(target=shop)