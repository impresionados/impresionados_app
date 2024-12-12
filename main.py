import os
import sys

# Agregar automáticamente el directorio raíz del proyecto al PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../.."))  # Ajusta según la estructura
if project_root not in sys.path:
    sys.path.insert(0, project_root)


if __name__ == "__main__":
    # aqui el from que necesitemos
    from project.utils.descargar_img_de_db import descargar_imagen
    descargar_imagen()