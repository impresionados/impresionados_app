import mongoengine


class User(mongoengine.Document):
    meta = {'collection': 'users'}  # To specify the collection being mapped

    _id = mongoengine.IntField(required=True)
    user_name = mongoengine.StringField(required=True)
    email = mongoengine.StringField(required=True)
    password = mongoengine.StringField(required=True)
    registration_date = mongoengine.DateTimeField(required=True)

    def __str__(self):
        return (
            f"ID: {self._id}\n"
            f"Nombre de usuario: {self.user_name}\n"
            f"Email: {self.email}\n"
            f"Contraseña: {self.password}\n"
            f"Fecha de registro: {self.registration_date.strftime('%Y-%m-%d %H:%M:%S')}\n"
        )
class Rating(mongoengine.EmbeddedDocument):  # To specify that it is inside another class
    user_id = mongoengine.StringField(required=True)
    rating = mongoengine.IntField(required=True)
    comment = mongoengine.StringField()
    date = mongoengine.DateTimeField(required=True)


class Product(mongoengine.Document):
    meta = {'collection': 'products'}

    _id = mongoengine.IntField(required=True)
    name = mongoengine.StringField(required=True)
    description = mongoengine.StringField()
    price = mongoengine.FloatField(required=True)
    stock = mongoengine.IntField(required=True)
    category = mongoengine.ListField(mongoengine.StringField())  # List of strings
    image = mongoengine.FileField()
    ratings = mongoengine.ListField(mongoengine.EmbeddedDocumentField(Rating))  # It will be a list of Rating objects


class Order(mongoengine.Document):
    meta = {'collection': 'orders'}

    _id = mongoengine.IntField(required=True)
    product_id = mongoengine.StringField(required=True)
    user_id = mongoengine.StringField(required=True)
    date = mongoengine.DateTimeField(required=True)
    total = mongoengine.FloatField(required=True)
    status = mongoengine.StringField(required=True)
