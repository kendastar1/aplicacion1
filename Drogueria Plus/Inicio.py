import flet as ft
import Menu  # Asegúrate de que el archivo Menu.py esté en el mismo directorio

class MainPage(ft.UserControl):
    def build(self):
        return ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text("GESTION DE PRODUCTOS", size=40, weight="bold", text_align=ft.TextAlign.CENTER),
                    width=400,
                    alignment=ft.Alignment(0, 0)  # Alineación centrada en el contenedor
                ),
                ft.Container(height=20),
                ft.Image(src="farmacia.png", width=300, height=200),
                ft.Container(height=20),
                ft.ElevatedButton(
                    "Comenzar", 
                    on_click=self.start_application,
                    width=150, 
                    height=50,
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=20)
                    )
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20  # Espaciado entre los elementos
        )

    def start_application(self, e):
        self.page.clean()
        Menu.main(self.page)  # Llama a la función main del menú

def main(page: ft.Page):
    page.title = "Drogueria"
    page.window_width = 400
    page.window_height = 700
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = ft.colors.WHITE
    page.resizable = False
    page.icon = "icono.png"
    page.add(MainPage())

ft.app(target=main)  # Este es el punto de entrada de la aplicación