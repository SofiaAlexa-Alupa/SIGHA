#Librerias utilizadas
import flet as ft

import interfaz_grafica
#interfaz codficada
import interfaz_grafica as interfaz
import usuario

#Importacion de las clases
from administrador import Administrador
from alumno import Alumno
from maestro import Maestro
from materia import Materia

# Base de datos temporales
db_alumnos : list[Alumno]=[]
db_maestros : list[Maestro]=[]
db_materias : list[Materia]=[]


def main(pagina: ft.Page):#
    pagina.tittle = "SIGHA"#Titulo de la pagina
    pagina.vertical_alignment = ft.MainAxisAlignment.CENTER
    pagina.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    pagina.padding = 5 #Espacio interno entre borde y contenido
    pagina.bgcolor = "#0f172a"

    #usuario = interfaz_grafica.login(pagina)
    #usuario = Maestro()
    #interfaz.interfaz_maestro_nueva(pagina, usuario)
    usuario = Alumno()
    interfaz_grafica.interfaz_alumno(pagina, usuario, db_alumnos)
    #usuario = Administrador()
    #interfaz_grafica.interfaz_administrador(pagina,usuario, db_alumnos= db_alumnos,db_maestros= db_maestros, db_materias = db_materias)

ft.app(main)


