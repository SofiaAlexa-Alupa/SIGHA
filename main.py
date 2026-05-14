#Librerias utilizadas
import flet as ft

#interfaz codficada
import interfaz_grafica as interfaz

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

    #usuario = interfaz.login(pagina)
    usuario = Maestro()
    #usuario = Alumno()

     if isinstance(usuario, Administrador):
         interfaz.interfaz_administrador(pagina,usuario,db_materias,db_alumnos,db_maestros)

     if isinstance(usuario, Alumno):
        interfaz.interfaz_alumno(  pagina, usuario, db_materias)

    if isinstance(usuario, Maestro):
        interfaz.interfaz_maestro(pagina, usuario)






ft.run(main)


