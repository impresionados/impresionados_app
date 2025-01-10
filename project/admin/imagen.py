import flet as ft
import os
import shutil


# Función que se ejecuta cuando el usuario selecciona un archivo
def on_file_select(e):
    if e.files:
        selected_file = e.files[0]
        print(f"Archivo seleccionado: {selected_file.name}")

        # Guardar el archivo en una ruta del sistema
        save_file(selected_file)


# Función que guarda el archivo seleccionado en el sistema
def save_file(selected_file):
    try:
        # Definir la ruta donde se guardará el archivo (puedes personalizarla)
        save_path = os.path.join("saved_files", selected_file.name)

        # Crear el directorio si no existe
        if not os.path.exists("saved_files"):
            os.makedirs("saved_files")

        # Copiar el archivo desde la ubicación temporal a la ruta de destino
        shutil.copy(selected_file.path, save_path)  # Copiar el archivo utilizando su path

        print(f"Archivo guardado en: {save_path}")
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")


# Función que se ejecuta cuando el botón de guardar es presionado
def on_save_button_click(e):
    image_input.pick_files()  # Abrir el FilePicker para seleccionar el archivo


# Crear la página
def main(page: ft.Page):
    # Crear el FilePicker con el callback on_result
    global image_input
    image_input = ft.FilePicker(on_result=on_file_select)

    # Crear el botón para guardar el archivo
    save_button = ft.ElevatedButton("Guardar archivo", on_click=on_save_button_click)

    # Añadir los componentes a la página
    page.add(
        ft.Column([
            save_button,  # Botón para guardar archivo
            image_input,  # FilePicker
        ])
    )


# Ejecutar la aplicación Flet
ft.app(target=main)
