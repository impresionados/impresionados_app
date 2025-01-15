import flet as ft
import project.database.conection
from project.models.mapeo_colecciones import Product, Category
import os, shutil
from project.database.crud_entero import create_product, add_category, delete_category_by_name, get_category
import mongoengine

# Función para agregar un producto
def add_product(page, name, description, price, stock, categories, image):
    try:
        create_product(name, description, price, stock, list(categories), image.path)
        page.add(ft.Text(f"Producto '{name}' creado"))
    except Exception as e:
        page.add(ft.Text(f"No se ha creado el producto: {str(e)}"))

# Función para manejar la subida de imágenes
def upload_image(file_picker_result):
    if file_picker_result.files:
        image_file = file_picker_result.files[0]
        return image_file
    return None

# Función para cargar categorías desde la base de datos
def load_categories():
    try:
        categories = [get_category(cat) for cat in Category.objects()]
        return categories
    except Exception as e:
        return []

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
                ]
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

    # Función para enviar el producto
    def submit_product(e):
        if not image_input:
            page.add(ft.Text("Please select an image before submitting the product."))
            return

        # Subir el producto con la imagen
        add_product(
            page,
            name_input.value,
            description_input.value,
            float(price_input.value),
            int(stock_input.value),
            selected_categories,
            image_data,
        )

    submit_button = ft.ElevatedButton("Add Product", on_click=submit_product)

    # Layout
    page.add(
        name_input,
        description_input,
        price_input,
        stock_input,
        category_dropdown_button,
        selected_text,
        confirm_button,
        save_button,
        image_input,
        submit_button,
    )

if __name__ == "__main__":
    image_data = None
    # Ejecutar la app
    ft.app(target=main)
