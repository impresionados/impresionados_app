from project.database.conection import conection
from mongoengine import get_db
from project.user.guardar_datos import crear_json

def autenticar(us)->bool:
    user_email, password = us

    # Acceder a la colección 'users'
    users_collection = get_db()['users']

    # Buscar el usuario
    user = users_collection.find_one({
        "email": str(user_email),
        "password": str(password)
    })
    if user:
        print("Usuario autenticado correctamente.")
        crear_json(user)
        return True
    else:
        print("Nombre de usuario o contraseña incorrectos.")
        return False

