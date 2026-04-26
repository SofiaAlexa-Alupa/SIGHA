#Librerias utilizadas
import flet as ft
from time import sleep
import asyncio


#interfaz codficada
import interfaz_grafica as interfaz

#Importacion de las clases
from administrador import Administrador
from alumno import Alumno
from maestro import Maestro
from materia import Materia
from nombre import Nombre
from seccion import Seccion
from fecha import Fecha
from hora import Hora

def main(pagina: ft.Page):#
    pagina.tittle = "SIGHA"#Titulo de la pagina
    pagina.vertical_alignment = ft.MainAxisAlignment.CENTER
    pagina.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    pagina.padding = 5 #Espacio interno entre borde y contenido
    pagina.bgcolor = "0f172a"
    pagina.primary_color = "c084fc"








ft.app(main)


