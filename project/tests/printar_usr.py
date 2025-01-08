from project.models.mapeo_colecciones import *
from project.database.conection import conection
'''Este archivo solo contiene las funciones de select y delete de algún registro según su id'''

def select_usuario(id:int) -> object|None:
    """Select de usuario por id"""
    user = User.objects(_id = id).first()
    if user:
        print(f"Se encontró el usuario con id {id}")
        to_return = user
        print(user)
    else:
        print(f"No se encontró el usuario con id {id}")
        to_return = None
    return to_return
select_usuario(1)