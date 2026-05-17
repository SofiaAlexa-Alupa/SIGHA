from pathlib import Path

import flet as ft
from datetime import datetime
import calendar
from fecha import Fecha
from alertas import Alerta
from hora import Hora
from maestro import Maestro
from alumno import Alumno
from materia import Materia
from administrador import Administrador
from fpdf import FPDF
import platform
import os

BG      = "#0f172a"   # Fondo oscuro principal
CARD    = "#1e293b"   # Fondo de las tarjetas
PURPLE  = "#7c3aed"   # Morado para acentos
PURPLE_MIDNIGHT = "#280137"
TEXT    = "#white"   # Texto blanco
TEXT_SECONDARY = "#94a3b8"   # Texto gris secundario
BORDER = "#818cf8"
PRIMARY = "#c084fc"
SECONDARY = "#f472b6"





def login(pagina: ft.Page):
     pagina.bg = BG
     pagina.title = "Inicio de sesion"
     pagina.padding = 0
     pagina.vertical_alignment = ft.MainAxisAlignment.CENTER
     pagina.horizontal_alignment = ft.CrossAxisAlignment.CENTER

     usuario = None
     contraseña = None

     codigo_usuario = ft.TextField(
         label="Ingrese su codigo",
         border_color=SECONDARY,
         focused_border_color=PRIMARY,
         border_radius=2,
         color=TEXT,
         bgcolor=CARD,
         width=350
     )

     contraseña_usuario = ft.TextField(
         label="Ingrese su contraseña",
         border_color=SECONDARY,
         focused_border_color=PRIMARY,
         border_radius=2,
         color=TEXT,
         bgcolor=CARD,
         password=True,
         can_reveal_password=True,
         width=350
     )

     boton_continuar = ft.ElevatedButton(
         "continuar",
         on_click=lambda e: accion_continuar(),
         style=ft.ButtonStyle(
             color=SECONDARY,
             shape=ft.RoundedRectangleBorder(radius=10),
             bgcolor=PURPLE_MIDNIGHT,
         )

     )

     build = ft.Container(
         content=ft.Column(
             controls=[
                 ft.Text("Login",
                         color = TEXT_SECONDARY,
                         size = 14),

                 codigo_usuario,
                 contraseña_usuario,
                 boton_continuar
             ],
             spacing=10,
             alignment=ft.MainAxisAlignment.CENTER,
             horizontal_alignment=ft.CrossAxisAlignment.CENTER,

         ),
         alignment=ft.Alignment.CENTER,
         expand=True,
         margin=36
     )

     pagina.add(build)


     def accion_continuar():
        campos_validos = True
        contraseña_usuario.error = None
        codigo_usuario.error = None

        if not contraseña_usuario.value:
            contraseña_usuario.error = "Ingrese una contraseñá valida"
            campos_validos = False

        if not codigo_usuario.value:
            codigo_usuario.error = "Ingrese un codigo valido"
            campos_validos = False

        if campos_validos:
            pass
            #Aqui se integra la base de datos


        pagina.update()

def interfaz_maestro_nueva(pagina: ft.Page, usuario: Maestro):

    pagina.vertical_alignment = ft.MainAxisAlignment.START
    pagina.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    pagina.scroll = None
    pagina.window_prevent_close = True

    cabezera = ft.Container(
        content = ft.Row(
            controls = [
                ft.Column(
                    controls = [
                        ft.Text(f"Hola, {usuario.obtenerNombre()}",
                                color = TEXT,
                                size = 16,
                                weight = ft.FontWeight.BOLD,
                                ),
                        ft.Text(f"{usuario.obtener_departamento()}"),
                    ],
                    spacing=2,
                ),

                ft.Icon(ft.Icons.ACCOUNT_CIRCLE_OUTLINED,
                        color = ft.Colors.RED_ACCENT,
                        size = 64)

            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment= ft.CrossAxisAlignment.CENTER,
            expand = True
        ),

        alignment = ft.Alignment.TOP_CENTER,
        bgcolor = CARD,
        padding = ft.Padding.all(10)
    )

    seccion_1 = seccion_1_maestro(pagina, usuario)
    seccion_2 = seccion_2_Disponibilidad(pagina, usuario)
    seccion_3 = seccion_3_Notificaciones(pagina, usuario)

    hogar = ft.Container(
        content = ft.Column(
            [
                cabezera,
                seccion_1,
                seccion_2,
                seccion_3,
            ]
        ),
        alignment = ft.Alignment.TOP_CENTER,
    )

    vistas_manager = ft.Container(content = hogar, expand = True)


    def cambio_pagina(event):
        opcion = event.control.selected_index
        print(opcion)

        if opcion == 0:
            vistas_manager.content = hogar
        elif opcion == 1:
            vistas_manager.content = pagina_materias(pagina, usuario)
        elif opcion == 2:
            vistas_manager.content = pagina_notificaciones(pagina, usuario)
        elif opcion == 3:
            vistas_manager.content = pagina_perfil(pagina, usuario)


        vistas_manager.update()
        pagina.update()




    barra_navegacion = ft.NavigationBar(
        bgcolor = CARD,
        selected_index = 0,
        on_change = cambio_pagina,

        destinations = [
            ft.NavigationBarDestination(
                icon =  ft.Icons.HOME_OUTLINED,
                selected_icon = ft.Icons.HOME,
                label = "Inicio"
            ),
            ft.NavigationBarDestination(
                icon = ft.Icons.CALENDAR_MONTH_OUTLINED,
                selected_icon = ft.Icons.CALENDAR_MONTH,
                label = "Materias"
            ),
            ft.NavigationBarDestination(
                icon = ft.Icons.NOTIFICATIONS_OUTLINED,
                selected_icon = ft.Icons.NOTIFICATIONS,
                label = "Notificaciones"
            ),
            ft.NavigationBarDestination(
                icon = ft.Icons.PERSON_OUTLINE,
                selected_icon = ft.Icons.PERSON,
                label = "Perfil"
            )

        ]
    )
    pagina.navigation_bar = barra_navegacion
    pagina.add(vistas_manager)

def seccion_1_maestro(pagina: ft.Page, usuario:Maestro):
    materia_actual, materia_siguiente = filtrar_materia_hoy(usuario)

    materia_actual= Materia()
    materia_siguiente = Materia()

    alumno = Alumno()

    for i in range(0, 100):
        materia_actual.agregar_alumno(alumno)
    boton_materia_actual = None
    boton_materia_siguiente = None

    header = ft.Text("Seccion 1: Mis alertas clase",
                     color = PURPLE,
                     weight = ft.FontWeight.BOLD,
                     size = 16)

    if materia_actual is None:
        return ft.Container(
            content = ft.Column(
                controls = [
                    header,

                    ft.Container(content = ft.Text("No tienes mas clases el dia de hoy",
                              size = 20,
                              color = TEXT,
                              weight = ft.FontWeight.W_800),
                                 bgcolor = CARD,
                                 padding = ft.Padding.all(10),
                                 alignment = ft.Alignment.CENTER_LEFT,
                                 border = ft.Border.all(3, PURPLE_MIDNIGHT)
                                 )
                ]
            )
        )
    else:
        boton_materia_actual = ft.Container(
        content = ft.Column(
            controls = [

                ft.Text("Clase actual: ",
                        size = 16,
                        color = TEXT_SECONDARY,
                        weight = ft.FontWeight.W_600),

                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.ACCESS_TIME_OUTLINED,
                                color=ft.Colors.PURPLE,
                                size=64,
                                ),
                        ft.Button(
                            content=ft.Text(
                                f"Materia: {materia_actual.obtener_nombre()}\n Aula: {materia_actual.obtener_aula()} | Edificio {materia_actual.obtener_edificio()}",
                                color=TEXT,
                                size=16,
                                italic=True, ),
                            style=ft.ButtonStyle(
                                bgcolor={
                                    ft.ControlState.HOVERED: PURPLE_MIDNIGHT,
                                    ft.ControlState.DEFAULT: CARD,
                                },
                                shape=ft.BeveledRectangleBorder(radius=5),
                                side = ft.BorderSide(width=2, color = PURPLE),
                            ),
                            on_click = lambda e: mostrar_informacion_materia_maestro(pagina, materia_actual)

                        )
                    ],
                    tight = True,
                )
            ],
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
        )
    )

        if materia_siguiente is None:
            boton_materia_siguiente = ft.Container(
                ft.Text("Ultima materia del dia",
                        color = TEXT_SECONDARY,
                        size = 16,
                        weight = ft.FontWeight.W_600)
            )
        else:
            boton_materia_siguiente = ft.Container(
            content = ft.Column(
            controls = [

                ft.Text("Su siguiente clase: ",
                        size = 16,
                        color = TEXT_SECONDARY,
                        weight = ft.FontWeight.W_600),

                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.ACCESS_TIME_OUTLINED,
                                color=TEXT_SECONDARY,
                                size=64,
                                ),
                        ft.Button(
                            content=ft.Text(
                                f"Materia: {materia_siguiente.obtener_nombre()}\n Aula: {materia_siguiente.obtener_aula()} | Edificio {materia_siguiente.obtener_edificio()}",
                                color=TEXT,
                                size=16,
                                italic=True, ),
                            style=ft.ButtonStyle(
                                bgcolor={
                                    ft.ControlState.HOVERED: TEXT_SECONDARY,
                                    ft.ControlState.DEFAULT: CARD,
                                },
                                shape=ft.BeveledRectangleBorder(radius=5),
                                side = ft.BorderSide(width=2, color = TEXT_SECONDARY),
                            ),
                            on_click = lambda event: mostrar_informacion_materia_maestro(pagina, materia_siguiente)

                        )
                    ],
                    tight = True
                )
            ],
        horizontal_alignment = ft.CrossAxisAlignment.CENTER,
        )
            )


    build = ft.Container(
        content  = ft.Column(
            controls = [
                header,
                boton_materia_actual,
                boton_materia_siguiente,
            ],
            spacing=10,
            tight = True,
        ),
    )

    return build

def filtrar_materia_hoy(usuario:Maestro ):

    if not usuario.obtener_materias():#En caso de no tener materias en mi lista, retorna nada
        return None, None


    materia_actual = None
    materia_siguiente = None
    timepo_actual = datetime.now()
    mapa_dias = {0: "Lunes", 1:"Martes", 2:"Miercoles", 3:"Jueves", 4:"Viernes", 5:"Sabado", 6:"Domingo"}
    dia_actual = mapa_dias[timepo_actual.weekday()]
    hora_actual = Hora(timepo_actual.hour, timepo_actual.minute)

    materias_hoy = [materia for materia in usuario.obtener_materias() if dia_actual in materia.obtener_dias_clase()]

    for materia in materias_hoy:
        hora_inicio = materia.obtenerHoraInicio()
        hora_fin = materia.obtenerHoraFin()

        if hora_inicio <= hora_actual <= hora_fin:
            materia_actual = materia

        elif hora_actual < hora_inicio and materia_siguiente is None:
            materia_siguiente = materia

    return materia_actual, materia_siguiente

def mostrar_informacion_materia_maestro(pagina:ft.Page, materia:Materia):
    alumnos = materia.obtener_alumnos()
    alumnos.sort(key = lambda alumno: alumno.obtenerNombre())


    header = ft.Container(
        content = ft.Row(
            controls = [
                ft.IconButton(ft.Icons.ARROW_BACK_OUTLINED,
                              icon_color = PURPLE_MIDNIGHT,
                              icon_size = 64,
                              on_click = lambda event: (pagina.views.pop(), pagina.update())
                              ),

                ft.Container(content = ft.Text("Informacion materia",
                                               color = TEXT,
                                               size = 36,
                                               italic = True,
                                               weight = ft.FontWeight.W_400),
                             alignment = ft.Alignment.TOP_CENTER,
                             expand = True,
                             padding = ft.Padding.all(10)
                            ),
            ]
        ),
        bgcolor = CARD,
    )

    boton_descargar_pdf = ft.Button(
        content=ft.Text("Descargar lista en PDF",
                        color=TEXT_SECONDARY,
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        italic=True),

        style=ft.ButtonStyle(
            bgcolor={
                ft.ControlState.HOVERED: TEXT_SECONDARY,
                ft.ControlState.DEFAULT: CARD,
            },
            shape=ft.BeveledRectangleBorder(radius=5),
            side=ft.BorderSide(width=2, color=TEXT_SECONDARY),
        ),
        on_click=lambda event: generar_pdf(pagina, alumnos)

    )

    cuerpo_materia = ft.Container(
        content = ft.Column(
            controls = [
                ft.Text(f"Materia: {materia.obtener_nombre()}",
                        color = TEXT,
                        size = 16,
                        weight = ft.FontWeight.W_600),
                ft.Text(f"Horario: {materia.hora_inicio} - {materia.hora_fin}",
                        color = TEXT,
                        size = 16,
                        weight = ft.FontWeight.W_400),
                ft.Text(f"Dias: ".join(materia.obtener_dias_clase()) if materia.obtener_dias_clase() else "No hay dias clase regristrado",
                        color = TEXT,
                        size = 16,
                        weight = ft.FontWeight.W_400),
                ft.Text(f"Aula: {materia.obtener_aula()} | Edificio {materia.edificio}",
                        color = TEXT,
                        size = 16,
                        weight = ft.FontWeight.W_400),
                ft.Text(f"Cupos: {materia.obtenerCuposDisponibles()} / {materia.cupos_totales}",
                        color=TEXT,
                        size=16,
                        weight=ft.FontWeight.W_400
                        )
            ],
        ),
        bgcolor = CARD,
        border = ft.Border.all(4, PURPLE),
        padding = ft.Padding.all(10),
    )

    cuerpo_alumnos = None

    if not materia.obtener_alumnos():
        cuerpo_alumnos = ft.Container(
            content = ft.Text(
                "No hay alumnos inscritos en esta materia",
                color = TEXT,
                size = 36,
                weight = ft.FontWeight.BOLD,
                italic = True
            ),
            bgcolor = CARD,
            padding = ft.Padding.all(10),
            border = ft.Border.all(4, TEXT_SECONDARY),
        )
    else :
        cuerpo_alumnos = ft.Column(
            controls = [
                ft.DataTable(
                    columns=[
                        ft.DataColumn(
                            ft.Text("No.",
                                    color=TEXT,
                                    weight=ft.FontWeight.BOLD,
                                    size=16)
                        ),

                        ft.DataColumn(
                            ft.Text("Nombre",
                                    color=TEXT,
                                    weight=ft.FontWeight.BOLD,
                                    size=16)
                        ),

                        ft.DataColumn(
                            ft.Text("Codigo",
                                    color=TEXT,
                                    weight=ft.FontWeight.BOLD,
                                    size=16)
                        )
                    ],

                    rows=[
                        ft.DataRow(
                            cells=[
                                ft.DataCell(
                                    ft.Text(f"{index}",
                                            color=TEXT_SECONDARY,
                                            size=16)
                                ),
                                ft.DataCell(
                                    ft.Text(f"{alumno.obtenerNombre()}",
                                            color=TEXT_SECONDARY,
                                            size=16)
                                ),
                                ft.DataCell(
                                    ft.Text(f"{alumno.obtenerIdentificacion()}",
                                            color=TEXT_SECONDARY,
                                            size=16)
                                )
                            ]
                        ) for index, alumno in enumerate(alumnos)
                    ],
                    border=ft.Border.all(4, PURPLE),
                    border_radius=10,
                    divider_thickness=10,
                    data_row_max_height=50,
                    data_row_min_height=40,
                    heading_row_height=50,
                    heading_row_color=PURPLE_MIDNIGHT
                ),

                boton_descargar_pdf

            ]
        )

    def generar_pdf(pagina: ft.Page, alumnos:list[Alumno]):
        dia_actual = datetime.now()

        fecha = Fecha()
        fecha.ponerDia(dia_actual.day)  # Usamos dia_actual, no la clase pura
        fecha.ponerMes(dia_actual.month)  # ¡Sin comas al final, guapo!
        fecha.ponerAño(dia_actual.year)

        meses = [
            "", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        mes_actual = meses[fecha.obtenerMes()]
        _, dias_totales = calendar.monthrange(dia_actual.year, dia_actual.month)

        # 2. Definimos la estructura interna del PDF
        class PDF(FPDF):
            def header(self):
                self.set_font("Arial", "B", 12)  # 'B' para que se vea imponente
                self.set_text_color(255, 255, 255)  # Letras blancas radiantes
                self.set_fill_color(0, 0, 0)  # Fondo negro absoluto (¡sin coma!)
                self.cell(0, 12, f"LISTA DE ASISTENCIA ({mes_actual} {fecha.obtenerAño()})", ln=True, align="C",
                          fill=True)
                self.ln(10)

        # 3. Instanciamos el lienzo
        pdf = PDF(orientation="L", unit="mm", format="A4")
        pdf.add_page()

        # --- ENCABEZADOS DE LA TABLA ---
        pdf.set_font("Arial", "B", 10)
        pdf.set_fill_color(30, 41, 59)  # Un gris/azul oscuro muy elegante para los títulos
        pdf.set_text_color(255, 255, 255)  # Letras blancas para contrastar el título de la tabla

        # Celda para el nombre
        pdf.cell(50, 8, "Nombre del Alumno", border=1, align="C", fill=True)

        # Celdas para los días
        ancho_celda_dia = 220 / dias_totales
        for dia in range(1, dias_totales + 1):
            pdf.cell(ancho_celda_dia, 8, str(dia), border=1, align="C", fill=True)
        pdf.ln()

        # --- CUERPO DE ALUMNOS (LOS DATOS REALES) ---
        pdf.set_font("Arial", "", 10)
        pdf.set_text_color(0, 0, 0)  # Volvemos al texto negro para los datos de los alumnos



        for alumno in alumnos:
                # Imprimimos el nombre con un borde limpio (1 suele ser el estándar)
            pdf.cell(50, 8, str(alumno.obtenerNombre()), border=1, align="L")

                # Creamos las casillas vacías para que el maestro marque la asistencia
            for _ in range(1, dias_totales + 1):
                pdf.cell(ancho_celda_dia, 8, "", border=1, align="C")

            pdf.ln()

        ruta_final = generar_ruta() / f"Lista_{materia.obtener_nombre()}.pdf"
        pdf.output(str(ruta_final))

    def generar_ruta():
        """
        Detecta de forma infalible el entorno y encuentra el punto exacto
        para depositar el archivo sin que Android se nos ponga digno.
        """
        import os
        import platform
        from pathlib import Path

        sistema = platform.system().lower()

        es_android = False
        try:
            # En Android, estas variables o rutas siempre están presentes en el entorno de ejecución
            if "ANDROID_BOOTLOGO" in os.environ or "ANDROID_ROOT" in os.environ:
                es_android = True
        except:
            es_android = False

        if es_android:

            ruta_base = Path("/storage/emulated/0/Download")

            if not os.path.access(ruta_base, os.W_OK):
                ruta_base = Path(os.path.expanduser("~")) / "Downloads"

        elif sistema == "windows":
            ruta_base = Path(os.environ.get("USERPROFILE", ".")) / "Documents"

        elif sistema == "darwin":
            ruta_base = Path.home() / "Downloads"

        else:
            ruta_base = Path.home() / "Documents"

        carpeta_sigha = ruta_base / "SIGHA"

        try:
            carpeta_sigha.mkdir(parents=True, exist_ok=True)
            print(f"¡Carpeta penetrada y creada con éxito en: {carpeta_sigha}!")
        except Exception as e:
            import tempfile
            carpeta_sigha = Path(tempfile.gettempdir()) / "SIGHA"
            carpeta_sigha.mkdir(parents=True, exist_ok=True)
            print(f"Tuvimos que usar la ruta de emergencia, mi amor: {carpeta_sigha}. Error: {e}")

        return carpeta_sigha











    vista = ft.View(
        [
            header,
            cuerpo_materia,
            cuerpo_alumnos,
        ],
        bgcolor = BG,
        vertical_alignment = ft.MainAxisAlignment.START,
        horizontal_alignment = ft.CrossAxisAlignment.CENTER,
        scroll = ft.ScrollMode.AUTO,
    )

    pagina.views.append(vista)

def seccion_2_Disponibilidad(pagina: ft.Page, usuario:Maestro):

    cuerpo = ft.Container(
        content =  ft.Button(
                    content = ft.Row(
                      controls = [
                          ft.Icon(ft.Icons.CALENDAR_MONTH_ROUNDED,
                                  size = 48,
                                  color = PURPLE_MIDNIGHT,
                            ),
                          ft.Text("Gestion de disponibilidad",
                                  size = 36,
                                  weight = ft.FontWeight.BOLD)

                      ],
                        tight = True
                    ),
                    style = ft.ButtonStyle(
                                bgcolor={
                                    ft.ControlState.HOVERED: PURPLE,
                                    ft.ControlState.DEFAULT: CARD,
                                },
                                shape=ft.BeveledRectangleBorder(radius=5),
                                side = ft.BorderSide(width=2, color = PURPLE_MIDNIGHT),
                            ),
                    on_click = lambda event: vista_disponibilidad()
                ),
    )

    vista = ft.Container(
        content = ft.Column(
            controls = [
                ft.Text("Seccion 2: Disponibilidad",
                        size = 16,
                        color = PURPLE,
                        weight = ft.FontWeight.BOLD),

                cuerpo
            ]
        ),

    )

    def vista_disponibilidad():
        header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.IconButton(ft.Icons.ARROW_BACK_OUTLINED,
                                  icon_color=PURPLE_MIDNIGHT,
                                  icon_size=64,
                                  on_click=lambda event: (pagina.views.pop(), pagina.update())
                                  ),

                    ft.Container(content=ft.Text("Disponibilidad",
                                                 color=TEXT,
                                                 size=36,
                                                 italic=True,
                                                 weight=ft.FontWeight.W_400),
                                 alignment=ft.Alignment.TOP_CENTER,
                                 expand=True,
                                 padding=ft.Padding.all(10)
                                 ),
                ]
            ),
            bgcolor=CARD,
        )

        dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
        horas = ["7:00 - 9:00", "9:00 : 11:00", "11:00 - 13:00", "13:00 - 15:00", "15:00 - 17:00", "17:00 - 19:00",
                 "19:00 - 21:00"]

        matriz_disponibilidad = {dia: {} for dia in dias}

        columnas = [
            ft.DataColumn(ft.Text("Hora / Dia", color=TEXT, weight=ft.FontWeight.BOLD))
        ]

        for dia in dias:
            columnas.append(
                ft.DataColumn(ft.Text(dia, color=TEXT, weight=ft.FontWeight.BOLD))
            )

        filas = []

        for hora in horas:
            celdas = [
                ft.DataCell(ft.Text(hora, color=TEXT, weight=ft.FontWeight.BOLD))
            ]

            for dia in dias:
                checkbox_celda = ft.Checkbox(value=False, active_color=ft.Colors.PURPLE)
                matriz_disponibilidad[dia][hora] = checkbox_celda
                celdas.append(ft.DataCell(checkbox_celda))

            filas.append(ft.DataRow(cells=celdas))

        tabla_disponibilidad = ft.DataTable(
            columns=columnas,
            rows=filas,
            show_checkbox_column=False,
            border=ft.Border.all(width=2, color=PURPLE_MIDNIGHT),
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.PURPLE),
            vertical_lines=ft.border.BorderSide(1, ft.Colors.PURPLE),
            bgcolor=CARD
        )

        contenedor_scroll_lateral = ft.Row(
            controls=[tabla_disponibilidad],
            scroll=ft.ScrollMode.AUTO,
            vertical_alignment=ft.CrossAxisAlignment.START
        )

        boton_continuar = ft.Button(
            content=ft.Text("Enviar", size=16, color=TEXT),
            style=ft.ButtonStyle(
                bgcolor={ft.ControlState.HOVERED: SECONDARY, ft.ControlState.DEFAULT: PRIMARY},
                shape=ft.RoundedRectangleBorder(radius=5),
                side=ft.BorderSide(width=2, color=PURPLE_MIDNIGHT),
            ),
            on_click=lambda event: boton_coninuar_accion()
        )

        boton_continuar = ft.Button(
            content=ft.Text("Enviar", size=16, color=TEXT),
            style=ft.ButtonStyle(
                bgcolor={ft.ControlState.HOVERED: SECONDARY, ft.ControlState.DEFAULT: PRIMARY},
                shape=ft.RoundedRectangleBorder(radius=5),
                side=ft.BorderSide(width=2, color=PURPLE_MIDNIGHT),
            ),
            on_click=lambda event: boton_coninuar_accion()
        )


        def boton_coninuar_accion():
            matriz = {}
            for dia in dias:
                matriz[dia] = {}
                for hora in horas:
                    matriz[dia][hora] = matriz_disponibilidad[dia][hora].value

            usuario.poner_disponibilidad(matriz)

            snack_bar = ft.SnackBar(
                content=ft.Text("Se ha enviado con éxito", color=TEXT, size=14, weight=ft.FontWeight.BOLD),
                bgcolor=PURPLE,
            )
            pagina.overlay.append(snack_bar)
            snack_bar.open = True
            pagina.update()


        ancho_auto = pagina.width * 0.90 if pagina.width else 360

        vista_disponibilidad = ft.View(
            controls=[
                header,
                ft.Divider(height=15, color="transparent"),
                ft.Container(
                    width=ancho_auto,
                    content=ft.Column(
                        controls=[
                            ft.Text("Desliza hacia los lados para ver toda la semana...",
                                    color=TEXT_SECONDARY, size=12, italic=True),
                            contenedor_scroll_lateral,  # La tabla que ahora se desliza divino
                            ft.Divider(height=10, color="transparent"),
                            boton_continuar
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    alignment=ft.Alignment.CENTER.CENTER,
                )
            ],
            bgcolor=BG,
            scroll=ft.ScrollMode.AUTO
        )

        pagina.views.append(vista_disponibilidad)
        pagina.update()








    return vista

def seccion_3_Notificaciones(pagina: ft.Page, usuario:Maestro):

    cuerpo = ft.Container(
        content = ft.Column(
            controls = [
                ft.Text("Seccion 3: Mis alertas",
                        color = PURPLE,
                        size = 16,
                        weight = ft.FontWeight.BOLD),

                ft.Button(
                    content = ft.Text("Cambio de Aula",
                                      size = 16,
                                      color = TEXT),
                    style = ft.ButtonStyle(
                                bgcolor={
                                    ft.ControlState.HOVERED: SECONDARY,
                                    ft.ControlState.DEFAULT: CARD,
                                },
                                shape=ft.BeveledRectangleBorder(radius=5),
                                side = ft.BorderSide(width=2, color = PURPLE),
                            ),
                    on_click = lambda event: pagina_nueva_solicitud(pagina, usuario)
                ),

                ft.Button(
                    content=ft.Text("Solicitudes pendientes",
                                    size=16,
                                    color=TEXT),
                    style=ft.ButtonStyle(
                        bgcolor={
                            ft.ControlState.HOVERED: SECONDARY,
                            ft.ControlState.DEFAULT: CARD,
                        },
                        shape=ft.BeveledRectangleBorder(radius=5),
                        side=ft.BorderSide(width=2, color=PURPLE_MIDNIGHT),
                    ),
                    on_click = lambda event: pagina_respuestas()
                )
            ],
            spacing = 10
        ),
    )
    def crear_header (texto:str):
        header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.IconButton(ft.Icons.ARROW_BACK_OUTLINED,
                                  icon_color=PURPLE_MIDNIGHT,
                                  icon_size=64,
                                  on_click=lambda event: (pagina.views.pop(), pagina.update())
                                  ),

                    ft.Container(content=ft.Text(f"{texto}",
                                                 color=TEXT,
                                                 size=36,
                                                 italic=True,
                                                 weight=ft.FontWeight.W_400),
                                 alignment=ft.Alignment.TOP_CENTER,
                                 expand=True,
                                 padding=ft.Padding.all(10)
                                 ),
                ]
            ),
            bgcolor=CARD,
        )
        return header

    def pagina_nueva_solicitud(pagina: ft.Page, usuario:Maestro):
        header = crear_header("Solicitud cambio de Aula")

        cuadro_texto = ft.TextField(
                        label = ft.Text("Ingrese su solicitud",
                                        color = TEXT_SECONDARY,
                                        size = 16),
                        max_lines = 8,
                        max_length = 200,
                        bgcolor = CARD,
                        border_color = SECONDARY,
                        border_radius = 2
                    )

        cuerpo = ft.Container(
            content = ft.Column(
                controls = [
                    cuadro_texto,

                    ft.Button(
                        content=ft.Text("Enviar",
                                        size=16,
                                        color=TEXT),
                        style=ft.ButtonStyle(
                            bgcolor={
                                ft.ControlState.HOVERED: SECONDARY,
                                ft.ControlState.DEFAULT: CARD,
                            },
                            shape=ft.BeveledRectangleBorder(radius=5),
                            side=ft.BorderSide(width=2, color=SECONDARY),
                        ),
                        on_click = lambda event: continuar()

                    )

                ],
            ),
            alignment = ft.Alignment.CENTER
        )
        def continuar():
            if cuadro_texto.value:
                peticion = Alerta(mensaje=cuadro_texto.value)
                usuario.agregar_peticion(peticion)
                cuadro_texto.error = None
                cuadro_texto.value = None
                pagina.show_dialog(snackBar)

            else:
                cuadro_texto.error = "Ingrese una peticion valida"


            pagina.update()


        snackBar = ft.SnackBar(
            content = ft.Text("Se a enviado con exito",
                              color = TEXT_SECONDARY,
                              size = 12,
                              weight = ft.FontWeight.BOLD),
            duration = 3000,
            bgcolor = CARD,
            visible = True
        )

        vista = ft.View(
            controls = [
                header,
                cuerpo
            ],
            padding = 10,
            bgcolor = BG,
        )
        pagina.views.append(vista)

    def pagina_respuestas():
        header = crear_header("Solicitudes pendientes")
        cuerpo = None

        if not usuario.obtener_alertas():
            cuerpo = ft.Container(
                content = ft.Text(
                    "No tienes respuestas",
                    color = TEXT,
                    size = 36,
                    weight = ft.FontWeight.BOLD,
                    italic = True,
                ),
                bgcolor = CARD,
                padding = ft.Padding.all(10),
                border = ft.Border.all(4 ,color = PURPLE),
                alignment = ft.Alignment.CENTER
            )

        else:
            cuerpo = ft.Column(
                controls = [
                    ft.Button(
                        content = ft.Text(f"{alerta.obtener_mensaje()[0:20]}",
                                          color = TEXT_SECONDARY,
                                          size = 16
                                          ),
                        style = ft.ButtonStyle(
                            bgcolor={
                                ft.ControlState.HOVERED: SECONDARY,
                                ft.ControlState.DEFAULT: CARD,
                            },
                            shape=ft.BeveledRectangleBorder(radius=5),
                            side=ft.BorderSide(width=2, color=PRIMARY),
                        ),
                        on_click=lambda event: alerta_completa(alerta)

                    )for alerta in usuario.obtener_alertas()
                ]

            )

            def alerta_completa(alerta:Alerta):
                header = crear_header("Respuesta")

                cuerpo = ft.Container(
                    content = ft.TextField(
                        value = f"{alerta.obtener_mensaje()}",
                        max_lines=8,
                        bgcolor=CARD,
                        border_color=PURPLE_MIDNIGHT,
                        border_radius=2,
                        read_only = True

                    ),

                    alignment = ft.Alignment.CENTER,
                )

                vista = ft.View(
                    controls = [
                        header,
                        cuerpo
                    ],
                    bgcolor = BG,
                )

                alerta.poner_visto(True)
                usuario.depurar_alertas()
                pagina.views.append(vista)



        vista = ft.View(
            controls = [
                header,
                cuerpo
            ],
            scroll = ft.ScrollMode.AUTO,
            bgcolor = BG
        )

        pagina.views.append(vista)

    return cuerpo

def pagina_materias(pagina:ft.Page, usuario:Maestro):
    header = ft.Container(

        content = ft.Row(
            controls = [
                ft.IconButton(ft.Icons.ARROW_BACK_OUTLINED,
                              icon_color = PURPLE_MIDNIGHT,
                              icon_size = 64,
                              on_click = lambda event: (pagina.views.pop(), pagina.update())
                              ),

                ft.Container(content = ft.Text("Materias",
                                               color = TEXT,
                                               size = 36,
                                               italic = True,
                                               weight = ft.FontWeight.W_400),
                             alignment = ft.Alignment.TOP_CENTER,
                             expand = True,
                             padding = ft.Padding.all(10)
                            ),
            ]
        ),
        bgcolor = CARD,
    )


    materias = usuario.obtener_materias()

    if not materias:
        cuerpo = ft.Container(
           content = ft.Text(
               "No tienes materias registradas",
               color = TEXT,
               size = 16,
               weight = ft.FontWeight.BOLD,
           ),
           bgcolor = BG,
           alignment = ft.Alignment.CENTER,
       )
    else:
        cuerpo = ft.Container(
            content = ft.Column(
                controls = [
                    ft.Button(
                        content=ft.Text(
                            f"Materia: {materia.obtener_nombre()}\n Aula: {materia.obtener_aula()} | Edificio {materia.obtener_edificio()}",
                            color=TEXT,
                            size=16,
                            italic=True, ),
                        style=ft.ButtonStyle(
                            bgcolor={
                                ft.ControlState.HOVERED: PURPLE_MIDNIGHT,
                                ft.ControlState.DEFAULT: CARD,
                            },
                            shape=ft.BeveledRectangleBorder(radius=5),
                            side=ft.BorderSide(width=2, color=PURPLE),
                        ),
                        on_click=lambda e, m = materia: mostrar_informacion_materia_maestro(pagina, m)

                    )for materia in materias
                ]
            ),
            alignment = ft.Alignment.CENTER,
        )

    build = ft.Container(
        content = ft.Column(
            controls = [
                header,
                cuerpo
                 ]
             )
        )
    return build

def pagina_notificaciones(pagina:ft.Page, usuario:Maestro):
    header = ft.Container(

        content=ft.Row(
            controls=[
                ft.IconButton(ft.Icons.ARROW_BACK_OUTLINED,
                              icon_color=PURPLE_MIDNIGHT,
                              icon_size=64,
                              on_click=lambda event: (pagina.views.pop(), pagina.update())
                              ),

                ft.Container(content=ft.Text("Materias",
                                             color=TEXT,
                                             size=36,
                                             italic=True,
                                             weight=ft.FontWeight.W_400),
                             alignment=ft.Alignment.TOP_CENTER,
                             expand=True,
                             padding=ft.Padding.all(10)
                             ),
            ]
        ),
        bgcolor=CARD,
    )

    notificaciones = usuario.obtener_notifiaciones()

    if not notificaciones:
        cuerpo = ft.Container(
            content=ft.Text(
                "No tienes notificaciones",
                color=TEXT,
                size=16,
                weight=ft.FontWeight.BOLD,
            ),
            bgcolor=BG,
            alignment=ft.Alignment.CENTER,
        )

    else:
        cuerpo = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Button(
                        content=ft.Text(
                            f"{notificacion.obtener_mensaje()[0:15]}. . .",
                            color=TEXT,
                            size=16,
                            italic=True, ),
                        style=ft.ButtonStyle(
                            bgcolor={
                                ft.ControlState.HOVERED: PURPLE_MIDNIGHT,
                                ft.ControlState.DEFAULT: CARD,
                            },
                            shape=ft.BeveledRectangleBorder(radius=5),
                            side=ft.BorderSide(width=2, color=PURPLE),
                        ),
                        on_click=lambda e, n=notificacion: mostrar_notificacion(n)

                    ) for notificacion in notificaciones
                ]
            ),
            alignment=ft.Alignment.CENTER,
        )

        def mostrar_notificacion(notificacion: Alerta):
            header = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.IconButton(ft.Icons.ARROW_BACK_OUTLINED,
                                      icon_color=PURPLE_MIDNIGHT,
                                      icon_size=64,
                                      on_click=lambda event: (pagina.views.pop(), pagina.update())
                                      ),

                        ft.Container(content=ft.Text("Disponibilidad",
                                                     color=TEXT,
                                                     size=36,
                                                     italic=True,
                                                     weight=ft.FontWeight.W_400),
                                     alignment=ft.Alignment.TOP_CENTER,
                                     expand=True,
                                     padding=ft.Padding.all(10)
                                     ),
                    ]
                ),
                bgcolor=CARD,
            )

            cuerpo = ft.Container(
                    content=ft.TextField(
                        value=f"{notificacion.obtener_mensaje()}",
                        max_lines=8,
                        bgcolor=CARD,
                        border_color=PURPLE_MIDNIGHT,
                        border_radius=2,
                        read_only=True
                    ),

                    alignment=ft.Alignment.CENTER,
                )

            vista = ft.View(
                controls = [
                    header,
                    cuerpo
                ],
                bgcolor = BG
            )

            pagina.views.append(vista)





    build = ft.Container(
        content=ft.Column(
            controls=[
                header,
                cuerpo
            ]
        )
    )
    return build

def pagina_perfil(pagina, usuario:Maestro):
    header = ft.Container(

        content=ft.Row(
            controls=[
                ft.IconButton(ft.Icons.ARROW_BACK_OUTLINED,
                              icon_color=PURPLE_MIDNIGHT,
                              icon_size=64,
                              on_click=lambda event: (pagina.views.pop(), pagina.update())
                              ),

                ft.Container(content=ft.Text("Materias",
                                             color=TEXT,
                                             size=36,
                                             italic=True,
                                             weight=ft.FontWeight.W_400),
                             alignment=ft.Alignment.TOP_CENTER,
                             expand=True,
                             padding=ft.Padding.all(10)
                             ),
            ]
        ),
        bgcolor=CARD,
    )

    materias = usuario.obtener_materias()
    carga_horaria = 0

    for materia in materias:
        carga_horaria += materia.obtener

    cuerpo = ft.Container(
        content = ft.Column(
            controls = [
                ft.Icon(ft.Icons.ACCOUNT_CIRCLE_OUTLINED,
                        color = ft.Colors.RED,
                        size = 64),
                
                ft.Text(f"Nombre: {usuario.obtenerNombre()}",
                        color = TEXT,
                        size = 16),

                ft.Text(f"{usuario.obtener_departamento()}",
                        color=TEXT_SECONDARY,
                        size=20),

                ft.Text(f"Codigo: {usuario.obtenerIdentificacion()}",
                        color=TEXT,
                        size=16),
                ft.Text(f"Correo: {usuario.obtenerCorreo()}",
                        color=TEXT,
                        size=16),

                ft.Text(f"Carga horaria: {carga_horaria}",
                        color=TEXT,
                        size=16)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            tight = True
        ),
        bgcolor = CARD,
        padding = 16,
        border_radius = 12,
    )

    build = ft.Container(
        content = ft.Column(
            controls = [
                header,
                cuerpo
            ],
            spacing = 12,
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
        ),
    )

    return build






































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
                            size=16,
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
                                        size=16,
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
                    size=16,
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
                                size=16,
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
                                size=16,
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
                                size=16,
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