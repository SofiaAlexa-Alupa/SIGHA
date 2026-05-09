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