import mongoengine
import os
from project.models.mapeo_colecciones import User
# Conexión a la base de datos MongoDB
def connect_db():
    mongoengine.connect(
        db="impresionados_app",
        host=f"mongodb+srv://impresionados:{os.getenv('DATABASE_PASSWORD')}@prueba.2hwb4.mongodb.net/?retryWrites=true&w=majority&appName=prueba"
    )
# Función para obtener los datos del usuario por su ID
def get_user_by_id(user_id: int):
    # Asegúrate de que la base de datos está conectada
    connect_db()

    # Buscar el usuario por su ID
    user = User.objects(_id=user_id).first()  # Usamos el campo '_id' para buscar el usuario

    return user
