import flet as ft
from project.views.header import header
from project.database.crud_entero import *
# Variable con la dirección
default_address = "Calle Falsa 123, Madrid, España"

def compra_view(page, shopping_cart, cart_count_text):
    # Opciones de pago
    payment_methods = ["Visa", "MasterCard", "PayPal"]
    selected_payment = ft.Dropdown(
        label="Selecciona un método de pago",
        options=[ft.dropdown.Option(text=method) for method in payment_methods]
    )

    # Confirmar compra
    def confirm_purchase(e):
        if not shopping_cart:
            page.snack_bar = ft.SnackBar(ft.Text("Tu cesta está vacía."))
            page.snack_bar.open = True
        elif not selected_payment.value:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor, elige un método de pago."))
            page.snack_bar.open = True
        else:
            for item in shopping_cart:
                delete_product(str(item[0].id))
            shopping_cart.clear()
            page.snack_bar = ft.SnackBar(ft.Text("¡COMPRA REALIZADA! 🎉"))
            page.snack_bar.open = True
            page.go("/")  # Redirige al home después de la compra

    page.controls.clear()
    page.add(header(page, shopping_cart, cart_count_text))
    page.add(ft.Text("Zona de Compra", style="headlineMedium"))
    page.add(ft.Text(f"Dirección: {default_address}"))
    page.add(selected_payment)
    page.add(ft.ElevatedButton("Finalizar Compra", on_click=confirm_purchase))
    page.update()
