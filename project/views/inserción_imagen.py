from mapeo_colecciones import *
import mongoengine


# Conexión a la base de datos

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
