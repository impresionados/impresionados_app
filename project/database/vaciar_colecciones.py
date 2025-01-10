import mongoengine
from datetime import datetime
from project.models.mapeo_colecciones import *
from project.database.conection import conection



# -----------------------------
# FUNCION PARA ELIMINAR TODOS LOS REGISTROS DE UNA COLECCIÓN
# -----------------------------
def clear_collection(collection_name: str) -> None:
    """
    Elimina todos los registros de una colección específica en la base de datos.

    :param collection_name: Nombre de la colección a vaciar
    """
    db = mongoengine.get_db()
    result = db[collection_name].delete_many({})
    print(f"Se eliminaron {result.deleted_count} documentos de la colección '{collection_name}'")

clear_collection("orders")
clear_collection("products")
clear_collection("users")