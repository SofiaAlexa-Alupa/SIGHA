import flet as ft
from datetime import datetime



import usuario
from alertas import Alerta
from hora import Hora
from maestro import Maestro
from alumno import Alumno
from nombre import Nombre
from materia import Materia

BG      = "#0f172a"   # Fondo oscuro principal
CARD    = "#1e293b"   # Fondo de las tarjetas
PURPLE  = "#7c3aed"   # Morado para acentos
TEXT    = "#ffffff"   # Texto blanco
GREY    = "#94a3b8"   # Texto gris secundario
BORDER = "#818cf8"




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

    pagina.padding = 0
    pagina.vertical_alignment = ft.MainAxisAlignment.START
    pagina.horizontal_alignment = ft.CrossAxisAlignment.STRETCH

    cabezal = ft.Container(
        content=ft.Row(
            [
                ft.Column(
                    [
                        ft.Text(f"Hola, {usuario.obtenerNombre()}",
                                color=ft.Colors.WHITE,
                                size=24),
                        ft.Text(f"{usuario.obtener_departamento()}",
                                color=ft.Colors.GREY,
                                size=10),
                    ],
                    spacing=2,
                ),
                ft.Icon(ft.Icons.ACCOUNT_CIRCLE_OUTLINED,
                        color=ft.Colors.RED_ACCENT,
                        size=60),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=CARD,
        padding=ft.Padding.only(left=20, right=20, top=40, bottom=12),
    )


    def menu_hogar():
        seccion_1 = seccion_1_materias_registradas(pagina, usuario)
        seccion_2 = seccion_2_disponibilidad(pagina, usuario)
        seccion_3 = seccion_3_Notificaciones(pagina, usuario)

        pagina.controls.clear()
        pagina.add(cabezal)          # ← El cabezal siempre aparece
        pagina.add(ft.Container(
            content=ft.Column(
                [
                    seccion_1,
                    seccion_2,
                    seccion_3,
                ],
                scroll=ft.ScrollMode.AUTO,  # ← Scroll si el contenido es largo
                spacing=10,
            ),
            padding=ft.Padding.symmetric(horizontal=16, vertical=10),
            expand=True,
        ))
        pagina.update()

    def control_barra_navegacion(evento):
        indice = evento.control.selected_index  # ← selected_index correcto

        if indice == 0:
            menu_hogar()
        elif indice == 1:
            pass
        elif indice == 2:
            notificaciones_maestro(pagina, usuario)
        elif indice == 3:
            perfil_maestro(pagina, usuario)

    barra_inferior = ft.NavigationBar(
        bgcolor=CARD,
        indicator_color=PURPLE,
        selected_index=0,
        on_change=control_barra_navegacion,
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icons.HOME_OUTLINED,
                selected_icon=ft.Icons.HOME,
                label="Inicio",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.CALENDAR_MONTH_OUTLINED,
                selected_icon=ft.Icons.CALENDAR_MONTH,
                label="Buscar",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.NOTIFICATIONS_OUTLINED,
                selected_icon=ft.Icons.NOTIFICATIONS,
                label="Alertas",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.PERSON_OUTLINE,
                selected_icon=ft.Icons.PERSON,
                label="Perfil",
            ),
        ],
    )

    pagina.navigation_bar = barra_inferior
    menu_hogar()

def mostrar_informacion_materia_vista_profesor(pagina: ft.Page, materia: Materia):

    def build_lista_alumnos(materia: Materia):
        # Si la lista está vacía mostramos mensaje
        if not materia.alumnos:
            return ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.PERSON_OFF_OUTLINED, color=GREY, size=40),
                        ft.Text(
                            "No hay alumnos en esta materia",
                            color=GREY,
                            size=14,
                            italic=True,
                        )
                    ],
                    spacing=10,
                ),
                alignment=ft.Alignment.CENTER,
                bgcolor=CARD,
                padding=ft.Padding.all(16),
            )

        # Se ordena  la lista por nombre
        alumnos = materia.obtener_alumnos()
        alumnos.sort(key=lambda a: str(a.obtenerNombre()))  # ← key= y sin asignar

        return ft.Container(
            content=ft.Column(
                [
                    # Encabezado de la tabla
                    ft.Row(
                        [
                            ft.Text("Num",      size=14, color=GREY),
                            ft.Text("Nombre",   size=14, color=GREY, expand=True),
                            ft.Text("Semestre", size=14, color=GREY),
                        ],
                        spacing=16,
                    ),

                    # Filas de alumnos
                    ft.Column(
                        [
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Text(str(i),                        # ← número
                                                size=13, color=GREY),
                                        ft.Text(str(alumno.obtenerNombre()),
                                                size=13, color=TEXT, expand=True),
                                        ft.Text(str(alumno.obtener_semestre()),
                                                size=13, color=GREY),
                                    ],
                                    spacing=16,
                                ),
                                bgcolor=CARD,
                                border_radius=8,
                                padding=ft.Padding.symmetric(horizontal=12, vertical=8),
                            )
                            for i, alumno in enumerate(alumnos, start=1)  # ← enumerate correcto
                        ],
                        spacing=6,
                        scroll=ft.ScrollMode.AUTO,
                    )
                ],
                spacing=8,
            ),
            bgcolor=BG,
            border_radius=12,
            padding=ft.Padding.all(12),
        )

    # Header
    header = ft.Container(
        content=ft.Row(
            [
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK_OUTLINED,
                    icon_size=30,
                    on_click=lambda evento: (pagina.views.pop(), pagina.update()),
                ),
                ft.Container(
                    content=ft.Text(
                        "Detalles de la Materia",
                        size=24,
                        italic=True,
                        weight="bold",
                        color=TEXT,
                    ),
                    expand=True,
                    alignment=ft.Alignment.CENTER  # ← minúsculas
                )
            ]
        ),
        bgcolor=CARD,
        padding=ft.Padding.only(top=40, bottom=12),
    )

    # Días de clase unidos en un string
    dias_clase = ""
    if materia.obtener_dias_clase() is not None:
        for dia in materia.obtener_dias_clase():
            dias_clase += dia + " "  # ← Espacio entre días

    # Cuerpo con info de la materia
    cuerpo = ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                f"Materia: {materia.obtener_nombre()}",
                                color=GREY,
                                size=16,
                            ),
                            ft.Text(
                                f"Horario: {dias_clase} {materia.obtenerHoraInicio()} a {materia.obtenerHoraFin()}",
                                color=GREY,
                                size=16,
                            ),
                            ft.Text(
                                f"Aula: {materia.obtener_aula()}  –  Edificio: {materia.obtener_edificio()}",
                                color=GREY,
                                size=16,
                            ),
                            ft.Text(
                                f"Cupos: {materia.obtenerCuposDisponibles()} / {materia.obtenerCuposTotales()}",
                                color=GREY,
                                size=16,
                            ),
                        ],
                        spacing=8,
                    ),
                    bgcolor=CARD,
                    border=ft.Border.all(2, ft.Colors.GREY_500),  # ← minúsculas
                    border_radius=12,
                    padding=ft.Padding.all(16),
                    alignment=ft.Alignment.CENTER,# ← minúsculas
                ),
            ],
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
        ),
        padding=ft.Padding.all(16),
        alignment=ft.Alignment.CENTER,
        expand=True,
    )

    # Lista de alumnos
    vista_alumnos = build_lista_alumnos(materia)

    # Vista completa
    vista_completa = ft.View(
        controls=[
            header,
            cuerpo,
            vista_alumnos,
        ],
        bgcolor=BG,
    )

    pagina.views.append(vista_completa)
    pagina.update()

def obtener_clases_activas(usuario: Maestro):#Funcion que nosdevuelve la amtreia que tiene en este momento que enseñar yla materia que sigue
    timepo_actual = datetime.now()#Obtener la fehca actual
    dias_mapa = {0 : "L", 1 : "M", 2 : "X", 3 : "J", 4 : "V", 5 : "S", 6 : "D"}
    dia_hoy = dias_mapa[timepo_actual.weekday()]
    hora_actual = Hora(timepo_actual.hour, timepo_actual.minute)

    print(usuario)


    materias_hoy = [
        materia for materia in usuario.materias
        if dia_hoy in materia.obtener_dias_clase()
    ]

    materias_hoy.sort(key = lambda m: m.obtenerHoraInicio())

    activa = None
    proxima = None

    for materia in materias_hoy:
        hora_inicio = materia.obtenerHoraInicio()
        hora_fin = materia.obtenerHoraFin()

        if hora_inicio <= hora_actual <= hora_fin:
            activa = materia

        elif hora_actual < hora_inicio and proxima is None:
            proxima = materia



    return activa, proxima

def seccion_1_materias_registradas(pagina:ft.Page, usuario: Maestro):

    #materia_activa, materia_proxima = obtener_clases_activas(usuario=usuario)
    boton_activo = []

    materia_activa = Materia()
    materia_proxima = Materia()

    boton_activo.append(ft.Text(
        "Mis alertas clase (Sección 1)",
        color = PURPLE,
        size = 16,
        italic = True,
        weight = "bold"
    ))

    if materia_activa is None:
         boton_activo.append( ft.Container(
            content= ft.Row(
                [
                    ft.Text(
                        "No tienes mas materias el dia de hoy",
                        color=GREY,
                        size=14,
                        italic=True,
                    ),

                    ft.Icon(ft.Icons.WEEKEND_OUTLINED,
                            color = ft.Colors.GREY_500,
                            size = 60,
                            )
                ],
                spacing = 50
            ),
            border=ft.Border.all(1, GREY),
            border_radius=10,
            padding=ft.Padding.symmetric(horizontal=12, vertical=8),
            bgcolor= CARD,
            alignment=ft.Alignment.CENTER,
        )
         )
    elif materia_activa is not None:
        boton_activo.append( ft.Container(

            content = ft.Column(
                [
                    ft.Text("Su clase actual: ",
                            color=GREY,
                            size=16,
                            weight="bold"),

                    ft.Row(
                        [
                            ft.ElevatedButton(
                                content=f"Materia: {materia_activa.obtener_nombre()} | Edificio: {materia_activa.obtener_edificio()} | Aula: {materia_activa.obtener_aula()}",
                                on_click=lambda e: mostrar_informacion_materia_vista_profesor(pagina, materia_proxima),
                                expand=True,
                                width=float("inf"),
                                height=60,
                                style=ft.ButtonStyle(
                                    bgcolor=CARD,
                                    side = ft.BorderSide(width=2, color =ft.Colors.GREEN)
                                ),
                            ),
                            ft.Icon(ft.Icons.ACCESS_TIME,
                                    color = ft.Colors.GREEN,
                                    size = 50)
                        ]
                    )
                ],
                spacing = 6
            )
        )
    )
        if materia_proxima is not None:
            boton_activo.append( ft.Container(
                content = ft.Column(
                    [
                        ft.Text("Su siguiente clase: ",
                                color=GREY,
                                size = 16,
                                weight="bold"),

                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    content=f"{materia_proxima.obtener_nombre()} | Edificio: {materia_proxima.obtener_edificio()} Aula: {materia_proxima.obtener_aula()}",
                                    on_click= lambda e: mostrar_informacion_materia_vista_profesor(pagina, materia_proxima),
                                    expand=True,
                                    width=float("inf"),
                                    height=60,
                                    style=ft.ButtonStyle(
                                        bgcolor=CARD,
                                        side = ft.BorderSide(2, ft.Colors.GREY_300))
                                ),
                                ft.Icon(ft.Icons.ACCESS_TIME,
                                        color= ft.Colors.GREY_300,
                                        size=50)
                            ]
                        )
                    ]
                ),
            )
        )

    return ft.Container(
        content = ft.Column(
            boton_activo
        )
    )


def seccion_2_disponibilidad(pagina: ft.Page, usuario: Maestro):
    parte_izquiera = ft.Icon(
        ft.Icons.TIMER_OUTLINED,
        color = ft.Colors.BLACK,
        size = 120
    )

    parte_derecha = ft.Column(
        [
            ft.Text("Mi disponibilidad",
                    size = 20),

            ft.Text("Registrar disponibilidad",
                    size = 20)
        ]
    )



    integrado = ft.Container(
        content = ft.Column(
            [
            ft.Text(
                "Disponibilidad (Sección 2):",
                color = PURPLE,
                size = 16,
                italic = True,
                weight = "bold"
            ),

            ft.ElevatedButton(
                content = ft.Row(
                    [
                        parte_izquiera,
                        parte_derecha,
                    ],
                    spacing = 30
                ),
                    style = ft.ButtonStyle(
                    bgcolor = CARD,
                    side = ft.BorderSide(2, ft.Colors.AMBER_400)
                ),
                width = float("inf"),
                expand = True,
                on_click = lambda x: disponibilidad_maestro(pagina, usuario)
            )
                ]
        )
    )


    return  integrado

def seccion_3_Notificaciones(pagina: ft.Page, usuario: Maestro):

    controles = ft.Container(
        content = ft.Column(
            [

            ft.Text (
                "Notificaciones (Sección 3):",
                color = PURPLE,
                size = 16,
                italic = True,
                weight = "bold"
            ),

            ft.ElevatedButton(
                ft.Text(
                    "Cambio de Aula",
                    size = 14,
                ),
                style = ft.ButtonStyle(
                    bgcolor = CARD,
                    side = ft.BorderSide(2, ft.Colors.BLUE_300)
                ),
                width = float("inf"),
                expand = True,
                on_click = lambda x: None
            ),

    ft.ElevatedButton(
        ft.Text(
            "Solicitud de aula especian pendiente",
            size=14,
        ),
        style=ft.ButtonStyle(
            bgcolor=CARD,
            side=ft.BorderSide(2, ft.Colors.BLUE_300)
        ),
        width=float("inf"),
        expand=True,
        on_click=lambda x: None
    )
                ]
        )
    )

    return controles

def disponibilidad_maestro(pagina: ft.Page, usuario:Maestro):

    header = ft.Container(
        content = ft.Row(
            [
                ft.IconButton(
                    ft.Icons.ARROW_BACK_OUTLINED,
                    icon_color = ft.Colors.GREY_500,
                    icon_size = 40,
                    on_click = lambda event: (pagina.views.pop(), pagina.update())
                ),

                ft.Container(
                    content = ft.Text(
                        "Disponibilidad",
                        size = 30,
                        color = TEXT,
                        italic = True,
                        weight = "bold"
                    ),
                    alignment = ft.Alignment.CENTER
                )
            ],
        ),
        alignment = ft.Alignment.TOP_CENTER,
        bgcolor = CARD,
        expand = True,
    )

    disponibilidad = [[0]*7 for _ in range(7)]
    tabla_disponibilidad = ft.Container(
        content = ft.DataTable(
            columns = [
                
            ]
        )

    )

    build = ft.View(
        controls = [
            header,
        ]
    )

    pagina.views.append(build)
    pagina.update()

def notificaciones_maestro(pagina: ft.Page, usuario:Maestro):

    def notificacion_completa(notificacion):

        header_actual = crear_header()

        pagina_notificacion_completa = ft.Container(
            content = ft.Column(
                [
                    ft.Text(f"{notificacion.obtener_mensaje()}",
                            size  = 36,
                            color = TEXT,
                            )
                ]
            ),
            bgcolor = CARD,
            alignment = ft.Alignment.CENTER,
            margin=ft.Margin.symmetric(vertical=pagina.height * 0.25, horizontal=pagina.width * 0.25),
        )

        build = ft.View(
            [
                header_actual,
                pagina_notificacion_completa
            ],
            padding = 12,
            bgcolor = BG
        )






        pagina.views.append(build)
        pagina.update()


    def crear_header():
        return ft.Container(
            content=ft.Row(
                [
                    # Botón de regreso
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK_OUTLINED,  # ← icon=
                        icon_color=ft.Colors.GREY_500,
                        icon_size=40,
                        on_click=lambda event: (pagina.views.pop(), pagina.update()),
                    ),

                    # Texto centrado
                    ft.Container(
                        content=ft.Text(  # ← content=
                            "Notificaciones",
                            color=TEXT,
                            size=30,
                            italic=True,
                            weight="bold",
                        ),
                        expand=True,
                        alignment=ft.Alignment.CENTER,
                    ),

                    # Contenedor vacío para equilibrar el Row
                    ft.Container(width=48),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),

            bgcolor=CARD,
            padding=ft.Padding.only(top=40, bottom=12),
        )

    cuerpo = ft.Container(
        content = ft.Column(
            [
                
            ]
        )
    )




    header = crear_header()

    notificaciones = usuario.obtener_notifiaciones()
    cuerpo = None

    if not notificaciones:
        cuerpo = ft.Container(
            content = ft.Row(
                controls = [
                    ft.Icon(ft.Icons.NOTIFICATIONS_NONE,
                            size = 106,
                            color = PURPLE,
                            ),
                    ft.Text(
                        "No tienes alertas por el momento",
                        size = 56,
                        color = PURPLE,
                        weight = "bold",

                        )
                ],
                alignment = ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand = True,
            ),
            alignment = ft.Alignment.CENTER,
            bgcolor = CARD,
            border = ft.Border.all(2, BORDER)

        )


    else:
        cuerpo = ft.Container(
            content = ft.Column(
                controls = [
                    ft.Container(
                        content = ft.Row(
                            [ft.Icon(ft.Icons.CIRCLE_NOTIFICATIONS,
                                    size = 36,
                                    color = PURPLE,
                                    ),
                            ft.Button(
                                ft.Text(f"{notificacion.obtener_mensaje()[:15]} . . .",
                                size = 24,
                                color = PURPLE),
                                bgcolor = CARD,
                                expand = True,
                                on_click = lambda event:notificacion_completa(notificacion),
                            )

                            ],
                            alignment = ft.Alignment.CENTER_LEFT,
                        ),
                        bgcolor=CARD,
                        border=ft.Border.all(2, BORDER),

                    )for notificacion in notificaciones



                ],
                alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
                spacing = 24,
                expand = True,

            ),
            alignment = ft.Alignment.CENTER,
            margin = ft.Margin.symmetric(vertical = pagina.height * 0.25, horizontal = pagina.width * 0.25),

        )

    build = ft.View(
        [
            header,
            cuerpo
        ],
        bgcolor = BG,
        spacing = 50


    )

    pagina.views.append(build)
    pagina.update()

def perfil_maestro(pagina:ft.Page, usuario:Maestro):
    def crear_header():
        return ft.Container(
            content=ft.Row(
                [
                    # Botón de regreso
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK_OUTLINED,  # ← icon=
                        icon_color=ft.Colors.GREY_500,
                        icon_size=40,
                        on_click=lambda event: (pagina.views.pop(), pagina.update()),
                    ),

                    # Texto centrado
                    ft.Container(
                        content=ft.Text(  # ← content=
                            "Perfil",
                            color=TEXT,
                            size=30,
                            italic=True,
                            weight="bold",
                        ),
                        expand=True,
                        alignment=ft.Alignment.CENTER,
                    ),

                    # Contenedor vacío para equilibrar el Row
                    ft.Container(width=48),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),

            bgcolor=CARD,
            padding=ft.Padding.only(top=40, bottom=12),
        )

    header = crear_header()


    build = ft.View(
        [
            header,
        ],
        padding = 20,
        bgcolor = BG,

    )

    pagina.views.append(build)



def interfaz_alumno(pagina: ft.Page, usuario: Alumno, db_materias: list[Materia]):

    #  CONFIGURACION
    pagina.title = "SIGHA - Alumno"
    pagina.bgcolor = "#0f172a"
    pagina.padding = 15
    pagina.scroll = ft.ScrollMode.AUTO
    pagina.vertical_alignment = ft.MainAxisAlignment.START

    pagina.clean()

    #  COLORES
    COLOR_FONDO = "#0f172a"
    COLOR_CARD = "#1e293b"
    COLOR_PRIMARIO = "#c084fc"
    COLOR_SECUNDARIO = "#f472b6"
    COLOR_TEXTO = "white"
    COLOR_GRIS = "#94a3b8"

    #  ALERTAS
    if not hasattr(usuario, "notificaciones"):
        usuario.notificaciones = []

    #  CAMBIO PANTALLA
    def cambiar_pantalla(vista):
        pagina.clean()
        vista()
        pagina.update()

    #  NOTIFICACION PUSH SIMULADA
    def enviar_notificacion(
            titulo,
            mensaje
    ):

        pagina.snack_bar = ft.SnackBar(

            bgcolor=COLOR_CARD,

            content=ft.Row(
                controls=[

                    ft.Icon(
                        ft.Icons.NOTIFICATIONS,
                        color=COLOR_PRIMARIO
                    ),

                    ft.Column(
                        controls=[

                            ft.Text(
                                titulo,
                                color="white",
                                weight="bold"
                            ),

                            ft.Text(
                                mensaje,
                                color="white"
                            )
                        ]
                    )
                ]
            )
        )

        pagina.snack_bar.open = True
        pagina.update()

    #  FUNCIONES ALERTAS
    def agregar_alerta(materia):

        if materia not in usuario.notificaciones:

            usuario.notificaciones.append(materia)

            enviar_notificacion(
                "Alerta activada",

                f"{materia.obtener_nombre()} | "
                f"{materia.obtener_codigo()}"
            )

        cambiar_pantalla(mostrar_alertas)

    def eliminar_alerta(materia):

        if materia in usuario.notificaciones:

            usuario.notificaciones.remove(materia)

            enviar_notificacion(
                "Alerta eliminada",
                materia.obtener_nombre()
            )

        cambiar_pantalla(mostrar_alertas)

    #  SIMULAR CUPO DISPONIBLE
    def simular_cupo(materia):

        enviar_notificacion(

            "¡Cupo disponible!",

            f"{materia.obtener_nombre()} | "
            f"{materia.obtener_codigo()} | "
            f"Aula: {materia.obtener_aula()}"
        )

    #  PERFIL
    def mostrar_perfil():

        pagina.clean()

        informacion_usuario = ft.Container(
            bgcolor=COLOR_CARD,
            border_radius=20,
            padding=20,

            content=ft.Column(
                controls=[

                    ft.Icon(
                        ft.Icons.ACCOUNT_CIRCLE,
                        size=100,
                        color=COLOR_PRIMARIO
                    ),

                    ft.Text(
                        usuario.nombre.obtenerNombre(),
                        size=26,
                        weight="bold",
                        color="white"
                    ),

                    ft.Text(
                        usuario.obtener_carrera(),
                        size=16,
                        color=COLOR_GRIS
                    ),

                    ft.Divider(color="transparent"),

                    ft.Text(
                        f"Matrícula: {usuario.obtener_matricula()}",
                        color="white"
                    ),

                    ft.Text(
                        f"Semestre: {usuario.obtener_semestre()}",
                        color="white"
                    ),

                    ft.Text(
                        f"Promedio General: {usuario.obtener_promedio_general()}",
                        color="white"
                    ),

                    ft.Text(
                        f"Créditos Obtenidos: {usuario.obtener_creditos_obtenidos()}",
                        color="white"
                    ),
                ],

                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

        pagina.add(
            ft.Column(
                controls=[

                    ft.Row(
                        controls=[

                            ft.IconButton(
                                icon=ft.Icons.ARROW_BACK,
                                icon_color="white",
                                on_click=lambda _: cambiar_pantalla(
                                    mostrar_home
                                )
                            ),

                            ft.Text(
                                "Mi Perfil",
                                size=22,
                                weight="bold",
                                color="white"
                            )
                        ]
                    ),

                    ft.Container(height=20),

                    informacion_usuario
                ]
            )
        )

    #  HOME
    def mostrar_home():

        pagina.clean()

        parte_superior = ft.Row(
            controls=[

                ft.Column(
                    controls=[

                        ft.Text(
                            f"Hola, {usuario.nombre.obtenerNombre()}",
                            size=24,
                            weight="bold",
                            color=COLOR_TEXTO
                        ),

                        ft.Text(
                            f"{usuario.obtener_carrera()} • "
                            f"{usuario.obtener_semestre()}° semestre",
                            size=14,
                            color=COLOR_GRIS
                        )
                    ],
                    spacing=2
                ),

                ft.Container(expand=True),

                ft.IconButton(
                    icon=ft.Icons.ACCOUNT_CIRCLE,
                    icon_color=COLOR_PRIMARIO,
                    icon_size=50,
                    on_click=lambda _: cambiar_pantalla(
                        mostrar_perfil
                    )
                )
            ]
        )

        buscador = ft.Container(
            bgcolor=COLOR_CARD,
            border_radius=20,
            padding=15,

            on_click=lambda _: cambiar_pantalla(
                mostrar_busqueda
            ),

            content=ft.Row(
                controls=[

                    ft.Icon(
                        ft.Icons.SEARCH,
                        color=COLOR_GRIS
                    ),

                    ft.Text(
                        "Buscar materia...",
                        color=COLOR_GRIS
                    )
                ]
            )
        )

        alertas_texto = (
            f"{len(usuario.notificaciones)} alertas activas"
            if usuario.notificaciones
            else "No tienes alertas activas"
        )

        seccion_alertas = ft.Container(
            bgcolor=COLOR_CARD,
            border_radius=20,
            padding=15,

            on_click=lambda _: cambiar_pantalla(
                mostrar_alertas
            ),

            content=ft.Column(
                controls=[

                    ft.Text(
                        "Mis Alertas",
                        color=COLOR_PRIMARIO,
                        weight="bold"
                    ),

                    ft.Text(
                        alertas_texto,
                        color=COLOR_GRIS
                    )
                ]
            )
        )

        tarjeta_simulador = ft.Container(
            bgcolor=COLOR_CARD,
            border_radius=20,
            padding=20,

            content=ft.Row(
                controls=[

                    ft.Icon(
                        ft.Icons.CALENDAR_MONTH,
                        color=COLOR_PRIMARIO,
                        size=40
                    ),

                    ft.Container(width=20),

                    ft.Column(
                        controls=[

                            ft.Text(
                                "Ver posibles traslapes",
                                color="white"
                            ),

                            ft.ElevatedButton(
                                "Ir al simulador",
                                bgcolor=COLOR_PRIMARIO,
                                color="white",

                                on_click=lambda _: cambiar_pantalla(
                                    mostrar_simulador
                                )
                            )
                        ]
                    )
                ]
            )
        )

        navbar = ft.Container(
            bgcolor=COLOR_CARD,
            border_radius=20,
            padding=10,

            content=ft.Row(
                controls=[

                    ft.IconButton(
                        icon=ft.Icons.HOME,
                        icon_color=COLOR_PRIMARIO,
                        on_click=lambda _: cambiar_pantalla(
                            mostrar_home
                        )
                    ),

                    ft.IconButton(
                        icon=ft.Icons.SEARCH,
                        icon_color="white",
                        on_click=lambda _: cambiar_pantalla(
                            mostrar_busqueda
                        )
                    ),

                    ft.IconButton(
                        icon=ft.Icons.NOTIFICATIONS,
                        icon_color="white",
                        on_click=lambda _: cambiar_pantalla(
                            mostrar_alertas
                        )
                    ),

                    ft.IconButton(
                        icon=ft.Icons.PERSON,
                        icon_color="white",
                        on_click=lambda _: cambiar_pantalla(
                            mostrar_perfil
                        )
                    )
                ],

                alignment=ft.MainAxisAlignment.SPACE_AROUND
            )
        )

        pagina.add(
            ft.Column(
                controls=[
                    parte_superior,
                    ft.Container(height=20),
                    buscador,
                    ft.Container(height=20),
                    seccion_alertas,
                    ft.Container(height=20),
                    tarjeta_simulador,
                    ft.Container(height=20),
                    navbar
                ]
            )
        )

    #  BUSQUEDA
    def mostrar_busqueda():

        pagina.clean()

        lista_resultados = ft.Column()

        def abrir_detalles(materia):

            pagina.clean()

            pagina.add(

                ft.Column(
                    controls=[

                        ft.Row(
                            controls=[

                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    icon_color="white",

                                    on_click=lambda _:
                                    cambiar_pantalla(
                                        mostrar_busqueda
                                    )
                                ),

                                ft.Text(
                                    "Detalles Materia",
                                    color="white",
                                    size=22,
                                    weight="bold"
                                )
                            ]
                        ),

                        ft.Container(height=20),

                        ft.Container(

                            bgcolor=COLOR_CARD,
                            border_radius=20,
                            padding=20,

                            content=ft.Column(
                                controls=[

                                    ft.Text(
                                        materia.obtener_nombre(),
                                        size=24,
                                        color="white",
                                        weight="bold"
                                    ),

                                    ft.Text(
                                        f"Código: {materia.obtener_codigo()}",
                                        color=COLOR_GRIS
                                    ),

                                    ft.Text(
                                        f"Facultad: {materia.obtener_facultad()}",
                                        color="white"
                                    ),

                                    ft.Text(
                                        f"Aula: {materia.obtener_aula()}",
                                        color="white"
                                    ),

                                    ft.Text(
                                        f"Edificio: {materia.obtener_edificio()}",
                                        color="white"
                                    ),

                                    ft.Text(
                                        f"Créditos: {materia.obtener_creditos()}",
                                        color="white"
                                    ),

                                    ft.Text(
                                        "Días:",
                                        color=COLOR_PRIMARIO,
                                        weight="bold"
                                    ),

                                    ft.Text(
                                        ", ".join(
                                            materia.obtener_dias_clase()
                                        ),
                                        color="white"
                                    ),

                                    ft.Text(
                                        f"Horario: "
                                        f"{materia.obtenerHoraInicio().hora}"
                                        f" - "
                                        f"{materia.obtenerHoraFin().hora}",
                                        color="white"
                                    ),

                                    ft.Container(height=10),

                                    ft.ElevatedButton(

                                        "Agregar alerta",

                                        bgcolor=COLOR_SECUNDARIO,

                                        on_click=lambda _:
                                        agregar_alerta(
                                            materia
                                        )
                                    ),

                                    ft.ElevatedButton(

                                        "Simular cupo disponible",

                                        bgcolor=COLOR_PRIMARIO,

                                        color="white",

                                        on_click=lambda _:
                                        simular_cupo(
                                            materia
                                        )
                                    )
                                ]
                            )
                        )
                    ]
                )
            )

        def buscar(e):

            texto = campo_busqueda.value.lower()
            lista_resultados.controls.clear()

            resultados = []

            for materia in db_materias:

                coincide = (

                    texto in materia.obtener_nombre().lower()
                    or texto in materia.obtener_codigo().lower()
                    or texto in materia.obtener_facultad().lower()
                    or texto in materia.obtener_edificio().lower()
                    or any(
                        texto in dia.lower()
                        for dia in materia.obtener_dias_clase()
                    )
                )

                if coincide:
                    resultados.append(materia)

            for materia in resultados:

                tarjeta = ft.Container(
                    bgcolor=COLOR_CARD,
                    border_radius=15,
                    padding=15,

                    on_click=lambda _, m=materia:
                    abrir_detalles(m),

                    content=ft.Column(
                        controls=[

                            ft.Text(
                                materia.obtener_nombre(),
                                color="white",
                                size=18,
                                weight="bold"
                            ),

                            ft.Text(
                                f"Código: {materia.obtener_codigo()}",
                                color=COLOR_GRIS
                            ),

                            ft.Text(
                                f"Aula: {materia.obtener_aula()}",
                                color=COLOR_GRIS
                            ),

                            ft.Text(
                                f"Días: {', '.join(materia.obtener_dias_clase())}",
                                color=COLOR_GRIS
                            ),
                        ]
                    )
                )

                lista_resultados.controls.append(tarjeta)

            pagina.update()

        campo_busqueda = ft.TextField(
            label="Buscar materia",
            border_color=COLOR_PRIMARIO,
            color="white",

            hint_text="Nombre, código, facultad, días...",

            on_change=buscar
        )

        pagina.add(
            ft.Column(
                controls=[

                    ft.Row(
                        controls=[

                            ft.IconButton(
                                icon=ft.Icons.ARROW_BACK,
                                icon_color="white",
                                on_click=lambda _: cambiar_pantalla(
                                    mostrar_home
                                )
                            ),

                            ft.Text(
                                "Buscar Materias",
                                color="white",
                                size=22,
                                weight="bold"
                            )
                        ]
                    ),

                    campo_busqueda,
                    lista_resultados
                ]
            )
        )

    #  ALERTAS
    def mostrar_alertas():

        pagina.clean()

        lista_alertas = ft.Column()

        if usuario.notificaciones:

            for materia in usuario.notificaciones:

                tarjeta = ft.Container(
                    bgcolor=COLOR_CARD,
                    border_radius=15,
                    padding=15,

                    content=ft.Column(
                        controls=[

                            ft.Text(
                                materia.obtener_nombre(),
                                color="white",
                                size=18,
                                weight="bold"
                            ),

                            ft.Text(
                                materia.obtener_codigo(),
                                color=COLOR_GRIS
                            ),

                            ft.Row(
                                controls=[

                                    ft.ElevatedButton(
                                        "Eliminar alerta",
                                        bgcolor="red",
                                        color="white",

                                        on_click=lambda _, m=materia:
                                        eliminar_alerta(m)
                                    ),

                                    ft.ElevatedButton(
                                        "Simular cupo",
                                        bgcolor=COLOR_PRIMARIO,
                                        color="white",

                                        on_click=lambda _, m=materia:
                                        simular_cupo(m)
                                    )
                                ]
                            )
                        ]
                    )
                )

                lista_alertas.controls.append(tarjeta)

        else:

            lista_alertas.controls.append(
                ft.Text(
                    "No tienes alertas activas",
                    color=COLOR_GRIS
                )
            )

        pagina.add(
            ft.Column(
                controls=[

                    ft.Row(
                        controls=[

                            ft.IconButton(
                                icon=ft.Icons.ARROW_BACK,
                                icon_color="white",
                                on_click=lambda _: cambiar_pantalla(
                                    mostrar_home
                                )
                            ),

                            ft.Text(
                                "Mis Alertas",
                                color="white",
                                size=22,
                                weight="bold"
                            )
                        ]
                    ),

                    lista_alertas
                ]
            )
        )

    #  SIMULADOR
    def mostrar_simulador():

        pagina.clean()

        dias = [
            "Lunes",
            "Martes",
            "Miércoles",
            "Jueves",
            "Viernes"
        ]

        horas = list(range(7, 22))

        colores = [
            "#c084fc",
            "#f472b6",
            "#0ea5e9",
            "#22c55e",
            "#f59e0b",
            "#ef4444"
        ]

        def crear_celda(
                texto="",
                color=COLOR_CARD
        ):

            return ft.Container(
                width=110,
                height=60,
                bgcolor=color,
                border_radius=10,

                border=ft.border.all(
                    1,
                    "#334155"
                ),

                alignment=ft.Alignment(0, 0),

                content=ft.Text(
                    texto,
                    color="white",
                    size=10,
                    text_align=ft.TextAlign.CENTER,
                    weight="bold"
                )
            )

        tabla = []

        #  ENCABEZADO
        encabezado = ft.Row(
            controls=[

                crear_celda(
                    "Hora",
                    COLOR_PRIMARIO
                )

            ] +

            [

                crear_celda(
                    dia,
                    COLOR_PRIMARIO
                )

                for dia in dias
            ]
        )

        tabla.append(encabezado)

        #  FILAS HORARIO
        for hora in horas:

            fila = [

                crear_celda(
                    f"{hora}:00",
                    "#334155"
                )
            ]

            for dia in dias:

                texto = ""
                color = COLOR_CARD

                conflictos = 0

                for indice, materia in enumerate(
                    usuario.obtener_materias_actuales()
                ):

                    dias_materia = (
                        materia.obtener_dias_clase()
                    )

                    hora_inicio = int(
                        str(materia.obtenerHoraInicio().hora).split(":")[0]
                    )

                    hora_fin = int(
                        str(materia.obtenerHoraFin().hora).split(":")[0]
                    )

                    if (
                        dia in dias_materia
                        and hora >= hora_inicio
                        and hora < hora_fin
                    ):

                        conflictos += 1

                        texto = (
                            f"{materia.obtener_nombre()}\n"
                            f"{materia.obtener_aula()}"
                        )

                        color = colores[
                            indice % len(colores)
                        ]

                #  DETECTAR CONFLICTOS
                if conflictos > 1:
                    color = "red"
                    texto = "⚠ CONFLICTO"

                fila.append(
                    crear_celda(
                        texto,
                        color
                    )
                )

            tabla.append(
                ft.Row(
                    controls=fila
                )
            )

        pagina.add(

            ft.Column(
                controls=[

                    ft.Row(
                        controls=[

                            ft.IconButton(
                                icon=ft.Icons.ARROW_BACK,
                                icon_color="white",

                                on_click=lambda _:
                                cambiar_pantalla(
                                    mostrar_home
                                )
                            ),

                            ft.Text(
                                "Simulador",
                                color="white",
                                size=22,
                                weight="bold"
                            )
                        ]
                    ),

                    ft.Container(height=10),

                    ft.Column(
                        controls=tabla,
                        scroll=ft.ScrollMode.AUTO
                    ),

                    ft.Container(height=20),

                    ft.Row(
                        controls=[

                            ft.Text(
                                "⚠",
                                color="red",
                                size=20,
                                weight="bold"
                            ),

                            ft.Text(
                                "Indica conflicto entre materias",
                                color="white"
                            )
                        ]
                    )
                ]
            )
        )

    #  INICIO
    mostrar_home()



def interfaz_administrador(
        pagina: ft.Page,
        usuario: Administrador,
        db_materias: list[Materia],
        db_alumnos: list[Alumno],
        db_maestros: list[Maestro]
):

    #  CONFIGURACIÓN 

    pagina.title = "SIGHA - Administrador"
    pagina.bgcolor = "#0f172a"
    pagina.padding = 15
    pagina.scroll = ft.ScrollMode.AUTO

    pagina.clean()

    #  COLORES 

    COLOR_FONDO = "#0f172a"
    COLOR_CARD = "#1e293b"
    COLOR_PRIMARIO = "#c084fc"
    COLOR_SECUNDARIO = "#f472b6"
    COLOR_TEXTO = "white"
    COLOR_GRIS = "#94a3b8"
    COLOR_WARNING = "#f59e0b"

    #  MÉTRICAS 

    total_alertas = 0

    for alumno in db_alumnos:
        total_alertas += len(alumno.notificaciones)

    total_usuarios = (
        len(db_alumnos)
        + len(db_maestros)
    )

    total_materias = len(db_materias)

    #  CAMBIO DE PANTALLA 

    def cambiar_pantalla(vista):

        pagina.clean()
        vista()
        pagina.update()

    #  SELECTOR GLOBAL 

    selector_materia = ft.Dropdown(
        width=350,
        label="Seleccionar materia",
        options=[
            ft.dropdown.Option(
                materia.obtener_nombre()
            )
            for materia in db_materias
        ]
    )

    #  PERFIL 

    def mostrar_perfil():

        pagina.clean()

        parte_superior = ft.Row(
            controls=[

                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_color="white",
                    on_click=lambda _: cambiar_pantalla(
                        mostrar_home
                    )
                ),

                ft.Container(expand=True),

                ft.Text(
                    "Perfil Administrador",
                    size=22,
                    weight="bold",
                    color="white"
                ),

                ft.Container(expand=True)
            ]
        )

        informacion = ft.Container(
            bgcolor=COLOR_CARD,
            border_radius=20,
            padding=20,

            content=ft.Column(
                controls=[

                    ft.Icon(
                        ft.Icons.ADMIN_PANEL_SETTINGS,
                        size=100,
                        color=COLOR_PRIMARIO
                    ),

                    ft.Text(
                        usuario.nombre.obtenerNombre(),
                        size=26,
                        weight="bold",
                        color="white"
                    ),

                    ft.Text(
                        usuario.obtener_rango(),
                        size=16,
                        color=COLOR_GRIS
                    ),

                    ft.Divider(color="transparent"),

                    ft.Text(
                        f"Correo: {usuario.obtenerCorreo()}",
                        color="white"
                    ),

                    ft.Text(
                        f"Teléfono: {usuario.obtenerNumeroTelefono()}",
                        color="white"
                    ),

                    ft.Text(
                        f"Estado: {usuario.obtenerEstado()}",
                        color="white"
                    ),

                    ft.Text(
                        f"Rol: {usuario.obtenerRol()}",
                        color="white"
                    ),

                    ft.Text(
                        f"ID: {usuario.obtenerIdentificacion()}",
                        color="white"
                    ),
                ],

                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

        pagina.add(
            ft.Column(
                controls=[
                    parte_superior,
                    ft.Container(height=20),
                    informacion
                ]
            )
        )

    #  REPORTES 

    def generar_reporte(e):

        pagina.snack_bar = ft.SnackBar(
            content=ft.Text(
                "Reporte PDF y CSV generado correctamente"
            )
        )

        pagina.snack_bar.open = True
        pagina.update()

    #  SIMULAR LIBERACIÓN 

    def simular_liberacion(e):

        materia_nombre = selector_materia.value

        if not materia_nombre:

            pagina.snack_bar = ft.SnackBar(
                content=ft.Text(
                    "Selecciona una materia"
                )
            )

            pagina.snack_bar.open = True
            pagina.update()

            return

        for materia in db_materias:

            if (
                materia.obtener_nombre()
                == materia_nombre
            ):

                materia.cupos_disponibles += 1

                usuario.notificaciones.append(
                    f"Prueba realizada por admin en "
                    f"{materia.obtener_nombre()}"
                )

                pagina.snack_bar = ft.SnackBar(
                    content=ft.Text(
                        f"Cupo liberado en "
                        f"{materia.obtener_nombre()}"
                    )
                )

                pagina.snack_bar.open = True
                pagina.update()

                return

    #  ANALYTICS 

    def mostrar_analytics():

        pagina.clean()

        parte_superior = ft.Row(
            controls=[

                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_color="white",
                    on_click=lambda _: cambiar_pantalla(
                        mostrar_home
                    )
                ),

                ft.Container(expand=True),

                ft.Text(
                    "Analytics",
                    size=24,
                    weight="bold",
                    color="white"
                ),

                ft.Container(expand=True)
            ]
        )

        # TOP MATERIAS

        materias_ordenadas = sorted(
            db_materias,
            key=lambda m: len(m.alumnos),
            reverse=True
        )

        top_materias_controls = []

        for materia in materias_ordenadas[:5]:

            porcentaje = 0

            if materia.cupos_totales > 0:

                porcentaje = (
                    len(materia.alumnos)
                    / materia.cupos_totales
                )

            top_materias_controls.extend([

                ft.Text(
                    materia.obtener_nombre(),
                    color="white"
                ),

                ft.ProgressBar(
                    value=porcentaje,
                    color=COLOR_PRIMARIO,
                    bgcolor="#334155"
                ),

                ft.Text(
                    f"{len(materia.alumnos)} alumnos inscritos",
                    color=COLOR_GRIS,
                    size=12
                ),

                ft.Container(height=10)
            ])

        # HORARIOS CRÍTICOS

        horarios = {}

        for materia in db_materias:

            clave = (
                f"{materia.obtenerHoraInicio()} - "
                f"{materia.obtenerHoraFin()}"
            )

            if clave not in horarios:
                horarios[clave] = 0

            horarios[clave] += len(materia.alumnos)

        horarios_criticos = sorted(
            horarios.items(),
            key=lambda x: x[1],
            reverse=True
        )

        horarios_controls = []

        for horario, demanda in horarios_criticos[:5]:

            horarios_controls.append(

                ft.Row(
                    controls=[

                        ft.Text(
                            horario,
                            color="white"
                        ),

                        ft.Container(expand=True),

                        ft.Text(
                            f"{demanda} alumnos",
                            color=COLOR_WARNING
                        )
                    ]
                )
            )

        # ESTUDIANTES CON MÁS ALERTAS

        top_estudiantes = sorted(
            db_alumnos,
            key=lambda a: len(a.notificaciones),
            reverse=True
        )

        alertas_controls = []

        for alumno in top_estudiantes[:5]:

            alertas_controls.append(

                ft.Row(
                    controls=[

                        ft.Text(
                            alumno.obtenerNombre().obtenerNombre(),
                            color="white"
                        ),

                        ft.Container(expand=True),

                        ft.Text(
                            f"{len(alumno.notificaciones)} alertas",
                            color=COLOR_SECUNDARIO
                        )
                    ]
                )
            )

        # OCUPACIÓN

        ocupacion_controls = []

        for materia in db_materias[:5]:

            porcentaje = 0

            if materia.cupos_totales > 0:

                porcentaje = (
                    len(materia.alumnos)
                    / materia.cupos_totales
                )

            ocupacion_controls.extend([

                ft.Text(
                    materia.obtener_nombre(),
                    color="white"
                ),

                ft.ProgressBar(
                    value=porcentaje,
                    color="#22c55e",
                    bgcolor="#334155"
                ),

                ft.Text(
                    f"{int(porcentaje * 100)}% ocupado",
                    color=COLOR_GRIS
                ),

                ft.Container(height=10)
            ])

        pagina.add(

            ft.Column(
                controls=[

                    parte_superior,

                    ft.Container(height=20),

                    ft.Container(
                        bgcolor=COLOR_CARD,
                        border_radius=20,
                        padding=20,

                        content=ft.Column(
                            controls=[

                                ft.Text(
                                    "Top Materias",
                                    size=18,
                                    weight="bold",
                                    color="white"
                                ),

                                *top_materias_controls
                            ]
                        )
                    ),

                    ft.Container(height=20),

                    ft.Container(
                        bgcolor=COLOR_CARD,
                        border_radius=20,
                        padding=20,

                        content=ft.Column(
                            controls=[

                                ft.Text(
                                    "Horarios Críticos",
                                    size=18,
                                    weight="bold",
                                    color="white"
                                ),

                                *horarios_controls
                            ]
                        )
                    ),

                    ft.Container(height=20),

                    ft.Container(
                        bgcolor=COLOR_CARD,
                        border_radius=20,
                        padding=20,

                        content=ft.Column(
                            controls=[

                                ft.Text(
                                    "Estudiantes con más alertas",
                                    size=18,
                                    weight="bold",
                                    color="white"
                                ),

                                *alertas_controls
                            ]
                        )
                    ),

                    ft.Container(height=20),

                    ft.Container(
                        bgcolor=COLOR_CARD,
                        border_radius=20,
                        padding=20,

                        content=ft.Column(
                            controls=[

                                ft.Text(
                                    "Uso de aulas",
                                    size=18,
                                    weight="bold",
                                    color="white"
                                ),

                                *ocupacion_controls
                            ]
                        )
                    )
                ]
            )
        )

        pagina.update()

    #  HOME 

    def mostrar_home():

        pagina.clean()

        parte_superior = ft.Row(
            controls=[

                ft.Column(
                    controls=[

                        ft.Text(
                            "Administración",
                            size=28,
                            weight="bold",
                            color="white"
                        ),

                        ft.Text(
                            usuario.obtener_rango(),
                            size=14,
                            color=COLOR_GRIS
                        )
                    ]
                ),

                ft.Container(expand=True),

                ft.IconButton(
                    icon=ft.Icons.ADMIN_PANEL_SETTINGS,
                    icon_color=COLOR_PRIMARIO,
                    icon_size=50,
                    on_click=lambda _: cambiar_pantalla(
                        mostrar_perfil
                    )
                )
            ]
        )

        # MÉTRICAS

        metricas = ft.Row(
            controls=[

                ft.Container(
                    expand=True,
                    bgcolor=COLOR_CARD,
                    border_radius=20,
                    padding=15,

                    content=ft.Column(
                        controls=[

                            ft.Icon(
                                ft.Icons.NOTIFICATIONS,
                                color=COLOR_SECUNDARIO,
                                size=35
                            ),

                            ft.Text(
                                str(total_alertas),
                                size=24,
                                weight="bold",
                                color="white"
                            ),

                            ft.Text(
                                "Alertas activas",
                                color=COLOR_GRIS
                            )
                        ],

                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                ),

                ft.Container(
                    expand=True,
                    bgcolor=COLOR_CARD,
                    border_radius=20,
                    padding=15,

                    content=ft.Column(
                        controls=[

                            ft.Icon(
                                ft.Icons.PEOPLE,
                                color=COLOR_PRIMARIO,
                                size=35
                            ),

                            ft.Text(
                                str(total_usuarios),
                                size=24,
                                weight="bold",
                                color="white"
                            ),

                            ft.Text(
                                "Usuarios activos",
                                color=COLOR_GRIS
                            )
                        ],

                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                ),

                ft.Container(
                    expand=True,
                    bgcolor=COLOR_CARD,
                    border_radius=20,
                    padding=15,

                    content=ft.Column(
                        controls=[

                            ft.Icon(
                                ft.Icons.MENU_BOOK,
                                color="#22c55e",
                                size=35
                            ),

                            ft.Text(
                                str(total_materias),
                                size=24,
                                weight="bold",
                                color="white"
                            ),

                            ft.Text(
                                "Materias",
                                color=COLOR_GRIS
                            )
                        ],

                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                )
            ]
        )

        # BOTONES

        botones = ft.Column(
            controls=[

                ft.ElevatedButton(
                    "Generar Reporte",
                    bgcolor=COLOR_SECUNDARIO,
                    color="black",
                    height=50,
                    width=300,
                    on_click=generar_reporte
                ),

                ft.ElevatedButton(
                    "Simular Liberación de Cupos",
                    bgcolor=COLOR_PRIMARIO,
                    color="white",
                    height=50,
                    width=300,
                    on_click=simular_liberacion
                )
            ],

            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        )

        # NAVBAR

        navbar = ft.Container(
            bgcolor=COLOR_CARD,
            border_radius=20,
            padding=10,

            content=ft.Row(
                controls=[

                    ft.IconButton(
                        icon=ft.Icons.HOME,
                        icon_color=COLOR_PRIMARIO,
                        on_click=lambda _: cambiar_pantalla(
                            mostrar_home
                        )
                    ),

                    ft.IconButton(
                        icon=ft.Icons.BAR_CHART,
                        icon_color="white",
                        on_click=lambda _: cambiar_pantalla(
                            mostrar_analytics
                        )
                    ),

                    ft.IconButton(
                        icon=ft.Icons.NOTIFICATIONS,
                        icon_color="white"
                    ),

                    ft.IconButton(
                        icon=ft.Icons.PERSON,
                        icon_color="white",
                        on_click=lambda _: cambiar_pantalla(
                            mostrar_perfil
                        )
                    )
                ],

                alignment=ft.MainAxisAlignment.SPACE_AROUND
            )
        )

        pagina.add(

            ft.Column(
                controls=[

                    parte_superior,

                    ft.Container(height=20),

                    metricas,

                    ft.Container(height=25),

                    botones,

                    ft.Container(height=15),

                    selector_materia,

                    ft.Container(height=25),

                    navbar
                ]
            )
        )

        pagina.update()

    #  INICIO 

    mostrar_home()