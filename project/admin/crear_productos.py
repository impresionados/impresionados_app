import flet as ft
import project.database.conection
from project.models.mapeo_colecciones import Product
import os, shutil
from project.database.crud_entero import create_product
# Función para agregar un producto
def add_product(page, name, description, price, stock, category, image):
    try:
        create_product(name, description, price, stock, list(category), image.path)
        page.add(ft.Text(f"Producto '{name}' creado"))
    except:
        page.add(ft.Text(f"no se ha creado el producto"))

# Función para manejar la subida de imágenes
def upload_image(file_picker_result):
    if file_picker_result.files:
        image_file = file_picker_result.files[0]  # Tomar el primer archivo
        # Guardar la imagen en MongoDB como un archivo binario
        return image_file  # Leemos el archivo como binario
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
    category_input = ft.TextField(label="Category (comma-separated)")
    ratings_input = ft.TextField(label="Ratings (comma-separated, score:comment)", multiline=True)

    def on_file_select(e):
        if e.files:
            selected_file = e.files[0]
            print(f"Archivo seleccionado: {selected_file.name}")
            # Asignar la imagen seleccionada
            global image_data
            image_data = upload_image(e)  # Guardar la imagen

    # Crear el componente para seleccionar archivos
    image_input = ft.FilePicker(on_result=on_file_select)

    def on_save_button_click(e):
        image_input.pick_files()  # Abrir el FilePicker para seleccionar el archivo

    save_button = ft.ElevatedButton("Guardar archivo", on_click=on_save_button_click)

    # Función para enviar el producto
    def submit_product(e):
        # # Procesar calificaciones
        # ratings = []
        # for rating_str in ratings_input.value.split(","):
        #     try:
        #         score, comment = rating_str.split(":")
        #         ratings.append(Rating(score=int(score), comment=comment))
        #     except ValueError:
        #         pass  # Handle any malformed rating input gracefully

        if not image_input:
            page.add(ft.Text("Please select an image before submitting the product."))
            return

        # Subir el producto con la imagen
        add_product(page, name_input.value, description_input.value, float(price_input.value),
                    int(stock_input.value), category_input.value, image_data)

    submit_button = ft.ElevatedButton("Add Product", on_click=submit_product)

    # Layout
    page.add(
        name_input, description_input, price_input, stock_input,
        category_input, save_button, image_input, submit_button
    )

if __name__ == "__main__":
    image_data = None
    # Ejecutar la app
    ft.app(target=main)
