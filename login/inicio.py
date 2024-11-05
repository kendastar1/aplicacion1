import flet as ft
import unicodedata

def normalize_string(s: str) -> str:
    # Normaliza la cadena para eliminar acentos y convierte a minúsculas
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').lower()

def main(page: ft.Page):
    page.window_width = 400  # Ancho de la ventana
    page.window_height = 700  # Alto de la ventana
    page.title = "Tienda Móvil"

    # Mensaje de bienvenida en una tarjeta
    welcome_message = ft.Container(
        content=ft.Column(
            controls=[ft.Text("¡Bienvenido!", size=20, weight="bold", color=ft.colors.BLUE)],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        padding=ft.padding.all(20),
        bgcolor=ft.colors.WHITE,
        border_radius=10,
        margin=ft.margin.only(left=10, right=10, top=10),
        width=page.window_width - 20,
    )

    # Crear la primera barra de navegación
    navigation_bar_1 = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.EXPLORE, label="Explore"),
            ft.NavigationBarDestination(icon=ft.icons.COMMUTE, label="Commute"),
            ft.NavigationBarDestination(icon=ft.icons.BOOKMARK_BORDER, selected_icon=ft.icons.BOOKMARK, label="Bookmark"),
        ],
        height=50,
    )

    # Crear la segunda barra de navegación
    navigation_bar_2 = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.HOME, label="Home"),
            ft.NavigationBarDestination(icon=ft.icons.MONEY, label="Currency"),
            ft.NavigationBarDestination(icon=ft.icons.ADD, label="Add Product"),
            ft.NavigationBarDestination(icon=ft.icons.SETTINGS, label="Settings"),
        ],
        height=70,
    )

    # Productos iniciales
    products = [
        {"name": "Teléfono Modelo A", "price": "$199", "image": "imagen2.jpg"},
        {"name": "Teléfono Modelo B", "price": "$299", "image": "imagen3.jpg"},
    ]

    # Sección de productos
    product_containers = []

    def update_product_section(filter_text=""):
        # Limpiar productos actuales
        product_containers.clear()
        # Normalizar el texto de búsqueda
        normalized_filter_text = normalize_string(filter_text)
        # Filtrar productos según el texto de búsqueda
        for product in products:
            if normalized_filter_text in normalize_string(product["name"]):
                product_containers.append(
                    ft.Container(
                        content=ft.Row(controls=[
                            ft.Container(
                                content=ft.Image(src=product["image"], width=100, height=150),
                                border_radius=10,
                                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                            ),
                            ft.Column(controls=[
                                ft.Text(product["name"], size=16),
                                ft.Text(product["price"], size=14, color=ft.colors.GREEN),
                                ft.ElevatedButton(text="Comprar", on_click=lambda e, p=product: print(f"Comprado: {p['name']}")),
                            ]),
                        ]),
                        padding=10,
                        bgcolor=ft.colors.WHITE,
                        margin=ft.margin.all(5),
                        border_radius=10,
                    )
                )
        # Actualizar la columna de productos
        products_section.controls = product_containers
        page.update()

    # Barra de búsqueda centrada con lupa más pequeña
    search_input = ft.TextField(hint_text="Buscar productos...", width=300, border_radius=10)

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

    # Sección de productos inicial
    products_section = ft.Column()

    # Llenar la sección de productos inicialmente
    update_product_section()  # Cargar todos los productos al inicio

    # Agregar todas las secciones a la página
    page.add(welcome_message)
    page.add(navigation_bar_1)
    page.add(search_bar)
    page.add(products_section)
    page.add(navigation_bar_2)

ft.app(main)
