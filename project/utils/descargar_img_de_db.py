from project.models.mapeo_colecciones import *
from project.database.conection import conection
import os


conection = conection()
# Asegúrate de que la carpeta donde guardarás las imágenes existe
os.makedirs("../imagens", exist_ok=True)


# Función para extraer y guardar la imagen
def descargar_imagen():
    for producto in Product.objects():
        if producto and producto.image:
            # Lee la imagen desde la base de datos
            with open(f"../imagens/producto_{producto._id}.jpg", "wb") as archivo_imagen:
                archivo_imagen.write(producto.image.read())
            print(f"Imagen descargada correctamente en './imagens/producto_{producto._id}.jpg'")
        else:
            print("No se encontró la imagen o el producto.")

if __name__ == "__main__":
    descargar_imagen()