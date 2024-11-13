import flet as ft
import unicodedata
import json
import Carro
import añadir
import Carro 

cart = []  

def normalize_string(s: str) -> str:
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').lower()

def load_products():
    with open("productos.json", "r", encoding="utf-8") as file:
        return json.load(file)

def save_products(products):
    with open("productos.json", "w", encoding="utf-8") as file:
        json.dump(products, file, ensure_ascii=False, indent=4)

def show_menu(page):
    page.controls.clear()  # Limpiar controles de la página
    main(page)

def main(page: ft.Page):
    page.window_width = 400
    page.window_height = 700
    page.title = "Tienda"
    products = load_products()

    def add_to_cart(product, quantity):
        if quantity <= 0:
            print("La cantidad debe ser mayor que cero.")
            return

        # Verificar si el producto ya está en el carrito
        for item in cart:
            if item['nombre'] == product['nombre']:
                item['cantidad'] += quantity  # Aumentar la cantidad
                break
        else:
            # Si no está en el carrito, agregarlo con la cantidad
            cart.append({**product, 'cantidad': quantity})

        print(f"Producto agregado al carrito: {product['nombre']} x{quantity}")
        print(f"Carrito actual: {cart}")

        show_snackbar(f"Producto agregado al carrito: {product['nombre']} x{quantity}")

    def show_snackbar(message):
        snackbar = ft.SnackBar(
            content=ft.Text(message),
            action="Cerrar",
            action_color=ft.colors.BLUE,
        )
        page.snack_bar = snackbar
        snackbar.open = True
        page.update()

    def go_to_cart(e, page):
        page.clean()
        Carro.main(page, cart)

    def delete_product(product):
        products.remove(product)
        save_products(products)
        update_product_section()

    def close_dialog(dialog):
        dialog.open = False
        page.update()

    def show_product_management():
        product_management_dialog = ft.AlertDialog(
            title=ft.Text("Gestión de Productos"),
            content=ft.Column(spacing=10, controls=[]),
            actions=[ 
                ft.TextButton("Cerrar", on_click=lambda e: close_dialog(product_management_dialog)),
            ],
        )

        # Llenar la columna con los productos
        for product in products:
            product_management_dialog.content.controls.append(
                ft.Row(
                    controls=[
                        ft.Text(product["nombre"], size=16),
                        # Formateamos el precio para que no se redondee
                        ft.Text(f"${float(product['precio']):.3f}"),  # Aquí utilizamos 3 decimales, para mostrar el valor original
                        ft.IconButton(
                            icon=ft.icons.DELETE,
                            on_click=lambda e, p=product: delete_product(p),
                            tooltip="Eliminar producto",
                            icon_color=ft.colors.RED,
                            icon_size=24,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                )
            )

        # Mostrar el diálogo
        page.dialog = product_management_dialog
        product_management_dialog.open = True
        page.update()

    welcome_message = ft.Container(
        content=ft.Row(
            controls=[ 
                ft.Text("¡Bienvenido!", size=20, weight="bold", color=ft.colors.BLUE),
                ft.IconButton(
                    icon=ft.icons.SHOPPING_CART,
                    on_click=lambda e: go_to_cart(e, page),  # Ir al carrito
                    tooltip="Ver carrito",
                    icon_color=ft.colors.BLUE,
                    icon_size=24,
                ),
                ft.IconButton(
                    icon=ft.icons.MANAGE_ACCOUNTS,
                    on_click=lambda e: show_product_management(),
                    tooltip="Gestionar productos",
                    icon_color=ft.colors.BLUE,
                    icon_size=24,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        padding=ft.padding.all(20),
        bgcolor=ft.colors.WHITE,
        border_radius=10,
        margin=ft.margin.only(left=10, right=10),
        width=page.window_width - 20,
    )
    page.update()
    navigation_bar_2 = ft.NavigationBar(
        destinations=[ 
            ft.NavigationBarDestination(icon=ft.icons.HOME, label="Home"),
            ft.NavigationBarDestination(icon=ft.icons.MONEY, label="Currency"),
            ft.NavigationBarDestination(icon=ft.icons.ADD, label="Añadir"),
        ],
        height=70,
        on_change=lambda e: handle_navigation_change(e),
    )

    def handle_navigation_change(e):
        if e.control.selected_index == 0:  # Home
            show_menu(page)
        elif e.control.selected_index == 2:  # Añadir
            page.clean()  # Limpiar la página actual
            añadir.main(page)  # Cargar la página de añadir producto

    product_containers = []
    quantity_inputs = {}

    def update_product_section(filter_text=""):
        product_containers.clear()
        normalized_filter_text = normalize_string(filter_text)
        for product in products:
            if normalized_filter_text in normalize_string(product["nombre"]):
                quantity_input = ft.TextField(
                    value="0",  # Valor por defecto
                    width=50,
                    text_align=ft.TextAlign.CENTER,
                    read_only=False,  # Hacer el campo solo lectura
                )
                quantity_inputs[product["nombre"]] = quantity_input  # Almacenar el campo en el diccionario

                product_containers.append(
                    ft.Container(
                        content=ft.Row(controls=[ 
                            ft.Container(
                                content=ft.Image(src=product["imagen"], width=100, height=150),
                                border_radius=10,
                                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                            ),
                            ft.Column(controls=[ 
                                ft.Text(product["nombre"], size=16),
                                ft.Text(f"Descripción: {product['descripcion']}", size=12, color=ft.colors.BLACK54),
                                # Mostramos el precio con los decimales completos
                                ft.Text(f"Precio: {float(product['precio']):.3f}", size=14, color=ft.colors.GREEN),
                                ft.Text(f"Cantidad disponible: {product['cantidad']}", size=12, color=ft.colors.BLACK),
                                ft.Row(
                                    controls=[ 
                                        ft.IconButton(
                                            icon=ft.icons.ADD,
                                            on_click=lambda e, p=product, q=quantity_input: increase_quantity(p, q),
                                            tooltip="Agregar al carrito",
                                            icon_color=ft.colors.BLUE,
                                            icon_size=24,
                                        ),
                                        quantity_input,
                                        ft.IconButton(
                                            icon=ft.icons.REMOVE,
                                            on_click=lambda e, q=quantity_input: decrease_quantity(q),
                                            tooltip="Eliminar del carrito",
                                            icon_color=ft.colors.RED,
                                            icon_size=24,
                                        ),
                                    ]
                                ),
                                ft.Container(
                                    content=ft.TextButton(
                                        text="Agregar al carrito",
                                        on_click=lambda e, p=product, q=quantity_input: add_to_cart(p, int(q.value) if q.value.isdigit() else 0),
                                        tooltip="Agregar cantidad al carrito",
                                        style=ft.ButtonStyle(
                                            color=ft.colors.WHITE,  # Color del texto
                                            bgcolor=ft.colors.GREEN,  # Color de fondo
                                        ),
                                    ),
                                    padding=ft.padding.all(10),  # Agregar algo de relleno
                                    border_radius=5,  # Agregar un borde redondeado
                                ),
                            ]),
                        ]),
                        padding=10,
                        bgcolor=ft.colors.WHITE,
                        margin=ft.margin.all(5),
                        border_radius=10,
                    ) 
                )
        products_section.controls = product_containers
        page.update()

    def increase_quantity(product, quantity_input):
        current_quantity = int(quantity_input.value)
        max_quantity = product['cantidad']  # Suponiendo que 'cantidad' es la cantidad disponible
        if current_quantity < max_quantity:  # Verificar que no exceda la cantidad disponible
            quantity_input.value = str(current_quantity + 1)
            quantity_input.update()  # Actualizar el campo de texto

    def decrease_quantity(quantity_input):
        current_quantity = int(quantity_input.value)
        if current_quantity > 0:  # Verificar que no sea menor a 0
            quantity_input.value = str(current_quantity - 1)
            quantity_input.update()  # Actualizar el campo de texto

    search_input = ft.TextField(
        hint_text="Buscar productos...", 
        width=300, 
        border_radius=10,
        on_change=lambda e: update_product_section(e.control.value)  # Actualiza automáticamente al escribir
    )

    search_bar = ft.Container(
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[ 
                search_input,
                ft.IconButton(
                    icon=ft.icons.SEARCH,
                    on_click=lambda _: update_product_section(search_input.value),
                    tooltip="Buscar",
                    icon_color=ft.colors.BLACK,
                    icon_size=18,
                ),
            ]
        ),
        padding=ft.padding.all(10),
    )

    products_section = ft.ListView(height=0, expand=True, spacing=10)
    
    update_product_section()

    page.add(welcome_message)
    page.add(search_bar)
    page.add(products_section)
    page.add(navigation_bar_2)
    page.update()

