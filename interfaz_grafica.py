import flet as ft

def login(pagina=ft.Page):
    # Funciones de login
    async def funcion_continuar(event):
        if caja_codigo.value:
            usuario = caja_codigo.value
            caja_codigo.error = None
        else:
            caja_codigo.error = "Ingrese una contraseña valida"

        if caja_nip.value:
            contraseña = caja_nip
            caja_nip.error = None
        else:
            caja_nip.error = "Ingrese una contraseña valida"

    # TODO implementar la funcion que aga posible la comunicacion de autentificacion

    pagina.tittle = "Login SIGHA"  # El nombre durante el login sera este
    usuario = ""
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

    return usuario, contraseña