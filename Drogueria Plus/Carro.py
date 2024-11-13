# Carro.py
import flet as ft
import Menu  # Asegúrate de importar correctamente el archivo Menu.py

def main(page: ft.Page, cart):
    page.window_width = 400
    page.window_height = 700
    page.title = "Carrito de Compras"

    def update_cart_section():
        product_containers.clear()
        total_price = 0  # Acumulador para el precio total
        
        for item in cart:
            item_price = float(item["precio"]) * item["cantidad"]  # Precio por producto
            total_price += item_price  # Acumulamos el precio total

            product_containers.append(
                ft.Container(
                    content=ft.Row(controls=[ 
                        ft.Container(
                            content=ft.Image(src=item["imagen"], width=100, height=150),
                            border_radius=10,
                            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                        ),
                        ft.Column(controls=[ 
                            ft.Text(item["nombre"], size=16),
                            ft.Text(f"Precio: ${item_price:.2f}", size=14, color=ft.colors.GREEN),
                            ft.Text(f"Cantidad: {item['cantidad']}", size=12, color=ft.colors.BLACK),
                        ]), 
                    ]), 
                    padding=5,  # Reducir padding
                    bgcolor=ft.colors.WHITE,
                    margin=ft.margin.only(top=5, bottom=5),  # Reducir la separación entre los productos
                    border_radius=10,
                )
            )
        
        # Mostrar el precio total
        product_containers.append(
            ft.Container(
                content=ft.Row(controls=[ 
                    ft.Column(controls=[ 
                        ft.Text(f"Precio Total: ${total_price:.2f}", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE)
                    ]),
                ]),
                padding=10,
                bgcolor=ft.colors.WHITE,
                margin=ft.margin.only(top=5, bottom=5),  # Reducir la separación debajo del precio total
                border_radius=10,
            )
        )
        
        page.update()

    product_containers = []
    update_cart_section()

    # Función para manejar el evento del botón de regreso
    def go_back(e):
        page.clean()  # Limpia la página
        Menu.main(page)  # Llama al menú, pasándole el carrito

    # Agregar el título, botón de regreso y la lista desplazable
    page.add(
        ft.Column(
            controls=[
                ft.Row(controls=[ 
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,  # Ícono de flecha hacia la izquierda
                        on_click=go_back,  # Acción al hacer clic
                        icon_size=30,  # Tamaño del ícono
                    ),
                    ft.Text("Carrito de Compras", size=20, weight=ft.FontWeight.BOLD, expand=True),
                ]),
                ft.Divider(),  # Línea de separación
                ft.ListView(  # Usamos ListView para el desplazamiento
                    controls=product_containers,
                    expand=True,  # Hace que ocupe el espacio disponible
                    spacing=5,  # Espaciado entre los elementos
                    auto_scroll=True,  # Permite el desplazamiento automáticamente
                ),
            ],
            expand=True
        )
    )
    page.update()


