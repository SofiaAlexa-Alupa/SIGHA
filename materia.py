from seccion import Seccion
from functools import total_ordering

@total_ordering
class Materia(Seccion):
    def __init__(self,
                 identificacion = "-2589751", #El id de la materia
                 codigo = "S0FtW4r3", #El codigo de la materia (Por ejemplo si es matematicas, todas las materias que tengan matematicas llevaran el mismo codigo)
                 nombre = "La materia mas hermosa, programacion",#Nombre de la materia
                 creditos = 12,#Los creditos que dara la materia al ser finalizada
                 facultad = "Computacion", #Facultad que depende la materia
                 promedio = 0#El promedio de la materia que el alumno tiene de la materia, unicamente visible en la informacion del alumno
     ):

        super().__init__()
        self.identificacion = identificacion
        self.codigo = codigo
        self.nombre = nombre
        self.creditos = creditos
        self.facultad = facultad
        self.promedio = promedio

    def __str__(self):#Retorna el stirng con la informacion EXCLUSIVA de la materia, lo que se mostrara en el horario
        return (f"Materia ID: {self.identificacion}\n"
                f"Codigo: {self.codigo}\n"
                f"Nombre: {self.nombre}\n"
                f"Creditos: {self.creditos}\n"
                f"Facultad: {self.facultad}")

    def __lt__(self, other):# Operador logico
        return self.criterios_comparacion() < other.criterios_comparacion()

    def __eq__(self, other):#Operador logico ==
        return self.criterios_comparacion() == other.criterios_comparacion()

    def criterios_comparacion(self):  # Los criterios que tomara a la hora de usar los operadores logicos
        return (self.codigo, self.facultad)


    def obtener_string_seccion(self):#Retorna el string que tenia la seccion
        return super().__str__()

    def obtener_string_vista_alumno(self):#Obtenemos un string, con todo lo visible una vez que el alumno registre una materia
        return (f"self.__str__()"
                f"Promedio: {self.promedio}\n")

    #Las funciones de la clase "Padre" o "Superclase" ya estan implementadas por herencia <;p

    def poner_identificacion(self, identificacion): #Metodo que modifica el atributo de identificacion
        self.identificacion = identificacion

    def poner_codigo(self, codigo): #Metodo que moidfica el atributo codigo
        self.codigo = codigo

    def poner_nombre(self, nombre):#Metodo que modiica el atributo nombre
        self.nombre = nombre

    def poner_creditos(self, creditos):#Metodo que modifica el atributo credito
        self.creditos = creditos

    def poner_facultad(self, facultad):#Metodo que modifica el atributo facultad
        self.facultad = facultad

    def poner_promedio(self, promedio):#Metodo que modifica el atributo promedio
        self.promedio = promedio




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




