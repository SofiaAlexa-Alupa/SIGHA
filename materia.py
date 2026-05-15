from alumno import Alumno
from hora import Hora
from seccion import Seccion
from functools import total_ordering


@total_ordering
class Materia(Seccion):

    def __init__(self,
                 identificacion:str = "-2589751", #El id de la materia
                 codigo:str = "S0FtW4r3", #El codigo de la materia (Por ejemplo si es matematicas, todas las materias que tengan matematicas llevaran el mismo codigo)
                 nombre:str = "La materia mas hermosa, programacion",#Nombre de la materia
                 creditos:int = 12,#Los creditos que dara la materia al ser finalizada
                 facultad:str = "Computacion", #Facultad que depende la materia
                 promedio:int = 0,#El promedio de la materia que el alumno tiene de la materia, unicamente visible en la informacion del alumno
                 aula:int = 0, #Entero, el numero de aula dentro de un edificio
                 edificio:str = "A", #Nombre del edificio
                 dias_clase:list[str] = None,#Dias en los que se imparte
                 alumnos:list[Alumno] = None,#Alumnos inscritos
                 modalidad:str = "Presencial",#Presencial, Virtual o Hibrida
                 prerequisitos:list[str] = None,#Materias prerequisito
                 profesor_nombre:str = "Sin asignar",#Nombre profesor
                 profesor_correo:str = "correo@udg.mx",#Correo profesor
                 seccion_nombre:str = "D01",#Seccion visible para alumno
                 cupos_totales:int = 40,#Capacidad total
                 cupos_disponibles:int = 40,#Cupos restantes
                 hora_inicio:Hora = None,#Hora inicio clase
                 hora_fin:Hora = None#Hora final clase
                 ):

        super().__init__()

        self.identificacion = identificacion
        self.codigo = codigo
        self.nombre = nombre
        self.creditos = creditos
        self.facultad = facultad
        self.promedio = promedio
        self.aula = aula
        self.edificio = edificio

        self.dias_clase = (
            dias_clase
            if dias_clase is not None
            else []
        )

        self.alumnos:list[Alumno] = (
            alumnos
            if alumnos is not None
            else []
        )

       
        # NUEVOS ATRIBUTOS
       
        self.modalidad = modalidad

        self.prerequisitos = (
            prerequisitos
            if prerequisitos is not None
            else []
        )

        self.profesor_nombre = profesor_nombre
        self.profesor_correo = profesor_correo

        self.seccion_nombre = seccion_nombre

        self.cupos_totales = cupos_totales
        self.cupos_disponibles = cupos_disponibles

        self.hora_inicio = (
            hora_inicio
            if hora_inicio is not None
            else Hora()
        )

        self.hora_fin = (
            hora_fin
            if hora_fin is not None
            else Hora()
        )


    def __str__(self):#Retorna informacion EXCLUSIVA de la materia

        return (
                f"Materia ID: {self.identificacion}\n"
                f"Codigo: {self.codigo}\n"
                f"Nombre: {self.nombre}\n"
                f"Creditos: {self.creditos}\n"
                f"Facultad: {self.facultad}\n"
                f"Aula: {self.aula}\n"
                f"Edificio: {self.edificio}\n"
                f"Profesor: {self.profesor_nombre}\n"
                f"Seccion: {self.seccion_nombre}\n"
                f"Modalidad: {self.modalidad}\n"
        )


    def __lt__(self, other):#Operador logico <
        return (
            self.criterios_comparacion()
            <
            other.criterios_comparacion()
        )


    def __eq__(self, other):#Operador logico ==

        return (
            self.criterios_comparacion()
            ==
            other.criterios_comparacion()
        )


    def criterios_comparacion(self):#Criterios de comparacion
        return (
            self.codigo,
            self.facultad
        )


    def obtener_string_seccion(self):#Retorna string de seccion
        return super().__str__()


    def obtener_string_vista_alumno(self):#Vista completa alumno

        return (
                f"{self.__str__()}\n"
                f"Promedio: {self.promedio}\n"
                f"Cupos: {self.cupos_disponibles}/{self.cupos_totales}\n"
                f"Dias: {self.dias_clase}\n"
                f"Horario: {self.hora_inicio} - {self.hora_fin}\n"
                f"Profesor correo: {self.profesor_correo}\n"
                f"Prerequisitos: {self.prerequisitos}\n"
        )



       #METODOS QUE MODIFICAN ATRIBUTOS#
     
    def poner_identificacion(self, identificacion):
        self.identificacion = identificacion

    def poner_codigo(self, codigo):
        self.codigo = codigo

    def poner_nombre(self, nombre):
        self.nombre = nombre

    def poner_creditos(self, creditos):
        self.creditos = creditos

    def poner_facultad(self, facultad):
        self.facultad = facultad

    def poner_promedio(self, promedio):
        self.promedio = promedio

    def poner_aula(self, aula):
        self.aula = aula

    def poner_edificio(self, edificio):
        self.edificio = edificio

    def poner_modalidad(self, modalidad):
        self.modalidad = modalidad

    def poner_profesor_nombre(self, nombre):
        self.profesor_nombre = nombre

    def poner_profesor_correo(self, correo):
        self.profesor_correo = correo

    def poner_seccion_nombre(self, seccion):
        self.seccion_nombre = seccion

    def poner_cupos_totales(self, cupos):
        self.cupos_totales = cupos

    def poner_cupos_disponibles(self, cupos):
        self.cupos_disponibles = cupos

    def poner_hora_inicio(self, hora):
        self.hora_inicio = hora

    def poner_hora_fin(self, hora):
        self.hora_fin = hora

    def agregar_prerequisito(self, prerequisito):
        self.prerequisitos.append(prerequisito)

    def agregar_alumno(self, alumno):

        if self.cupos_disponibles > 0:

            self.alumnos.append(alumno)
            self.cupos_disponibles -= 1

            return 0

        return -1#No hay cupos


    def quitar_alumno(self, alumno):

        if alumno in self.alumnos:

            self.alumnos.remove(alumno)

            self.cupos_disponibles += 1

            return 0

        return -4#Error al no encontrar alumno


    def agregar_dias_clase(self, dia):
        self.dias_clase.append(dia)

    def limpiar_dias_clase(self):
        self.dias_clase.clear()


    
       #METODOS QUE DEVUELVEN ATRIBUTOS#
      

    def obtener_identificacion(self):
        return self.identificacion

    def obtener_codigo(self):
        return self.codigo

    def obtener_nombre(self):
        return self.nombre

    def obtener_creditos(self):
        return self.creditos

    def obtener_facultad(self):
        return self.facultad

    def obtener_promedio(self):
        return self.promedio

    def obtener_aula(self):
        return self.aula

    def obtener_edificio(self):
        return self.edificio

    def obtener_dias_clase(self):
        return self.dias_clase

    def obtener_alumnos(self):
        return self.alumnos

    def obtener_modalidad(self):
        return self.modalidad

    def obtener_prerequisitos(self):
        return self.prerequisitos

    def obtener_profesor_nombre(self):
        return self.profesor_nombre

    def obtener_profesor_correo(self):
        return self.profesor_correo

    def obtener_seccion_nombre(self):
        return self.seccion_nombre

    def obtener_cupos_totales(self):
        return self.cupos_totales

    def obtener_cupos_disponibles(self):
        return self.cupos_disponibles

    def obtenerHoraInicio(self):
        return self.hora_inicio

    def obtenerHoraFin(self):
        return self.hora_fin