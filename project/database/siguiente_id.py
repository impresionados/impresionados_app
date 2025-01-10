import mongoengine
from datetime import datetime
from project.models.mapeo_colecciones import *
from project.database.conection import conection


def get_next_id(counter_name: str) -> int:
    """
    Obtiene el siguiente ID disponible de manera autoincremental para una colección específica.
    Utiliza una colección de contadores en la base de datos para llevar el control.

    :param counter_name: Nombre del contador (ej: 'user_id', 'product_id', 'order_id')
    :return: El siguiente ID autoincremental
    """
    counters_collection = mongoengine.get_db()['counters']
    counter = counters_collection.find_one_and_update(
        {'_id': counter_name},
        {'$inc': {'seq': 1}},
        upsert=True,
        return_document=True
    )
    return counter['seq']


next_user_id = get_next_id('user_id')
print(f"El siguiente ID de usuario es: {next_user_id}")

# Obtener el siguiente ID para productos
next_product_id = get_next_id('product_id')
print(f"El siguiente ID de producto es: {next_product_id}")

# Obtener el siguiente ID para órdenes
next_order_id = get_next_id('order_id')
print(f"El siguiente ID de orden es: {next_order_id}")