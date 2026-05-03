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
    pagina.title = "SIGHA - Maestro"#Nombre de la pagina, eneste caso al ser la seccion maestro
    pagina.vertical_alignment = ft.MainAxisAlignment.START#Desde donde se pondran las cosas de la pagina
    pagina.padding = 20 #Espaciado de la pagina

    parte_superior_hogar = ft.Row(
        controls=[
            # Columna para Texto de Bienvenida y Departamento
            ft.Column(
                controls=[
                    ft.Text(
                        f"Hola, {usuario.nombre}",
                        size=24,
                        weight="bold",
                        color="white",
                    ),
                    ft.Text(
                        f"{usuario.obtener_departamento()}",
                        color=ft.Colors.GREY,
                        size=14
                    ),
                ],
                spacing=0,  # Sin espacio entre las lineas de txto
                tight=True  # La columna solo ocupa el espacio de su contenido
            ),

            # Espaciador que empuja el icono a la derecha
            ft.Container(expand=True),

            # Icono a la derecha
            ft.Icon(
                ft.Icons.ACCOUNT_CIRCLE,
                color="red",
                size=50,
            )
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    seccion_alertas_activas = f

    pagina.add(parte_superior_hogar)
    pagina.update()

    def interfaz_alumno(pagina: ft.Page, usuario: Alumno):
    pagina.title = "SIGHA - Alumno"
    pagina.vertical_alignment = ft.MainAxisAlignment.START
    pagina.padding = 20
    pagina.bgcolor = "#0f172a"

    # ── PARTE SUPERIOR ───────────────────
    parte_superior = ft.Row(
        controls=[
            ft.Column(
                controls=[
                    ft.Text(
                        f"Hola, {usuario.nombre}",  
                        size=24,
                        weight="bold",
                        color="white",
                    ),
                    ft.Text(
                        f"{usuario.obtener_carrera()} • {usuario.obtener_semestre()}° semestre",
                        color=ft.Colors.GREY,
                        size=14
                    ),
                ],
                spacing=0,
                tight=True
            ),

            ft.Container(expand=True),

            ft.Icon(
                ft.Icons.ACCOUNT_CIRCLE,
                color="#c084fc",
                size=50,
            )
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # ── TARJETAS  ───────────────────────
    seccion_datos = ft.Row(
        controls=[
            ft.Container(
                content=ft.Column([
                    ft.Text("Promedio", size=12, color=ft.Colors.GREY),
                    ft.Text(
                        str(usuario.obtener_promedio_general()),
                        size=22,
                        weight="bold",
                        color="#c084fc"
                    )
                ]),
                bgcolor="#1e293b",
                padding=15,
                border_radius=15,
                expand=True
            ),

            ft.Container(
                content=ft.Column([
                    ft.Text("Créditos", size=12, color=ft.Colors.GREY),
                    ft.Text(
                        f"{usuario.obtener_creditos_obtenidos()} / 320",
                        size=16,
                        weight="bold",
                        color="white"
                    )
                ]),
                bgcolor="#1e293b",
                padding=15,
                border_radius=15,
                expand=True
            ),
        ],
        spacing=10
    )

    # ── ACCIONES  ────────
    seccion_acciones = ft.Column(
        controls=[
            ft.ElevatedButton(
                "Buscar materias",
                width=float("inf"),
                height=50,
                bgcolor="#c084fc",
                color="white",
                on_click=lambda _: print("Buscar materias")
            ),

            ft.ElevatedButton(
                "Mis alertas",
                width=float("inf"),
                height=50,
                bgcolor="#f472b6",
                color="black",
                on_click=lambda _: print("Mis alertas")
            ),

            ft.ElevatedButton(
                "Simulador de horario",
                width=float("inf"),
                height=50,
                bgcolor="#0ea5e9",
                color="white",
                on_click=lambda _: print("Simulador")
            ),
        ],
        spacing=10
    )

    # ── ENSAMBLE FINAL ─────────────────────────────────────────────
    pagina.add(
        ft.Column(
            controls=[
                parte_superior,
                ft.Divider(color="transparent"),
                seccion_datos,
                ft.Divider(color="transparent"),
                ft.Text("Acciones", color="white", size=16, weight="bold"),
                seccion_acciones
            ]
        )
    )

    pagina.update()