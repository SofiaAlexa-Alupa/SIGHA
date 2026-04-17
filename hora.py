from functools import total_ordering

@total_ordering
class Hora:

    def __init__(self,
                 hora = 0, #La hora sera un entero
                 minuto = 0): #Atributo minuto que tambien es un entero

        self.hora = hora
        self.minuto = minuto

    def __str__(self):#metodo que nos regresa un string formateado de la hora en el siguiente formato (H:M:S)
        return f"{self.hora:02d}:{self.minuto:02d}"

    def __eq__(self, otro):
        return self.criterio_busqueda() == otro.criterio_busqueda()

    def __lt__(self, otro):
        return self.criterio_busqueda() < otro.criterio_busqueda()

    def criterio_busqueda(self):
        return (self.hora, self.minuto)

    '''
    ##########################################
    #Metodos operacionales dentro de la clase#
    ##########################################
    '''

    def validar(self, hora, minuto):#metodo que nos permite evaluar antes de poner una hora si esta dentro del rango de las 24 hrs, devolviendo VERDARERO en caso se que sea correcto

        if hora > 23 or hora < 0: #En caso de que la hora que queramos agregar sobrepase las 24 hrs, dara falso. Y lo mismo si es menor a las 00
            return False

        if minuto > 59 or minuto < 0:#En caso de que el minuto que pongamos sea mayor a 59, sera falso. De la misma forma si minuto es menor a 0
            return False

        return True #En caso de que la hora sea valida, dara verdaero  (El valor maximo sera 23:59), el valor minimo (00:00)

    '''
    ##################################
    #Metodos para modificar atributos#
    ##################################
    '''
    def ponerHora(self, hora):#metodo que modifica el atributo hora
        self.hora = hora

    def ponerMinuto(self, minuto):#metodo que modifica el atribuo minuto
        self.minuto = minuto

    '''
    #####################################
    #Metodos para devolver los atributos#
    #####################################
    '''

    def obtenerHora(self):#Metodo que nos regresa la hora Da un string
        return f"{self.hora}:02d"

    def obtenerMinuto(self):#Metodo que nos regresa el atributo minuto, Da un string
        return f"{self.minuto:02d}"


    #Fin de clase


