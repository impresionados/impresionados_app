import flet as ft
from project.views.header import header

def cesta_view(page, shopping_cart,update_cart_count):
    # Actualizar la vista de la cesta
    def update_cart_view():
        page.controls.clear()
        page.add(header(page, shopping_cart, update_cart_count))

        page.add(ft.Text("Cesta de Compras", style="headlineMedium"))

        if shopping_cart:
            page.add(ft.Column(
                controls=[
                    ft.Text(f"{item['name']} - {item['price']}€")
                    for item in shopping_cart
                ]
            ))
            # Nuevo botón para proceder a la compra
            page.add(ft.ElevatedButton("Comprar", on_click=lambda e: page.go("/compra")))
        else:
            page.add(ft.Text("Tu cesta está vacía", style="bodyLarge"))

        page.add(ft.ElevatedButton("Vaciar cesta", on_click=clear_cart))
        page.update()

    # Vaciar la cesta y refrescar
    def clear_cart(e):
        shopping_cart.clear()
        page.snack_bar = ft.SnackBar(ft.Text("Cesta vaciada"))
        page.snack_bar.open = True
        update_cart_view()

    update_cart_view()
