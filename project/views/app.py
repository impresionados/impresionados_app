import flet as fl
from project.views.object.Item import Item
from utils import get_images
from ui import item_ui, header


def app_layout(page: fl.Page, items):
    # Primero carga el header
    header(page)

    # Luego carga los ítems
    item_ui(page, items)


if __name__ == "__main__":
    items = []
    images = get_images()
    for i, img in enumerate(images):
        item = Item(i, f"titulo{i}", f"Descripcion{i}", img)
        items.append(item)

    # Ahora pasamos la función app_layout correctamente
    fl.app(target=lambda page: app_layout(page, items))
