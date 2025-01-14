from logging import exception

import mongoengine
from datetime import datetime
from project.models.mapeo_colecciones import *
from project.database.conection import conection
from project.database.crud_entero import *

# -----------------------------
# INSERT EXAMPLES FOR USERS
# -----------------------------

create_user("JohnDoe", "john@example.com", "password123")
create_user( "JaneDoe", "jane@example.com", "password456")
create_user( "AliceSmith", "alice@example.com", "password789")
create_user( "BobBrown", "bob@example.com", "password321")
create_user( "CharlieWhite", "charlie@example.com", "password654")

# -----------------------------
# INSERT EXAMPLES FOR PRODUCTS
# -----------------------------
create_product("Laptop", "High-end gaming laptop", 1500.00, 10, ["Electronics"], "../../imagens/img_1.jpeg")
create_product("Smartphone", "Latest model smartphone", 800.00, 20, ["Electronics"], "../../imagens/img_2.jpeg")
create_product("Headphones", "Noise-cancelling headphones", 200.00, 30, ["Accessories"], "../../imagens/img_3.jpeg")
create_product("Smartwatch", "Feature-rich smartwatch", 250.00, 15, ["Wearables"], "../../imagens/img_4.jpeg")
create_product("Camera", "Professional DSLR camera", 1200.00, 5, ["Photography"], "../../imagens/img_5.jpeg")

# -----------------------------
# INSERT EXAMPLES FOR ORDERS
# -----------------------------
create_order(1, "1", "1", 1500.00, "Processing")
create_order(2, "2", "2", 800.00, "Shipped")
create_order(3, "3", "3", 200.00, "Delivered")
create_order(4, "4", "4", 250.00, "Processing")
create_order(5, "5", "5", 1200.00, "Cancelled")

# -----------------------------
# INSERT EXAMPLES FOR RATINGS
# -----------------------------
add_comment_to_product(1, "1", 5, "Amazing laptop, highly recommend!")
add_comment_to_product(2, "2", 5, "Best headphones I've ever used.")
add_comment_to_product(3, "3", 5, "Best headphones I've ever used.")
add_comment_to_product(4, "4", 4, "Nice smartwatch with many features.")
add_comment_to_product(5, "5", 5, "Incredible camera for professionals.")




