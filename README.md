# 1. Comandos básicos de configuración
### -  Crear el entorno virtual:
```py
python3 -m venv env
source env/bin/activate # Linux/Mac
env\Scripts\activate # Windows
```
----
### -  Instalar dependencias iniciales:
```py
pip install flet pymongo # una vez dentro del entorno se puede instalar asi las librerias
pip freeze > requirements.txt # asi guardamos las librerias que usamos en un archivo que compartimos
```
### -  Iniciar un repositorio Git:
```bash
git add .
git commit -m "Configuración inicial del proyecto"
git branch -M main
git remote add origin <url_del_repositorio>
git push -u origin main
```
### -  Crear estructura de carpetas:
```bash
# si no existiera la estructura
mkdir -p project/{models,views,controllers,database,utils,tests}
touch project/main.py project/requirements.txt
```
### -  Estructura del proyecto
```
project/
--- models/                 # Modelos de datos (MongoDB)
\ --- user.py               # Ejemplo: Modelo de usuario
--- views/                  # Interfaces gráficas (Flet)
\ --- main_view.py          # Ejemplo: Pantalla principal
--- controllers/            # Lógica de negocio
\ --- user_controller.py    # Ejemplo: Controlador de usuario
--- database/               # Configuración de MongoDB
\ --- config.py             # Ejemplo: Configuración de conexión
--- utils/                  # Utilidades y funciones comunes
--- tests/                  # Pruebas unitarias y de integración
--- requirements.txt        # Dependencias del proyecto
--- main.py                 # Punto de entrada
```
# Código básico inicial
### -  - Configuración de la base de datos
```py
from pymongo import MongoClient
def get_database():
    client = MongoClient("mongodb://localhost:27017/")
    return client["nombre_proyecto"]
db = get_database()
```
### -  Modelo de usuario
```py
from database.config import db
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
    def save(self):
        db.users.insert_one({"name": self.name, "email": self.email})
    @staticmethod
    def get_all():
        return list(db.users.find({}))
```
### -  Interfaz gráfica con Flet
```py
import flet as ft
from controllers.user_controller import UserController
def main_view(page: ft.Page):
    page.title = "Gestión de usuarios"
    name_field = ft.TextField(label="Nombre")
    email_field = ft.TextField(label="Correo")
    result = ft.Text()
def save_user(e):
    UserController.create_user(name_field.value, email_field.value)
    result.value = "Usuario guardado"
    page.update()
    page.add(
        name_field,
        email_field,
        ft.ElevatedButton("Guardar", on_click=save_user),
        result,
    )
```
### -  Controlador de usuario
```py
from models.user import User
class UserController:
    @staticmethod
    def create_user(name, email):
        user = User(name, email)
        user.save()
```
### -  Archivo principal
```py
import flet as ft
from views.main_view import main_view
if __name__ == "__main__":
    ft.app(target=main_view)
```
# Flujo de trabajo en equipo
### -  Trabajar en ramas con Git:
```bash
git checkout -b feature/nombre_funcionalidad
```
### -  Subir cambios:
```
git add .
git commit -m "Implementación de funcionalidad X"
git push origin feature/nombre_funcionalidad
```
### -  Crear un pull request para revisión antes de fusionar en la rama principal.