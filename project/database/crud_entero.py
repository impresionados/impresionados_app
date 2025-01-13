import mongoengine
from datetime import datetime
from project.database.conection import conection
from project.models.mapeo_colecciones import *
import os

# -----------------------------
# CRUD FUNCTIONS FOR USERS
# -----------------------------
def create_user(user_name: str, email: str, password: str) -> User:
    """
    Crea un nuevo usuario y lo guarda en la base de datos.
    Verifica si el correo ya está registrado.

    :param user_name: Nombre del usuario
    :param email: Correo electrónico del usuario
    :param password: Contraseña del usuario
    :return: El objeto User creado o False si el correo ya está registrado
    """
    users_collection = mongoengine.get_db()['users']
    if users_collection.find_one({"email": email}):
        print("El correo ya está registrado.")
        return False
    user = User(
        user_name=user_name,
        email=email,
        password=password,
        registration_date=datetime.now()
    )
    user.save()
    print(f"Usuario {user_name} insertado correctamente")
    return user


def get_user_by_email(user_email: str) -> User:
    """
    Obtiene un usuario por su correo electrónico.

    :param user_email: Correo electrónico del usuario
    :return: El objeto User encontrado o None si no existe
    """
    return User.objects(email=user_email).first()


def update_user(user_email: str, **kwargs) -> User:
    """
    Actualiza los campos de un usuario existente.

    :param user_email: ID del usuario a actualizar
    :param kwargs: Campos a actualizar
    :return: El objeto User actualizado o None si no existe
    """
    user = User.objects(email=user_email).first()
    if user:
        user.update(**kwargs)
        return User.objects(email=user_email).first()
    return None


def delete_user(user_email: str) -> bool:
    """
    Elimina un usuario por su ID.

    :param user_email: email del usuario a eliminar
    :return: True si se eliminó, False si no existe
    """
    user = User.objects(email=user_email).first()
    if user:
        user.delete()
        return True
    return False


# -----------------------------
# CRUD FUNCTIONS FOR PRODUCTS
# -----------------------------
def create_product(name: str, description: str, price: float,
                   stock: int, category: list, img:str) -> Product:
    """
    Crea un nuevo producto y lo guarda en la base de datos.

    :param _id: ID del producto
    :param name: Nombre del producto
    :param description: Descripción del producto
    :param price: Precio del producto
    :param stock: Cantidad disponible en inventario
    :param category: Lista de categorías del producto
    :return: El objeto Product creado
    """
    with open(img, 'rb') as image_file:
        product = Product(
            name=name,
            description=description,
            price=price,
            stock=stock,
            category=category,
            image=image_file
        )
    product.save()
    print(f"Producto {name} insertado correctamente")
    return product


def save_product_image(product, folder_path: str):
    """
    Guarda la imagen del producto localmente en una carpeta específica.

    :param product: Objeto Product
    :param folder_path: Ruta de la carpeta donde se guardará la imagen
    """
    try:
        if product.image:  # Verifica si el producto tiene una imagen
            image_path = os.path.join(folder_path, f"{product.id}.jpg")
            with open(image_path, "wb") as img_file:
                img_file.write(product.image.read())
    except Exception as e:
        print(f"Error al guardar la imagen del producto {product.id}: {e}")


def get_product(product_id: str = "", category_list: list[str] = [], discard: bool = True) -> Product | mongoengine.QuerySet:
    """
    Obtiene un producto por su ID o todos los productos de la base de datos.

    :param product_id: ID del producto
    :param category_list: Lista de categorías a filtrar
    :param discard: Si es True, filtra por categorías; si es False, las descarta
    :return: El objeto Product encontrado o None si no existe
    """
    carpeta_imagenes = '../images'

    # Crear carpeta 'imagenes' si no existe
    if not os.path.exists(carpeta_imagenes):
        os.makedirs(carpeta_imagenes)

    if product_id == "":
        productos = Product.objects()  # Recupera todos los productos de la base de datos

        for producto in productos:
            if category_list:
                if discard:
                    if not set(producto.category) & set(category_list):
                        continue
                else:
                    if set(producto.category) & set(category_list):
                        continue

            save_product_image(producto, carpeta_imagenes)
        return productos
    else:
        producto = Product.objects(id=product_id).first()
        if producto:
            save_product_image(producto, carpeta_imagenes)
        return producto

def get_id_by_product(product):
    return product.id if product else None


def update_product(product_id: str, **kwargs) -> Product:
    """
    Actualiza los campos de un producto existente.

    :param product_id: ID del producto a actualizar
    :param kwargs: Campos a actualizar
    :return: El objeto Product actualizado o None si no existe
    """
    product = Product.objects(_id=product_id).first()
    if product:
        product.update(**kwargs)
        return Product.objects(_id=product_id).first()
    return None


def delete_product(product_id: str) -> bool:
    """
    Elimina un producto por su ID.

    :param product_id: ID del producto a eliminar
    :return: True si se eliminó, False si no existe
    """
    product = Product.objects(_id=product_id).first()
    if product:
        product.delete()
        return True
    return False


# -----------------------------
# CRUD FUNCTIONS FOR RATINGS
# -----------------------------
def create_rating(user_id: str, rating: int, comment: str) -> Rating:
    """
    Crea un nuevo rating.

    :param user_id: ID del usuario que deja el rating
    :param rating: Puntuación del producto
    :param comment: Comentario del usuario
    :return: El objeto Rating creado
    """
    new_rating = Rating(
        user_id=user_id,
        rating=rating,
        comment=comment,
        date=datetime.now()
    )
    print(f"Reating insertado correctamente")
    return new_rating


def get_rating_details(rating: Rating) -> dict:
    """
    Obtiene los detalles de un rating.

    :param rating: Objeto Rating
    :return: Un diccionario con los detalles del rating
    """
    return {
        "user_id": rating.user_id,
        "rating": rating.rating,
        "comment": rating.comment,
        "date": rating.date
    }


def update_rating(rating: Rating, **kwargs) -> Rating:
    """
    Actualiza un rating existente.

    :param rating: Objeto Rating a actualizar
    :param kwargs: Campos a actualizar
    :return: El objeto Rating actualizado
    """
    if 'user_id' in kwargs:
        rating.user_id = kwargs['user_id']
    if 'rating' in kwargs:
        rating.rating = kwargs['rating']
    if 'comment' in kwargs:
        rating.comment = kwargs['comment']
    rating.date = datetime.now()

    return rating


def delete_rating(product: Product, rating: Rating) -> bool:
    """
    Elimina un rating de un producto.

    :param product: Objeto Product del que se eliminará el rating
    :param rating: Objeto Rating a eliminar
    :return: True si se eliminó, False si no existe
    """
    if rating in product.ratings:
        product.ratings.remove(rating)
        product.save()
        return True
    return False


# -----------------------------
# CRUD FUNCTIONS FOR ORDERS
# -----------------------------
def create_order(_id: int, product_id: str, user_id: str, total: float, status: str) -> Order:
    """
    Crea una nueva orden y la guarda en la base de datos.

    :param _id: ID de la orden
    :param product_id: ID del producto en la orden
    :param user_id: ID del usuario que realizó la orden
    :param total: Total de la orden
    :param status: Estado de la orden
    :return: El objeto Order creado
    """
    order = Order(
        #_id=_id,
        product_id=product_id,
        user_id=user_id,
        date=datetime.now(),
        total=total,
        status=status
    )
    order.save()
    print(f"Orden {_id} insertado correctamente")
    return order


def get_order_by_id(order_id: int) -> Order:
    """
    Obtiene una orden por su ID.

    :param order_id: ID de la orden
    :return: El objeto Order encontrado o None si no existe
    """
    return Order.objects(_id=order_id).first()


def update_order(order_id: int, **kwargs) -> Order:
    """
    Actualiza los campos de una orden existente.

    :param order_id: ID de la orden a actualizar
    :param kwargs: Campos a actualizar
    :return: El objeto Order actualizado o None si no existe
    """
    order = Order.objects(_id=order_id).first()
    if order:
        order.update(**kwargs)
        return Order.objects(_id=order_id).first()
    return None


def delete_order(order_id: int) -> bool:
    """
    Elimina una orden por su ID.

    :param order_id: ID de la orden a eliminar
    :return: True si se eliminó, False si no existe
    """
    order = Order.objects(_id=order_id).first()
    if order:
        order.delete()
        return True
    return False

# -----------------------------
# ADD COMMENT TO PRODUCT
# -----------------------------
def add_comment_to_product(product_id: int, user_id: str, rating: int, comment: str) -> bool:
    """
    Añade un comentario (rating) a un producto existente.

    :param product_id: ID del producto al que se añadirá el comentario
    :param user_id: ID del usuario que deja el comentario
    :param rating: Puntuación del producto
    :param comment: Comentario del usuario
    :return: True si el comentario se añadió correctamente, False si el producto no existe
    """
    product = get_product(product_id)
    if product:
        new_rating = create_rating(user_id, rating, comment)
        product.ratings.append(new_rating)
        product.save()
        return True
    print(f"Reating añadido a {product_id} insertado correctamente")
    return False


# -----------------------------
# GIVE IMAGE PRODUCT PATH
# -----------------------------

def obtener_imagen_producto_id(producto_id):
    """
    Abre la imagen de un producto basado en su _id.

    Args:
        producto_id (int): El ID del producto cuya imagen se quiere abrir.
    """
    try:
        ruta_imagen = f"../images/{producto_id}.jpg"
        if os.path.exists(ruta_imagen):
            return ruta_imagen
        else:
            print(f"No se encontró la imagen para el producto con ID {producto_id}.")
    except Exception as e:
        print(f"Error al abrir la imagen: {e}")