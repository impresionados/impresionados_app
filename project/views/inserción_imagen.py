
from mapeo_colecciones import *


# Conexión a la base de datos
mongoengine.connect("impresionados_app" , host="mongodb+srv://impresionados:656UJjLTTcrEQNuQ@prueba.2hwb4.mongodb.net/?retryWrites=true&w=majority&appName=prueba")

# Insertar el producto
def insertar_producto():
    for producto in Product.objects():
        try:
            # Cargar imagen desde un archivo binario
            with open("img/product_1.jpg", "rb") as imagen:
                producto.image.put(imagen, content_type='image/jpg')

            # Guardar en la base de datos
            producto.save()
            print(f"Imagen insertada correctamente para el producto con ID {producto._id}")
        except Exception as e:
            print(f"Error al insertar la imagen para el producto con ID {producto._id}: {e}")

insertar_producto()
