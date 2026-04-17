from functools import total_ordering

@total_ordering #etiqueta que nos crea la sobrecarga de los otros operadores gracias al == y <
class Nombre:
    def __init__(self, nombre = "Susana", apellido_materno = "De las Flores", apellido_paterno = "Lara"):
        self.nombre = nombre
        self.apellidoMaterno = apellido_materno
        self.apellidoPaterno = apellido_paterno


    def __str__(self):#Metodo que regresa el toString
        return f"{self.apellidoPaterno} {self.apellidoMaterno} {self.nombre}"

    def __eq__(self, otro):#Sobrecarga del operador ==
        if not isinstance(otro, Nombre):
            return False

        return self.criterios_busquedas() == otro.criterios_busquedas()


    def __lt__(self, otro):#sobrecarga del operador <
        if not isinstance(otro, Nombre):
            return NotImplemented

        return self.criterios_busquedas() < otro.criterios_busquedas()

    def criterios_busquedas(self): #Regresa una tupla, la cual nos dice que se toma y en que orden se evalua para la sobrecarga de operadores, no se usara realmente en el programa
        return (self.apellidoPaterno, self.apellidoMaterno, self.nombre)



    '''
    #################################
    #METODOS QUE MODIFICAN ATRIBUTOS#
    #################################
    '''

    def ponerNombre(self, nombre):#Metodo que modifica el atrubuto nombre
        self.nombre = nombre.upper()

    def ponerApellidoPaterno(self, apellidoPaterno):#Metodo que modifica el apellido paterno
        self.apellidoPaterno = apellidoPaterno.upper()

    def ponerApellidoMaterno(self, apellidoMaterno):#Metodo que modifica el apellido materno
        self.apellidoMaterno = apellidoMaterno.upper()

    '''
     #####################################
     #Metodos para devolver los atributos#
     #####################################
     '''

    def obtenerNombre(self):#Metodo que retorna el atributo nombre
        return self.nombre

    def obtenerApellidoPaterno(self):#Metodo que retorna el apellido Paterno
        return self.apellidoPaterno

    def obtenerApellidoMaterno(self):#Metodo que retorna el apellido materno
        return self.apellidoMaterno

