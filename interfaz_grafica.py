import flet as ft
import flet.controls.material.icons
from flet.controls import alignment

from maestro import Maestro


def login(pagina=ft.Page):
    # Funciones de login
    def funcion_continuar(event):
        if caja_codigo.value:
            usuario_codigo = caja_codigo.value
            caja_codigo.error = None
        else:
            caja_codigo.error = "Ingrese una contraseña valida"

        if caja_nip.value:
            contraseña = caja_nip
            caja_nip.error = None
        else:
            caja_nip.error = "Ingrese una contraseña valida"

    # TODO implementar la funcion que aga posible la comunicacion de autentificacion

    pagina.title = "SIGHA - Login"  # El nombre durante el login sera este
    usuario = None
    usuario_codigo = ""
    contraseña = ""

    caja_codigo = ft.TextField(  # Donde el usuario debera de ingresar el dato codigo
        label="Usuario",  # Nombre de lo que vamos a pedir, aparecera en el recuadro
        border_color="1d1e33",  # Color del borde del recuadro
        hint_text="Ingrese su codigo o nombre de usuario"

    )

    caja_nip = ft.TextField(
        label="Contraseña",  # Nombre de que pedimos
        hint_text="Ingrese tu contraseña o NIP",  # Cuadro de texto que aparece al dejar el mouse
        border_color="1d1e33",  # Color del borde
        password=True,  # Indica que el modo contraseña esta activo
        can_reveal_password=True,  # Activa la opcion de revelar conraseña
        prefix_icon=ft.Icons.PASSWORD_OUTLINED,  # Remplaza los caracteres para que no se vean

    )

    boton_continuar = ft.ElevatedButton(
        content="Continuar",
        width=300,
        height=50,
        on_click=funcion_continuar,
        style=ft.ButtonStyle(
            bgcolor="#0ea5e9",
            color="white",
            shape=ft.RoundedRectangleBorder(radius=10)
        )
    )

    pagina_login = ft.Container(
        content=ft.Column(
            controls=[

                # TODO poner imagen del logotipo

                ft.Text("INICIO DE SESION",
                        color="white",
                        weight="bold",
                        size=26,
                        ),

                ft.Text("Ingrese sus credenciales",
                        color="white",
                        size=14,
                        ),

                caja_codigo,
                caja_nip,
                boton_continuar
            ]
        )
    )
    pagina.add(pagina_login)

    return usuario


def interfaz_maestro(pagina: ft.Page, usuario: Maestro):
    pagina.title = "SIGHA - Maestro"
    pagina.vertical_alignment = ft.MainAxisAlignment.SPACE_AROUND

    print(usuario)

    parte_superior_hogar = ft.Row(
        controls = [
            ft.Text(f"Hola, {usuario.nombre}",
                    size = 24,
                    weight = "bold",
                    color = "white",
                    ),
            ft.Icon(ft.Icons.ACCOUNT_CIRCLE,
                    color = "Red",
                    size = 50,
                    align = ft.Alignment(-1, 1) )

        ],
        expand = True,
        align = ft.Alignment(-1,-1),

    )

    pagina.add(ft.Container(
        content = ft.Column(
            controls=[
                parte_superior_hogar,
            ]
        )
    ))