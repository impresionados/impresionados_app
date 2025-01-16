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
# Función para calcular el total del carrito
def calcular_total(shopping_cart):
    return sum(product[0].price * product[1] for product in shopping_cart)

def compra_view(page, shopping_cart):
    # Opciones de pago
    payment_methods = ["Visa", "MasterCard", "PayPal"]
    selected_payment = ft.Dropdown(
        label="Selecciona un método de pago",
        value="PayPal",
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
    address = ft.TextField(label="Dirección", width=300)

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

    def show_snack_bar(message):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color=ft.colors.WHITE),
            bgcolor=ft.colors.RED_600,
        )
        page.snack_bar.open = True
        page.update()

    # Confirmar compra
    def confirm_purchase(e):
        # Verificar si el carrito está vacío
        if not shopping_cart:
            show_snack_bar("Tu cesta está vacía")

        # Verificar si la dirección está vacía
        elif not address.value or not address.value.strip():
            show_snack_bar("Por favor, ponga una dirección.")


        # Verificar si no se seleccionó un método de pago
        elif not selected_payment.value:
            show_snack_bar("Por favor, elige un método de pago.")

        # Validar campos de tarjeta de crédito
        elif selected_payment.value in ["Visa", "MasterCard"]:
            if all([card_number.value, expire_month.value, expire_year.value, cvv2.value, first_name.value,
                    last_name.value]):
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("¡Compra realizada con éxito! 🎉", color=ft.colors.WHITE),
                    bgcolor=ft.colors.GREEN_600,
                )
                page.snack_bar.open = True
                page.update()

                restar_stock(page, shopping_cart)
                shopping_cart.clear()
                page.go("/")
            else:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Por favor, completa todos los campos de la tarjeta.", color=ft.colors.WHITE),
                    bgcolor=ft.colors.RED_600,
                )
                page.snack_bar.open = True
                page.update()

        # Procesar pago con PayPal
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

        # Agregar el header en la parte superior
        page.add(
            header(page, shopping_cart),
            ft.Container(
                content=ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            controls=[
                                # Título en la parte superior
                                ft.Container(
                                    content=ft.Text(
                                        "Zona de Compra",
                                        style="headlineMedium",
                                        color=ft.colors.BLUE_GREY_900,
                                        weight="bold"
                                    ),
                                    alignment=ft.alignment.top_center,
                                ),
                                # Contenido principal dentro de una lista scrollable
                                ft.ListView(
                                    controls=[
                                        price_text,
                                        address,
                                        selected_payment,
                                        ft.Divider(height=1, thickness=1, color=ft.colors.BLUE_GREY_100),
                                        # Campos adicionales si es tarjeta
                                        *(
                                            [
                                                card_number,
                                                ft.Row([expire_month, expire_year, cvv2], spacing=10),
                                                first_name,
                                                last_name
                                            ] if selected_payment.value in ["Visa", "MasterCard"] else []
                                        ),
                                        # Botón de finalizar compra
                                        ft.ElevatedButton(
                                            "Finalizar Compra",
                                            icon=ft.icons.CHECK,
                                            bgcolor=ft.colors.GREEN_600,
                                            color=ft.colors.WHITE,
                                            on_click=confirm_purchase
                                        )
                                    ],
                                    spacing=20,
                                    expand=True,  # Permite que el contenido ocupe el espacio restante
                                )
                            ],
                            spacing=20,
                            alignment=ft.MainAxisAlignment.START,  # Título arriba
                        ),
                        padding=20,
                        border_radius=12,
                        bgcolor=ft.colors.WHITE,
                        height=page.window_height * 0.75,  # Tarjeta ocupa el 75% del alto disponible
                        width=page.window_width * 0.45,  # Tarjeta ocupa el 45% del ancho disponible
                    ),
                    elevation=10,
                ),
                alignment=ft.alignment.center,  # Centrar la tarjeta en la pantalla
                expand=True,  # Expandir para centrar verticalmente
            )
        )

        # Actualizar la página
        page.update()
    # Detectar cambios en el método de pago seleccionado
    selected_payment.on_change = update_payment_fields

    # Mostrar la vista inicial
    update_payment_fields(None)
    page.update()
