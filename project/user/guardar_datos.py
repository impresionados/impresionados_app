from project.models.mapeo_colecciones import User
import json
from project.database.conection import conection

from mongoengine import get_db

def crear_json(user:dict):
    user["_id"] = str(user["_id"])
    user["registration_date"] = str(user["registration_date"])
    print(user)
    # Guardar en un archivo JSON
    with open('user/user_data.json', 'w') as json_file:
        json.dump(user, json_file, indent=4)

    print("Archivo user_data.json creado exitosamente.")
