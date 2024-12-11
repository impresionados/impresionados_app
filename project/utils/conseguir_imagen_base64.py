from project.models.mapeo_colecciones import *
import base64

# Este archivo recupera una imágen de un producto según su id sin necesidad de gaurdala localmente


def obtener_imagen_base64(id) -> base64 or None:
    producto = Product.objects(_id=id).first()
    if producto and producto.image:
        # Leer la imagen como bytes
        image_bytes = producto.image.read()
        # Convertir a base64
        print("Imágen recuperada en base 64")
        return base64.b64encode(image_bytes).decode('utf-8')
    else:
        print(f"No se encontró imagen para el producto con ID {id}.")
        return None


######################################################################################################
######################################################################################################
# Para que la imágen se vea en el flet deben de existir las siguientes líneas
#   image_base64 = obtener_imagen_base64(product_id)
#   if image_base64:
#       image_data_url = f"data:image/jpeg;base64,{image_base64}"
#       img = ft.Image(src=image_data_url, width=300, height=300)
#       page.add(img)
######################################################################################################
######################################################################################################
