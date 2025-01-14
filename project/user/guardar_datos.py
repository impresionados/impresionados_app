from project.models.mapeo_colecciones import User
import json
from project.database.conection import conection
import os
from mongoengine import get_db

import os
import json

def crear_json(user: dict):
    # Ruta del archivo JSON
    file_path = "user/user_data.json"

    # Crear el directorio si no existe
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Convertir valores del usuario a cadenas
    user["_id"] = str(user["_id"])
    user["registration_date"] = str(user["registration_date"])
    print("Usuario procesado:", user)

    # Sobrescribir el archivo JSON con el nuevo contenido
    with open(file_path, 'w') as json_file:
        json.dump(user, json_file, indent=4)
        print("Archivo user_data.json sobrescrito exitosamente.")

