# Impresionads3D App

## Descripción General
Impresionads3D App es una aplicación diseñada para ofrecer a los usuarios una experiencia fácil e intuitiva al comprar productos para impresoras 3D, productos creados con impresoras 3D e incluso las propias impresoras.

## Características Principales
- Cesta de compras
- Inicio y registro de sesión
- Integración con PayPal para pagos seguros
- Zona de compra
- Persistencia de datos con MongoDB

## Tecnologías Utilizadas
- Flet
- Git
- MongoDB
- Python

## Estructura del Proyecto
El proyecto se ejecuta desde el archivo `app.py` ubicado en la raíz del proyecto. La estructura de carpetas es la siguiente:
- `database`: Contiene la base de datos.
- `models`: Define las clases de los objetos utilizados para la base de datos.
- `tests`: Proyectos para desarrollo personal.
- `user`: Almacena de manera persistente los datos de usuario.
- `utils`: Utilidades usadas fuera de las views para el correcto funcionamiento de la app.
- `views`: Vistas utilizadas por Flet para la interfaz de usuario.

## Requisitos Previos
Para ejecutar este proyecto, necesitas tener instalado:
- Python (versión 3.10 o superior recomendada)
- Git
- MongoDB
- PostgreSQL

## Instalación
1. Clonar el repositorio:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   ```
2. Acceder al directorio del proyecto:
   ```bash
   cd impresionads3D-app
   ```
3. Crear un entorno virtual:
   ```bash
   python -m venv venv
   ```
4. Activar el entorno virtual:
   - En Windows: `venv\Scripts\activate`
   - En Linux/macOS: `source venv/bin/activate`

5. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
6. Configurar las variables de entorno (`.env`):
   ```plaintext
   CLIENT_ID=your_paypal_client_id
   SECRET_KEY=your_paypal_secret_key
   ```

7. Ejecutar la aplicación:
   ```bash
   python app.py
   ```

## Uso
Desde el menú principal, podrás registrarte para poder comprar productos de forma sencilla e intuitiva.

## Licencia
Este proyecto utiliza la licencia MIT, adecuada para la mayoría de proyectos de código abierto.

## Autor y Contacto
- [nicolasdavidgilbert](https://github.com/nicolasdavidgilbert)
- [ratioski](https://github.com/ratioski)
- [Zino243](https://github.com/Zino243)

