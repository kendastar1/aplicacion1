import flet as ft
import os
import shutil  # Importar shutil para copiar archivos
import json

# Función para guardar el producto en un archivo JSON
def guardar_producto(nombre, descripcion, precio, cantidad, imagen_nombre):
    producto = {
        "nombre": nombre,
        "descripcion": descripcion,
        "precio": "{:.3f}".format(precio),  # Formato de tres decimales
        "cantidad": cantidad,
        "imagen": f"imagenes/{imagen_nombre}"  # Guardar la ruta relativa de la imagen en el JSON
    }
    
    # Cargar productos existentes si el archivo ya existe
    if os.path.exists("productos.json"):
        with open("productos.json", "r") as archivo:
            productos = json.load(archivo)
    else:
        productos = []

    # Añadir el nuevo producto a la lista
    productos.append(producto)
    
    # Guardar la lista actualizada en el archivo JSON
    with open("productos.json", "w") as archivo:
        json.dump(productos, archivo, indent=4)
    
    return "Producto guardado exitosamente."

# Función de Flet para crear la interfaz
def main(page: ft.Page):
    page.title = "Añadir Producto"
    page.window_width = 400
    page.window_height = 700
    
    # Crear campos de entrada para los datos del producto
    nombre_input = ft.TextField(label="Nombre del Producto")
    descripcion_input = ft.TextField(label="Descripción del Producto", multiline=True)
    precio_input = ft.TextField(label="Precio del Producto", keyboard_type=ft.KeyboardType.NUMBER)
    cantidad_input = ft.TextField(label="Cantidad Disponible", keyboard_type=ft.KeyboardType.NUMBER)

    # Campo de imagen para seleccionar una imagen
    imagen_input = ft.TextField(label="Imagen del Producto", disabled=True)
    imagen_ruta = ""
    imagen_nombre = ""

    # Crear carpeta "imagenes" si no existe
    if not os.path.exists("imagenes"):
        os.makedirs("imagenes")

    # Función para manejar el archivo seleccionado
    def archivo_seleccionado(e: ft.FilePickerResultEvent):
        nonlocal imagen_ruta, imagen_nombre
        if e.files and e.files[0].path:
            imagen_ruta = e.files[0].path  # Ruta completa de la imagen seleccionada
            imagen_nombre = os.path.basename(imagen_ruta)  # Obtener solo el nombre del archivo
            imagen_input.value = imagen_nombre  # Mostrar solo el nombre del archivo en el campo de texto
            page.update()
        else:
            mostrar_mensaje("Error: No se seleccionó ningún archivo.")

    # Añadir el FilePicker al inicio de la página
    file_picker = ft.FilePicker(on_result=archivo_seleccionado)
    page.overlay.append(file_picker)

    # Función para manejar la selección de imagen
    def seleccionar_imagen(e):
        file_picker.pick_files(allow_multiple=False, allowed_extensions=["png", "jpg", "jpeg"])

    # Función para mostrar mensajes en un cuadro de diálogo
    def mostrar_mensaje(texto):
        dialogo = ft.AlertDialog(title=ft.Text(texto))
        page.dialog = dialogo
        dialogo.open = True
        page.update()

    # Función para manejar el clic del botón de "Guardar"
    def guardar_click(e):
        # Obtener valores de los campos
        nombre = nombre_input.value
        descripcion = descripcion_input.value
        
        # Validar que precio y cantidad sean numéricos
        try:
            precio = float(precio_input.value.replace(",", "."))  # Convertir a float, permitir coma decimal
            cantidad = int(cantidad_input.value)
        except ValueError:
            mostrar_mensaje("Error: El precio y la cantidad deben ser números.")
            return

        # Copiar la imagen a la carpeta "imagenes" si se ha seleccionado una
        if imagen_ruta:
            destino = os.path.join("imagenes", imagen_nombre)
            try:
                shutil.copy(imagen_ruta, destino)
            except Exception as error:
                mostrar_mensaje(f"Error al copiar la imagen: {error}")
                return

        # Guardar el producto y mostrar mensaje
        mensaje = guardar_producto(nombre, descripcion, precio, cantidad, imagen_nombre)
        mostrar_mensaje(mensaje)

    # Función para volver al menú
    def volver_menu(e):
        page.clean()  # Limpiar la página actual
        import Menu  # Importar el archivo menu.py (la página principal)
        Menu.main(page)  # Llamar a la función main de menu.py para mostrar el menú

    # Botón de retroceso (flecha hacia atrás) para regresar al menú
    volver_button = ft.IconButton(
        icon=ft.icons.ARROW_BACK,  # Icono de flecha hacia atrás
        on_click=volver_menu,  # Función para volver al menú
        tooltip="Volver al Menú",  # Tooltip que aparece al pasar el ratón sobre el botón
        icon_size=30,  # Tamaño del icono
        icon_color=ft.colors.BLUE  # Color del icono
    )

    # Botón de guardar y botón de selección de imagen
    guardar_button = ft.ElevatedButton("Guardar Producto", on_click=guardar_click)
    seleccionar_imagen_button = ft.ElevatedButton("Seleccionar Imagen", on_click=seleccionar_imagen)

    # Crear la barra de navegación
    navigation_bar = ft.NavigationBar(
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
            volver_menu(None)  # Volver al menú
        elif e.control.selected_index == 1:  # Currency
            # Puedes agregar aquí una acción si deseas agregar una nueva vista para "Currency"
            pass
        elif e.control.selected_index == 2:  # Añadir
            # Ya estamos en la vista "Añadir Producto", no es necesario hacer nada
            pass
        elif e.control.selected_index == 3:  # Settings
            # Aquí puedes agregar acciones si deseas implementar la vista de configuración
            pass

    # Añadir todos los elementos a la página
    page.add(
        volver_button,  # Botón de retroceso (flecha)
        nombre_input,
        descripcion_input,
        precio_input,
        cantidad_input,
        imagen_input,
        seleccionar_imagen_button,
        guardar_button,
        navigation_bar  # Barra de navegación al final
    )
    page.update()
