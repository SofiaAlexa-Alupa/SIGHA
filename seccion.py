from fecha import Fecha
from hora import Hora

class Seccion:
    def __init__(self,
                 identificacion = "Moderm C7M", #Atributo tipo string para combinar numeros y letras,
                 seccion = "A00", #Atributo tipo string, que nos indica la seccion que pertenece
                 hora_inicio = Hora(),#Hora que se incia la clase de esa seccion, tipo Hora
                 hora_fin = Hora(), #Hora de finalizacion de claseen esa seccion, tambien tipo hora
                 fecha_inicio = Fecha(),#Fecha que inicia la seccion
                 fecha_fin = Fecha(),#Fecha que finaliza la seccion
                 cupos_totales = 0,#Cupos totales que tiene la materia
                 cupos_disponibles = 0):#Se actualizara cuando los estudiantes se inscriban a la seccion, en caso de agregar cupos tambien se actualiza

        self.identificacion = identificacion
        self.seccion = seccion
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.cupos_totales = cupos_totales
        self.cupos_disponibles = cupos_disponibles

    def __str__(self):#Funcion que nos devuelve el string de todos los datos formateados
        return (f"Identificacion de seccion: {self.identificacion}\n"
                f"Numero de seccion: {self.seccion}\n"
                f"Hora de inicio: {self.hora_inicio}\n"
                f"Hora de salida: {self.hora_fin}\n"
                f"Fecha de inicio: {self.fecha_inicio}\n"
                f"Fecha de fin: {self.fecha_fin}\n"
                f"Cupos totales: {self.cupos_totales}\n"
                f"Cupos disponibles: {self.cupos_disponibles}\n")



    '''
    ################################
    #METODOS QUE CALCULAN ATRIBUTOS#
    ################################
    '''

    def obtener_dias_totales(self):#Utiliza los metodos de las clases fecha, y retorna cuantos dias tiene en total la seccion
        return self.fecha_inicio.calculoDiferenciaDias(self.fecha_fin)

    def quitar_cupo(self):#Quita un unico cupo#Quita un UNICO cupo
        if self.cupos_disponibles - 1 <= 0:#En caso de que no sea suficiente
            return -1#Regresa este error, el cual esta en la lista de excel

        self.cupos_disponibles -= 1 #En caso de que si se pueda, restara solamente uno
        return 0 #Retorna 0 en caso de exito

    def quitar_cupos(self, cupos):#Puede quitar mas de un unico cupo
        if self.cupos_disponibles - cupos < 0:#Comprueba que existan suficientes cupos para poder eliminar
            return -1#En caso de que los cupos disponibles no sean sucifientes retorna -1

        if cupos <= 0:#Si los cupos que quieres eliminar son negativos (Por ejemplo -3), dara el error -2 (Esta en el exel)
            return -2

        self.cupos_disponibles -= cupos#Se restan los cupos disponibles si todo es correcto
        self.cupos_disponibles -= cupos#Se  restan los cupos disponibles si son suficientes
        return 0

    def agregar_cupos(self, cupos):#metodo para agregar los cupos
        if cupos <= 0:#Si los cupos son 0 o menor
            return -2#Da el error -2

        #Si todo bien, entonces se le sumaran los cupos a los cupos disponibles y a los totales
        self.cupos_disponibles += cupos
        self.cupos_totales += cupos
        return 0


    '''
    ##################################
    #Metodos para modificar atributos#
    #########
    '''
    def ponerIdentificacion(self, identificacion):
        self.identificacion = identificacion

    def ponerSeccion(self, seccion):
        self.seccion = seccion

    def ponerHoraInicio(self, Hora):
        self.hora_inicio = Hora

    def ponerHoraFin(self, Hora):
        self.hora_fin = Hora

    def ponerFechaInicio(self, Fecha):
        self.fecha_inicio = Fecha

    def ponerFechaFin(self, Fecha):
        self.fecha_fin = Fecha


    '''
    #####################################
    #Metodos para devolver los atributos#
    #####################################
    '''
    def obtenerIdentificacion(self):
        return self.identificacion

    def obtenerSeccion(self):
        return self.seccion

    def obtenerHoraInicio(self):
        return self.hora_inicio

    def obtenerHoraFin(self):
        return self.hora_fin

    def obtenerFechaInicio(self):
        return self.fecha_inicio

    def obtenerFechaFin(self):
        return self.fecha_fin

    def obtenerCuposTotales(self):
        return self.cupos_totales

    def obtenerCuposDisponibles(self):
        return self.cupos_disponibles



