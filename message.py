import flet as ft
import requests

API_URL = "http://localhost:8001"  # URL de tu API

def main(page: ft.Page):
    page.title = "Agregar Producto"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Inputs
    name_input = ft.TextField(label="Nombre del Producto", autofocus=True)
    description_input = ft.TextField(label="Descripción")
    price_input = ft.TextField(label="Precio", keyboard_type=ft.KeyboardType.NUMBER)
    stock_input = ft.TextField(label="Stock", keyboard_type=ft.KeyboardType.NUMBER)

    # Dropdown de supertipos
    supertype_dropdown = ft.Dropdown(label="Supertipo", on_change=lambda e: load_categories(e.control.value))

    # Columna para categorías (se actualizará dinámicamente según el supertipo)
    category_checkboxes = ft.Column()

    # Variable para almacenar la imagen seleccionada
    image_file = None

    def handle_image_selection(e):
        nonlocal image_file
        if e.files:
            image_file = e.files[0]
            page.add(ft.Text(f"Imagen seleccionada: {image_file.name}"))

    image_picker = ft.FilePicker(on_result=handle_image_selection)
    image_button = ft.ElevatedButton("Seleccionar Imagen", on_click=lambda _: image_picker.pick_files())

    # Cargar supertipos
    def load_supertypes():
        try:
            response = requests.get(f"{API_URL}/super_type_all/")
            response.raise_for_status()
            supertypes = response.json()

            supertype_dropdown.options = [
                ft.dropdown.Option(text=st["name"], data=st["id"]) for st in supertypes
            ]
            page.update()
        except requests.exceptions.RequestException as e:
            page.add(ft.Text(f"Error cargando supertipos: {e}", color=ft.colors.RED))

    # Cargar categorías según el supertipo seleccionado
    def load_categories(supertype_name):
        try:
            # Obtener el ID del supertipo seleccionado
            selected_supertype = next((st for st in supertype_dropdown.options if st.text == supertype_name), None)
            if not selected_supertype:
                page.add(ft.Text(f"Error: Supertipo no encontrado.", color=ft.colors.RED))
                return
            supertype_id = selected_supertype.data

            response = requests.get(f"{API_URL}/type/by_super_type/?id_super_type={supertype_id}")
            response.raise_for_status()
            categories = response.json()

            if not isinstance(categories, list):
                page.add(ft.Text(f"Error en categorías. Respuesta: {categories}", color=ft.colors.RED))
                return

            # Crear checkboxes con los nombres de categorías
            category_checkboxes.controls.clear()
            category_checkboxes.controls.extend([ft.Checkbox(label=c["name"], data=c["id"]) for c in categories])

            page.update()
        except requests.exceptions.RequestException as e:
            page.add(ft.Text(f"Error cargando categorías: {e}", color=ft.colors.RED))

    load_supertypes()

    # Enviar datos
    def submit_form(e):
        name = name_input.value.strip()
        description = description_input.value.strip()
        try:
            price = float(price_input.value) if price_input.value else 0.0
            stock = int(stock_input.value) if stock_input.value else 0
        except ValueError:
            page.add(ft.Text("Error: Precio y stock deben ser números válidos", color=ft.colors.RED))
            return

        selected_categories = [c.data for c in category_checkboxes.controls if c.value]
        supertype_id = next((st.data for st in supertype_dropdown.options if st.text == supertype_dropdown.value), None)

        if not name or not supertype_id or not selected_categories:
            page.add(ft.Text("Error: Todos los campos son obligatorios.", color=ft.colors.RED))
            return

        # Manejo del archivo de imagen
        files = {}
        if image_file:
            try:
                with open(image_file.path, "rb") as f:
                    files["image"] = (image_file.name, f.read(), "image/jpeg")  # Asegurar MIME correcto
            except Exception as ex:
                page.add(ft.Text(f"Error cargando imagen: {ex}", color=ft.colors.RED))
                return

        data = {
            "name": name,
            "description": description,
            "price": price,
            "stock": stock,
            "categories": selected_categories,
            "supertype": supertype_id
        }

        try:
            response = requests.post(f"{API_URL}/products/", json=data, files=files)
            if response.status_code == 201:  # 201 indica creación exitosa
                page.add(ft.Text("Producto creado exitosamente", color=ft.colors.GREEN))
            else:
                page.add(ft.Text(f"Error: {response.text}", color=ft.colors.RED))
        except requests.exceptions.RequestException as e:
            page.add(ft.Text(f"Error enviando datos: {e}", color=ft.colors.RED))

    submit_button = ft.ElevatedButton("Crear Producto", on_click=submit_form)

    page.add(name_input, description_input, price_input, stock_input, supertype_dropdown, category_checkboxes, image_picker, image_button, submit_button)

ft.app(target=main)
