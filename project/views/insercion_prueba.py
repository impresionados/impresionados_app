import mongoengine
from datetime import datetime
import random

from mapeo_colecciones import Product

# Conexión a la base de datos MongoDB en localhost
mongoengine.connect("impresionados_app" , host="mongodb+srv://impresionados:656UJjLTTcrEQNuQ@prueba.2hwb4.mongodb.net/?retryWrites=true&w=majority&appName=prueba")


# Función para insertar usuarios de prueba
def insert_users():
    for i in range(1, 6):
        mongoengine.connection.get_db().users.insert_one({
            "_id": i,
            "user_name": f"user_{i}",
            "email": f"user_{i}@example.com",
            "password": f"password_{i}",
            "registration_date": datetime.now()
        })
        print(f"User inserted: user_{i}")


# Función para insertar productos de prueba
def insert_products():
    for i in range(1, 6):
        mongoengine.connection.get_db().products.insert_one({
            "_id": i,
            "name": f"Product {i}",
            "description": f"Description of product {i}.",
            "price": round(random.uniform(10, 500), 2),
            "stock": random.randint(1, 100),
            "category": ["category1", "category2"],
            "ratings": []
        })
        print(f"Product inserted: Product {i}")




# Función para insertar valoraciones a productos
def insert_ratings():
    for i in range(1, 6):
        product = mongoengine.connection.get_db().products.find_one({"name": f"Product {i}"})
        # Insertar la valoración en el producto
        mongoengine.connection.get_db().products.update_one(
            {"_id": product["_id"]},
            {"$push": {
                "ratings": {
                    "user_id": str(i),  # ID del usuario que está dando la valoración
                    "rating": random.randint(1, 5),
                    "comment": f"Rating for product {i}.",
                    "date": datetime.now()
                }
            }}
        )
        print(f"Rating inserted for product: Product {i}")


# Función para insertar pedidos de prueba
def insert_orders():
    for i in range(1, 6):
        mongoengine.connection.get_db().orders.insert_one({
            "_id": i,
            "product_id": str(i),  # ID del producto
            "user_id": str(i),  # ID del usuario
            "date": datetime.now(),
            "total": round(random.uniform(10, 500), 2),
            "status": random.choice(["pending", "completed", "shipped"])
        })
        print(f"Order inserted for product: {i}")




# Insertar los datos de prueba
def insert_sample_data():
    # Insertar 5 usuarios
    # insert_users()

    # Insertar 5 productos
    insert_products()

    # Insertar 5 valoraciones
    # insert_ratings()
    #
    # # Insertar 5 pedidos
    # insert_orders()


# Llamar a la función para insertar los datos de prueba
insert_sample_data()
