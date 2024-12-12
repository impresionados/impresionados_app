class Item():
    def __init__(self, id, titulo, descripcion, imagen):
        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion
        self.imagen = imagen


    def get_id(self):
        return self.id

    def get_titulo(self):
        return self.titulo

    def get_descripcion(self):
        return self.descripcion

    def get_imagen(self):
        return self.imagen

    def __str__(self):
        return f"ID: {self.id}, Título: {self.titulo}, Descripción: {self.descripcion} img {self.imagen}"