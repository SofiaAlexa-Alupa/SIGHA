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

    '''
    TODO
    Calculo dias disonibles
    quitar cupos
    agregar cupos
    '''


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
        self.hora_inicio.ponerHora(Hora.obtenerHora())
        self.hora_fin.ponerMinuto(Hora.obtenerMinuto())

    def ponerHoraFin(self, Hora):
        self.hora_fin.ponerHora(Hora.obtenerHora())
        self.hora_fin.ponerMinuto(Hora.obtenerMinuto())

    def ponerFechaInicio(self, Fecha):
        self.fecha_inicio.ponerAño(Fecha.obtenerAño())
        self.fecha_inicio.ponerMes(Fecha.obtenerMes())
        self.fecha_inicio.ponerDia(Fecha.obtenerDia())

    def ponerFechaFin(self, Fecha):
        self.fecha_fin.ponerAño(Fecha.obtenerAño())
        self.fecha_fin.ponerMes(Fecha.obtenerMes())
        self.fecha_fin.ponerDia(Fecha.obtenerDia())

    def ponerCuposTotales(self, cupos_totales):
        self.calcularCuposDisponibles(cupos_totales)
        self.cupos_totales = cupos_totales


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



