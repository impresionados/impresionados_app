import flet as ft
from project.views.header import header, update_cart_count
from project.database.crud_entero import update_product
from paypalrestsdk import Payment, configure
import os
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

# Configurar PayPal con las credenciales del archivo .env
configure({
    "mode": "sandbox",  # Cambiar a "live" para producción
    "client_id": os.getenv("CLIENT_ID"),
    "client_secret": os.getenv("SECRET_KEY")
})

# Variable con la dirección
default_address = "Calle Falsa 123, Madrid, España"

# Función para calcular el total del carrito
def calcular_total(shopping_cart):
    return sum(product[0].price * product[1] for product in shopping_cart)

def compra_view(page, shopping_cart):
    # Opciones de pago
    payment_methods = ["Visa", "MasterCard", "PayPal"]
    selected_payment = ft.Dropdown(
        label="Selecciona un método de pago",
        options=[ft.dropdown.Option(text=method) for method in payment_methods],
        width=300
    )

    # Campos adicionales para tarjeta
    card_number = ft.TextField(label="Número de Tarjeta", width=300)
    expire_month = ft.TextField(label="Mes de Expiración", width=150)
    expire_year = ft.TextField(label="Año de Expiración", width=150)
    cvv2 = ft.TextField(label="CVV", width=100)
    first_name = ft.TextField(label="Nombre", width=300)
    last_name = ft.TextField(label="Apellido", width=300)
    address = ft.TextField(label="Dirección", value=default_address, width=300)

    # Mostrar el precio total
    total_price = calcular_total(shopping_cart)
    price_text = ft.Text(f"Total: {total_price:.2f}€", style="headlineSmall", color=ft.colors.GREEN_700)

    # Función para procesar pagos con PayPal
    def process_paypal_payment(amount):
        payment = Payment({
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "transactions": [{
                "amount": {"total": f"{amount:.2f}", "currency": "EUR"},
                "description": "Compra en la tienda 3D"
            }],
            "redirect_urls": {
                "return_url": "https://example.com/success",
                "cancel_url": "https://example.com/cancel"
            }
        })

        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    page.launch_url(link.href)
        else:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Error al procesar el pago con PayPal.", color=ft.colors.WHITE),
                bgcolor=ft.colors.RED_600,
            )
            page.snack_bar.open = True

    # Función para verificar el estado del pago con PayPal
    def check_paypal_payment(payment_id, payer_id):
        payment = Payment.find(payment_id)
        if payment.execute({"payer_id": payer_id}):
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Pago completado con éxito. 🎉", color=ft.colors.WHITE),
                bgcolor=ft.colors.GREEN_600,
            )
            page.snack_bar.open = True
            restar_stock(page, shopping_cart)
            shopping_cart.clear()
            page.go("/")
        else:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("El pago no se completó. Inténtalo nuevamente.", color=ft.colors.WHITE),
                bgcolor=ft.colors.RED_600,
            )
            page.snack_bar.open = True

    # Confirmar compra
    def confirm_purchase(e):
        if not shopping_cart:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Tu cesta está vacía.", color=ft.colors.WHITE),
                bgcolor=ft.colors.RED_600,
            )
            page.snack_bar.open = True
        elif not selected_payment.value:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Por favor, elige un método de pago.", color=ft.colors.WHITE),
                bgcolor=ft.colors.ORANGE_600,
            )
            page.snack_bar.open = True
        elif selected_payment.value in ["Visa", "MasterCard"]:
            if all([card_number.value, expire_month.value, expire_year.value, cvv2.value, first_name.value, last_name.value]):
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("¡Compra realizada con éxito! 🎉", color=ft.colors.WHITE),
                    bgcolor=ft.colors.GREEN_600,
                )
                page.snack_bar.open = True
                restar_stock(page, shopping_cart)
                shopping_cart.clear()
                page.go("/")
            else:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Por favor, completa todos los campos de la tarjeta.", color=ft.colors.WHITE),
                    bgcolor=ft.colors.RED_600,
                )
                page.snack_bar.open = True
        elif selected_payment.value == "PayPal":
            process_paypal_payment(total_price)

    # Confirmar stock
    def restar_stock(page, shopping_cart):
        for products in shopping_cart:
            product = products[0]
            quantity = products[1]
            product.stock -= quantity
            product.save()
        update_cart_count(page, shopping_cart)

    # Función para actualizar la vista según el método de pago seleccionado
    def update_payment_fields(e):
        page.controls.clear()
        fields = [
            header(page, shopping_cart),
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("Zona de Compra", style="headlineMedium", color=ft.colors.BLUE_GREY_900),
                        price_text,
                        address,
                        selected_payment,
                        ft.Divider(),
                    ], spacing=20, alignment=ft.MainAxisAlignment.CENTER),
                    padding=20,
                    border_radius=12,
                    bgcolor=ft.colors.WHITE,
                    alignment=ft.alignment.center,
                ),
                elevation=10,
            )
        ]

        if selected_payment.value in ["Visa", "MasterCard"]:
            fields[1].content.content.controls.extend([
                card_number,
                ft.Row([expire_month, expire_year, cvv2], spacing=10),
                first_name,
                last_name
            ])

        fields[1].content.content.controls.append(ft.ElevatedButton("Finalizar Compra", on_click=confirm_purchase))
        page.controls.extend(fields)
        page.update()

    # Detectar cambios en el método de pago seleccionado
    selected_payment.on_change = update_payment_fields

    # Mostrar la vista inicial
    update_payment_fields(None)
    page.update()
