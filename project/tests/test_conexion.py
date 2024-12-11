from project.database.conection import conection
import mongoengine

# Llamar a la función conection
db_connection = conection()

if db_connection:
    try:
        print('a')
        # Obtener el objeto de la base de datos
        db = mongoengine.get_db()
        print('b')
        # Listar colecciones de la base de datos
        collections = db.list_collection_names()
        print("Colecciones en la base de datos:", collections)
    except Exception as e:
        print("Error al interactuar con la base de datos:", str(e))
else:
    print("No se pudo establecer la conexión con la base de datos.")
