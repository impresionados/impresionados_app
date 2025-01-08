from project.database.conection import conection
from mongoengine import get_db

def autenticar(us)->bool:
    user_name, password = us

    # Acceder a la colección 'users'
    users_collection = get_db()['users']

    # Buscar el usuario
    user = users_collection.find_one({
        "user_name": str(user_name),
        "password": str(password)
    })
    if user:
        print("Usuario autenticado correctamente.")
        return True
    else:
        print("Nombre de usuario o contraseña incorrectos.")
        return False





