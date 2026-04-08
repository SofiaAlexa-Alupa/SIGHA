class Nombre:
    def __init__(self, nombre = "Susana", apellido_materno = "De las Flores", apellido_paterno = "Lara"):
        self.nombre = nombre
        self.apellidoMaterno = apellido_materno
        self.apellidoPaterno = apellido_paterno


    def __str__(self):
        return f"{self.apellido} {self.nombre}"


    '''
    #################################
    #METODOS QUE MODIFICAN ATRIBUTOS#
    #################################
    '''

    def ponerNombre(self, nombre):
        self.nombre = nombre

    def ponerApellido(self, apellido):
        self.apellido = apellido

    '''
     #####################################
     #Metodos para devolver los atributos#
     #####################################
     '''

    def obtenerNombre(self):
        return self.nombre

    def obtenerApellido(self):
        return self.apellido

