from project.models.mapeo_colecciones import *
from project.database.conection import conection
'''Este archivo solo contiene las funciones de select y delete de algún registro según su id'''

def select_usuario(id:int) -> object|None:
    """Select de usuario por id"""
    user = User.objects(_id = id).first()
    if user:
        print(f"Se encontró el usuario con id {id}")
        to_return = user
    else:
        print(f"No se encontró el usuario con id {id}")
        to_return = None
    return to_return

def select_producto(id:int) -> object|None:
    """Select de productos por id"""
    product = Product.objects(_id = id).first()
    if product:
        print(f"Se encontró el producto con id {id}")
        to_return = product
    else:
        print(f"No se encontró el producto con id {id}")
        to_return = None
    return to_return

def select_pedido(id:int) -> object|None:
    """Select de pedidos por id"""
    order = Order.objects(_id = id).first()
    if order:
        print(f"Se encontró el pedido con id {id}")
        to_return = order
    else:
        print(f"No se encontró el pedido con id {id}")
        to_return = None
    return to_return

def delete_usuario(id: int) -> bool:
    """Elimina un usuario por su ID"""
    user = User.objects(_id=id).first()
    if user:
        user.delete()
        print(f"Usuario con ID {id} eliminado correctamente.")
        to_return = True
    else:
        print(f"No se encontró el usuario con ID {id}.")
        to_return = False
    return to_return


def delete_producto(id: int) -> bool:
    """Elimina un producto por su ID"""
    product = Product.objects(_id=id).first()
    if product:
        product.delete()
        print(f"Producto con ID {id} eliminado correctamente.")
        to_return = True
    else:
        print(f"No se encontró el producto con ID {id}.")
        to_return = False
    return to_return


def delete_pedido(id: int) -> bool:
    """Elimina un pedido por su ID"""
    order = Order.objects(_id=id).first()
    if order:
        order.delete()
        print(f"Pedido con ID {id} eliminado correctamente.")
        to_return = True
    else:
        print(f"No se encontró el pedido con ID {id}.")
        to_return = False
    return to_return
from project.database.conection import conection
from mongoengine import get_db

def registrar_usuario(data: dict) -> bool:
    """
    Función para registrar un usuario en la base de datos.
    Args:
        data (dict): Diccionario con los datos del usuario. Ejemplo:
                     {"usuario": "nombre", "email": "correo@example.com", "password": "contraseña123"}
    Returns:
        bool: True si el usuario se registra con éxito, False en caso contrario.
    """
    try:
        # Obtener la conexión a la colección 'users'
        users_collection = get_db()['users']

        # Verificar si el correo ya existe en la base de datos
        if users_collection.find_one({"email": data["email"]}):
            print("El correo ya está registrado.")
            return False
        else:
        # Insertar el nuevo usuario
            users_collection.insert_one({
                "usuario": data["usuario"],
                "email": data["email"],
                "password": data["password"]  
            })
            print("Usuario registrado correctamente.")
            return True
    except Exception as e:
        print(f"Error al registrar usuario: {e}")
        return False



