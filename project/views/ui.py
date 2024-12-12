import flet as fl


def item_ui(page: fl.Page, items):
    main_column = fl.Column(spacing=10)

    page.snack_bar = fl.SnackBar(content=fl.Text("Hello, world!"), action="Alright!")

    def item_pulsado(e):
        button = e.control
        item_data = button.data
        item_title = item_data["title"]

        if button.text == "+":
            button.text = "-"
            action = "añadido"
        else:
            button.text = "+"
            action = "removido"

        page.snack_bar = fl.SnackBar(fl.Text(f"Producto {item_title} ha sido {action}"))
        page.update()

    row = fl.Row(spacing=10)
    for obj in items:
        item = fl.Container(
            width=220,
            height=250,
            border_radius=10,
            bgcolor=fl.colors.BLUE_GREY_50,
            padding=10,
            content=fl.Column(
                [
                    fl.Image(
                        src=obj.get_imagen(),
                        width=100,
                        height=100,
                        fit=fl.ImageFit.CONTAIN,
                    ),
                    fl.Text(
                        obj.get_titulo(),
                        weight=fl.FontWeight.BOLD,
                        size=12,
                        color=fl.colors.BLACK,
                    ),
                    fl.Text(
                        obj.get_descripcion(),
                        size=10,
                        color=fl.colors.GREY,
                    ),
                    fl.Container(expand=True),
                    fl.Container(
                        content=fl.ElevatedButton(
                            text="+",
                            on_click=item_pulsado,
                            data={"title": obj.get_titulo()},
                        ),
                        width=0.9 * 220,
                        alignment=fl.alignment.center,
                    ),
                ],
                spacing=10,
                alignment=fl.MainAxisAlignment.START,
                horizontal_alignment=fl.CrossAxisAlignment.CENTER,
            ),
        )
        row.controls.append(item)

        if len(row.controls) == 5:
            main_column.controls.append(row)
            row = fl.Row(spacing=10)

    if row.controls:
        main_column.controls.append(row)

    page.add(main_column)


def header(page: fl.Page):
    # Configuración inicial de la página
    page.title = "Impresionados 3D"
    page.theme_mode = fl.ThemeMode.LIGHT  # Comienza en modo claro
    page.scroll = "adaptive"
    page.padding = 10
    # Encabezado
    header = fl.Container(
        content=fl.Row(
            controls=[
                fl.Container(
                    fl.Image(src="logo.png", width=50),  # Reemplaza con tu logo
                    alignment=fl.alignment.center_left,
                    margin=fl.margin.only(right=10),
                ),
                fl.Text("IMPRESIONADOS 3D", size=20, weight=fl.FontWeight.BOLD, color="black"),
                fl.Container(
                    content=fl.TextField(
                        hint_text="Buscar...",
                        border_radius=fl.border_radius.all(20),
                        border_color="transparent",
                        filled=True,
                        fill_color="#AEEFFF",
                        content_padding=fl.Padding(15, 10, 15, 10),
                    ),
                    expand=True,
                    padding=fl.padding.only(left=15, right=15),
                ),
                fl.IconButton(fl.Icons.SEARCH, icon_size=20, tooltip="Buscar"),
                fl.Row(
                    controls=[
                        fl.ElevatedButton("Tienda", bgcolor="#AEEFFF", color="black"),
                        fl.ElevatedButton("Cesta", bgcolor="#AEEFFF", color="black"),
                        fl.ElevatedButton("Inicio sesión", bgcolor="#AEEFFF", color="black"),
                    ],
                    spacing=10,
                ),
            ],
            alignment="spaceBetween",
            height=80,
        ),
        bgcolor="#AEEFFF",  # Color de fondo del encabezado
        padding=fl.padding.symmetric(horizontal=15),
    )

    # Agregar el encabezado a la página
    page.add(header)
