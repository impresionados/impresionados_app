import flet as ft
import project.database.conection
from project.models.mapeo_colecciones import Product, Category
import os, shutil
from project.database.crud_entero import create_product, update_product, add_category, delete_category_by_name, get_category
import mongoengine

# Función para mostrar notificación temporal
def show_snackbar(page, message):
    page.snackbar = ft.SnackBar(ft.Text(message))
    page.snackbar.open = True  # Aseguramos que la snackbar esté visible
    page.update()

    # Después de 3 segundos, cerramos la snackbar
    page.snackbar.open = False
    page.update()

# Función para agregar un producto
def add_product(page, name, description, price, stock, categories, image):
    try:
        create_product(name, description, price, stock, list(categories), image.path if image else None)
        show_snackbar(page, f"Producto '{name}' creado correctamente.")
    except Exception as e:
        show_snackbar(page, f"Error al crear el producto: {str(e)}")

# Función para manejar la subida de imágenes
def upload_image(file_picker_result):
    if file_picker_result.files:
        image_file = file_picker_result.files[0]
        return image_file
    return None

# Función para cargar categorías desde la base de datos
def load_categories():
    try:
        categories = [cat.name for cat in Category.objects()]
        return categories
    except Exception as e:
        return []

# Función para cargar productos desde la base de datos
def load_products():
    try:
        products = Product.objects()
        return products
    except Exception as e:
        return []

# Función para actualizar un producto utilizando la función update_product
def update_product_in_db(page, product, name, description, price, stock, categories, image):
    # Verifica si se proporciona una nueva imagen y, en caso afirmativo, usa su ruta
    image_path = image.path if image and hasattr(image, 'path') else None

    try:
        # Actualiza el producto con los nuevos valores, manteniendo la imagen si no se cambia
        updated_product = update_product(product, image_path, name=name, description=description, price=price, stock=stock, category=categories)
        show_snackbar(page, f"Producto '{product.name}' actualizado correctamente.")
        return updated_product
    except Exception as e:
        show_snackbar(page, f"Error al actualizar el producto: {str(e)}")
        return None

# Crear la interfaz de Flet
def main(page):
    page.title = "Product Management"
    page.vertical_alignment = ft.MainAxisAlignment.START

    # Entradas de texto
    name_input = ft.TextField(label="Product Name")
    description_input = ft.TextField(label="Description", multiline=True)
    price_input = ft.TextField(label="Price", keyboard_type=ft.KeyboardType.NUMBER)
    stock_input = ft.TextField(label="Stock", keyboard_type=ft.KeyboardType.NUMBER)

    # Cargar categorías desde la base de datos
    categories = load_categories()
    selected_categories = []

    # Función para manejar la selección de categorías
    def toggle_category_selection(e, category):
        if e.control.value:
            selected_categories.append(category)
        else:
            selected_categories.remove(category)
        print("Categorías seleccionadas:", selected_categories)

    # Función para mostrar el diálogo de selección de categorías
    def show_category_dialog(e):
        page.dialog = ft.AlertDialog(
            title=ft.Text("Selecciona las categorías"),
            content=ft.Column(
                [
                    ft.Checkbox(
                        label=cat,
                        value=cat in selected_categories,
                        on_change=lambda e, cat=cat: toggle_category_selection(e, cat)
                    )
                    for cat in categories
                ],
                scroll=ft.ScrollMode.AUTO  # Habilitar scroll en la columna
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda _: close_dialog())
            ],
        )
        page.dialog.open = True
        page.update()

    # Función para cerrar el diálogo
    def close_dialog():
        page.dialog.open = False
        page.update()

    # Botón para abrir el diálogo de selección de categorías
    category_dropdown_button = ft.ElevatedButton(
        text="Seleccionar categorías",
        on_click=show_category_dialog,
    )

    # Mostrar las categorías seleccionadas
    selected_text = ft.Text(value="Categorías seleccionadas: Ninguna")

    # Función para actualizar el texto de las categorías seleccionadas
    def update_selected_text():
        selected_text.value = f"Categorías seleccionadas: {', '.join(selected_categories) if selected_categories else 'Ninguna'}"
        page.update()

    # Botón para confirmar la selección de categorías
    confirm_button = ft.ElevatedButton(
        text="Confirmar categorías",
        on_click=lambda _: update_selected_text(),
    )

    # Crear el componente para seleccionar archivos
    def on_file_select(e):
        if e.files:
            selected_file = e.files[0]
            print(f"Archivo seleccionado: {selected_file.name}")
            global image_data
            image_data = upload_image(e)

    image_input = ft.FilePicker(on_result=on_file_select)

    # Botón para abrir el FilePicker
    save_button = ft.ElevatedButton("Guardar archivo", on_click=lambda _: image_input.pick_files())

    def show_snackbar(page, message):
        page.snack_bar = ft.SnackBar(ft.Text(message))  # Asegúrate de que SnackBar está asignado a la página
        page.snack_bar.open = True  # Abrir el SnackBar
        page.update()  # Actualizar la página para reflejar los cambios

    # Función para enviar el producto (Agregar o actualizar según el caso)
    def submit_product(e, product=None):
        # Si estamos editando un producto, mantenemos la imagen seleccionada
        image_to_use = image_data if image_data else product.image if product else None

        if not image_to_use and not product:
            show_snackbar(page, "Por favor selecciona una imagen antes de enviar el producto.")
            return

        # Si estamos editando un producto, lo actualizamos
        if product:
            updated_product = update_product_in_db(page, product, name_input.value, description_input.value, float(price_input.value), int(stock_input.value), selected_categories, image_to_use)
            if updated_product:
                show_snackbar(page, f"Producto '{product.name}' actualizado correctamente.")
                page.update()  # Asegúrate de que se actualiza la página
            else:
                show_snackbar(page, f"No se pudo actualizar el producto.")
                page.update()  # También aquí


        else:
            # Crear el producto si no es edición
            add_product(
                page,
                name_input.value,
                description_input.value,
                float(price_input.value),
                int(stock_input.value),
                selected_categories,
                image_to_use,
            )

    submit_button = ft.ElevatedButton("Add Product", on_click=submit_product)


    # Listado de productos
    products_list = ft.Column()
    products_list.controls = [
        ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        product.name,
                        weight=ft.FontWeight.BOLD,
                        size=16,
                        color=ft.Colors.BLUE_GREY_900,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        f"Precio: {product.price}€",
                        style="bodyMedium",
                        color=ft.Colors.GREEN_700,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        f"Stock: {product.stock}",
                        style="bodySmall",
                        color=ft.Colors.BLUE_GREY_600,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.IconButton(
                        icon=ft.Icons.EDIT,
                        icon_size=20,
                        tooltip="Editar producto",
                        icon_color=ft.Colors.BLUE_ACCENT,
                        on_click=lambda e, p=product: edit_product_dialog(p),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
            ),
            width=100,  # Ancho dinámico
            height=100,  # Alto dinámico
            padding=10,
            margin=10,
            alignment=ft.alignment.center,
            border_radius=12,
            bgcolor=ft.Colors.BLUE_GREY_50,

        )
        for product in load_products()
    ]
    page.update()

    # Configura un listener para detectar el cambio de tamaño de ventana
    def on_resized(e):
        # Actualiza las dimensiones de las tarjetas al cambiar el tamaño de la ventana
        width = 100
        height = 100
        for control in products_list.controls:
            control.width = width
            control.height = height
        page.update()

    page.on_resized = on_resized  # Vincula el evento de redimensionamiento

    def update_products_list():
        products = load_products()
        products_list.controls = [
            ft.Row([
                ft.Text(f"{product.name}"),
                ft.IconButton(
                    icon=ft.Icons.EDIT,
                    on_click=lambda e, product=product: edit_product_dialog(product),
                )
            ])
            for product in products
        ]
        page.update()

    # Función para mostrar el diálogo de edición de productos
    def edit_product_dialog(product):
        selected_categories[:] = product.category
        name_input.value = product.name
        description_input.value = product.description
        price_input.value = str(product.price)
        stock_input.value = str(product.stock)
        update_selected_text()

        # Mantenemos la imagen asociada al producto
        global image_data
        image_data = None  # No pedimos una nueva imagen en este momento

        submit_button.on_click = lambda e: submit_product(e, product)  # Enviar el producto con la imagen actual

        page.update()

    # Función para agregar una nueva categoría
    def add_new_category(e):
        new_category_name = category_name_input.value
        if new_category_name:
            try:
                add_category(new_category_name)
                show_snackbar(page, f"Categoría '{new_category_name}' agregada correctamente.")
                categories.append(new_category_name)
                category_name_input.value = ""  # Limpiar el campo
                page.update()
            except ValueError as err:
                show_snackbar(page, f"Error al agregar la categoría: {str(err)}")

    category_name_input = ft.TextField(label="Nueva categoría")
    add_category_button = ft.ElevatedButton("Agregar Categoría", on_click=add_new_category)

    # Botón para actualizar el listado de productos
    load_products_button = ft.ElevatedButton(
        "Cargar productos",
        on_click=lambda _: update_products_list(),
    )

    # Layout
    # Layout modificado con agrupaciones más claras y scroll
    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Gestión de Productos", style="headlineLarge", weight="bold", color=ft.Colors.BLUE_700),
                    ft.Divider(),  # Línea divisoria para separar secciones
                    ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text("Información del Producto", style="titleMedium", color=ft.Colors.BLUE_600),
                                    name_input,
                                    description_input,
                                    price_input,
                                    stock_input,
                                ],
                                spacing=10,
                                expand=2,
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text("Categorías y Archivo", style="titleMedium", color=ft.Colors.BLUE_600),
                                    category_dropdown_button,
                                    selected_text,
                                    confirm_button,
                                    save_button,
                                    image_input,
                                ],
                                spacing=10,
                                expand=1,
                            )
                        ],
                        spacing=20,
                    ),
                    submit_button,
                    load_products_button,
                    ft.Divider(),  # Línea divisoria para la sección de productos
                    ft.Text("Lista de Productos", style="titleMedium", color=ft.Colors.BLUE_700),
                    ft.Container(
                        content=ft.GridView(
                            controls=products_list.controls,  # Usar la lista de productos como controles
                            runs_count=3,  # Tres productos por fila
                            spacing=10,  # Espaciado horizontal entre los productos
                            run_spacing=10,  # Espaciado vertical entre las filas
                            max_extent=300,  # Ancho máximo por tarjeta de producto
                        ),
                        expand=True,  # Permite que el contenedor crezca según el espacio disponible
                        height=800,  # Altura mayor del contenedor
                        padding=10,  # Añadir un poco de padding para mayor estética
                        alignment=ft.alignment.top_center,
                        # Alinear el contenido en la parte superior y centrado=ft.ScrollMode.AUTO,  # Scroll habilitado si excede la altura
                    ),

                    ft.Text("Agregar Categoría", style="titleMedium", color=ft.Colors.BLUE_700),
                    ft.Row(
                        controls=[
                            category_name_input,
                            add_category_button,
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=10,
                    ),
                ],
                spacing=20,
                scroll=ft.ScrollMode.AUTO,  # Habilita scroll en la columna principal
            ),
            padding=20,
            expand=True,
        )
    )


if __name__ == "__main__":
    image_data = None
    # Ejecutar la app
    ft.app(target=main)