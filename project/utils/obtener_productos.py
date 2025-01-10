import os
from mongoengine import QuerySet
from project.models.mapeo_colecciones import Product
from project.database.conection import conection

def obtener_productos() -> QuerySet:
    """
    Obtiene todos los productos de la base de datos y guarda sus imágenes en la carpeta 'imagenes'.

    Returns:
        QuerySet: Un conjunto de productos almacenados en la base de datos.
    """
    try:
        productos = Product.objects()  # Recupera todos los productos de la base de datos

        # Crear carpeta 'imagenes' si no existe
        carpeta_imagenes = '../imagens'
        if not os.path.exists(carpeta_imagenes):
            os.makedirs(carpeta_imagenes)

        # Guardar imágenes localmente con el nombre basado en el _id
        for producto in productos:
            if producto.image:  # Verifica si el producto tiene una imagen
                with open(f"{carpeta_imagenes}/{producto.id}.jpg", "wb") as img_file:
                    img_file.write(producto.image.read())  # Guarda la imagen con el nombre del ID

        return productos

    except Exception as e:
        print(f"Error al obtener los productos: {e}")
        return []


def obtener_producto_por_id(productos, producto_id):
    """
    Obtiene un producto de una lista por su _id.

    Args:
        productos (QuerySet): La lista de productos previamente obtenida.
        producto_id (int): El ID del producto a buscar.

    Returns:
        Product | None: El producto encontrado o None si no se encuentra.
    """
    try:
        for producto in productos:
            if producto.id == producto_id:
                return producto
        print(f"Producto con ID {producto_id} no encontrado.")
        return None
    except Exception as e:
        print(f"Error al buscar el producto: {e}")
        return None


def obtener_imagen_producto_id(producto_id):
    """
    Abre la imagen de un producto basado en su _id.

    Args:
        producto_id (int): El ID del producto cuya imagen se quiere abrir.
    """
    try:
        ruta_imagen = f"../imagens/{producto_id}.jpg"
        if os.path.exists(ruta_imagen):
            return ruta_imagen
        else:
            print(f"No se encontró la imagen para el producto con ID {producto_id}.")
    except Exception as e:
        print(f"Error al abrir la imagen: {e}")


if __name__ == "__main__":
    # Obtener productos y guardarlos en la carpeta 'imagenes'
    productos = obtener_productos()

    if productos:
        print("Productos encontrados:")
        for producto in productos:
            print(f"Nombre: {producto.name}")
            print(f"Descripción: {producto.description}")
            print(f"Precio: {producto.price}")
            print(f"Stock: {producto.stock}")
            print(f"Categoría(s): {', '.join(producto.category)}")
            print(f"Imagen guardada como: imagens/{producto._id}.jpg")
            print("-" * 40)

        # Prueba para buscar un producto por su ID y abrir su imagen
        producto_id = int(input("Introduce un ID de producto para buscar y abrir su imagen: "))
        producto_encontrado = obtener_producto_por_id(productos, producto_id)

        if producto_encontrado:
            print(f"Producto encontrado: {producto_encontrado.name}")
            obtener_imagen_producto_id(producto_id)

    else:
        print("No se encontraron productos en la base de datos.")
