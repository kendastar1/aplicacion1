import flet as ft
import subprocess
import sys

def main(page: ft.Page):
    # Configuración del tamaño de la ventana para simular un teléfono
    page.window_width = 400
    page.window_height = 700
    page.title = "Bienvenido a Kiosco"
    
    # Centrar el contenido en la ventana
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Función para manejar el evento de inicio de sesión
    def login_clicked(e):
        with open("usuarios.txt", "r") as file:
            users = file.readlines()
            user_found = False
            for line in users:
                stored_username, stored_password = line.strip().split(",")
                if username.value == stored_username and password.value == stored_password:
                    user_found = True
                    message.value = "Inicio de sesión exitoso"
                    message.color = "green"
                    page.update()
                    
                    # Ejecutar el archivo inicio.py
                    subprocess.Popen([sys.executable, "inicio.py"])
                    page.window_close()  # Cerrar la ventana actual si es necesario
                    return

            if not user_found:
                message.value = "Usuario o contraseña incorrectos"
                message.color = "red"
                log_failed_attempt(username.value)

        page.update()

    # Función para manejar el evento de registro
    def register_clicked(e):
        registration_form.visible = True
        login_form.visible = False
        page.update()

    # Función para manejar el evento de confirmación del registro
    def confirm_registration(e):
        if new_username.value and new_password.value:
            with open("usuarios.txt", "a") as file:
                file.write(f"{new_username.value},{new_password.value}\n")
            message.value = "Registro exitoso. Ahora puedes iniciar sesión."
            message.color = "green"
            registration_form.visible = False
            login_form.visible = True
        else:
            message.value = "Por favor, completa todos los campos."
            message.color = "red"
        page.update()

    # Función para registrar intentos fallidos
    def log_failed_attempt(user):
        with open("registro.txt", "a") as file:
            file.write(f"Intento fallido para usuario: {user}\n")

    # Crear los campos de usuario y contraseña para el inicio de sesión
    username = ft.TextField(label="Usuario", autofocus=True, width=300)
    password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)

    # Mensaje de feedback
    message = ft.Text("")

    # Imagen de perfil circular con sombra suave alrededor
    profile_image = ft.Container(
        content=ft.Image(
            src="imagen.jpeg",  # Imagen de alta resolución
            width=120,
            height=120,
            fit=ft.ImageFit.COVER,
        ),
        width=120,
        height=120,
        border_radius=ft.border_radius.all(60),  # Radio para hacer la imagen circular
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        bgcolor=ft.colors.TRANSPARENT,  # Fondo transparente para un borde limpio
        shadow=ft.BoxShadow(
            spread_radius=4,     # Extensión mínima de la sombra
            blur_radius=7,       # Difuminado de la sombra para suavidad
            color="rgba(0, 0, 0, 0.25)",  # Color de sombra más claro y sutil
            offset=ft.Offset(0, 1)  # Desplazamiento leve para centrar la sombra
        ),
    )

    # Botón de inicio de sesión
    login_button = ft.ElevatedButton("Iniciar sesión", on_click=login_clicked)
    
    # Botón para mostrar el formulario de registro
    register_button = ft.TextButton("¿No tienes cuenta? Regístrate", on_click=register_clicked)

    # Formulario de inicio de sesión
    login_form = ft.Column(
        [
            profile_image,
            ft.Text("Inicio de Sesión", size=30, weight="bold"),
            username,
            password,
            login_button,
            register_button,
            message,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        visible=True  # Hacer visible el formulario de inicio de sesión por defecto
    )

    # Campos del formulario de registro
    new_username = ft.TextField(label="Nuevo Usuario", width=300)
    new_password = ft.TextField(label="Nueva Contraseña", password=True, can_reveal_password=True, width=300)
    
    # Botón para confirmar el registro
    confirm_button = ft.ElevatedButton("Registrar", on_click=confirm_registration)

    # Formulario de registro (inicialmente oculto)
    registration_form = ft.Column(
        [
            profile_image,
            ft.Text("Registro", size=30, weight="bold"),
            new_username,
            new_password,
            confirm_button,
            message,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        visible=False  # Hacer invisible el formulario de registro por defecto
    )

    # Agregar ambos formularios a la página
    page.add(login_form)
    page.add(registration_form)

# Ejecutar la aplicación
ft.app(target=main)