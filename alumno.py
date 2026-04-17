from usuario import Usuario

class Alumno(Usuario):
    def __init__(self,
                 matricula = "*J#NF*#H",#Matricula del estudiante, es un string
                 carrera = "Ingenieria en ingeniosidad", #Caarrera del estudiante
                 semestre = 1, #Memestre que cursa el estudiante, al iniciar sera el primer semestre
                 creditos_obtenidos = 0,#Creditos obtenidos de las materias que ya curso
                 promedio_general = 0,#Promedio, calculado por las materias que ya curso
                 materias_actuales = [],#Una lista de las materias que cursa en el grado actual
                 materias_pasadas = []):#Las materias que ya paso, se guardaran aqui como un record

        super().__init__()
        self.matricula = matricula
        self.carrera = carrera
        self.semestre = semestre
        self.creditos_obtenidos = creditos_obtenidos
        self.promedio_general = promedio_general
        self.materias_actuales = materias_actuales
        self.materias_pasadas = materias_pasadas


    def __str__(self):#Devuelve un string con la informacion EXCUSIVA del estudiante
        return (f"Estudiante: {self.nombre}\n"
                f"Matricula: {self.matricula}\n"
                f"Carrera: {self.carrera}\n"
                f"Promedio general: {self.promedio_general}\n"
                )

    def obtener_string_usuario(self):#Devuelve un string con la informacion de la clase usuario
        return super().__str__()

    def poner_matricula(self, matricula):#Modifica el atributo matricula
        self.matricula = matricula

    def poner_carrera(self, carrera):#Modifica el aatributo carrera
        self.carrera = carrera

    def poner_semestre(self, semestre):#Modifica el atributo semestre
        self.semestre = semestre

    def calcular_creditos_obtenidos(self):#Modificael atributo de creditos obtenidos
        for materia in self.materias_actuales:
            self.creditos_obtenidos += materia.obtener_creditos()#Se agregaran de las materias actuales los creditos obtenidos

    def calcular_promedio_general(self):#Calcula el promedio de las materias cursadas en toda las trayectoria del estudainte
        promedio = 0
        for materia in self.materias_pasadas:#recorre cada materia
            promedio += materia.obtener_promedio()#Suma los promedios de las materias

        self.promedio_general = promedio / len(self.materias_pasadas)#Y las promedia entre todas

    def limpiar_materias_actuales(self):#Las materias que tomo en el ciclo escular
        for materia in self.materias_pasadas:
            self.materias_pasadas.append(materia)#Pasan a otra lista que contiene todas las materias que alguna vez curso

        self.materias_actuales.clear()#Limpia la lista de las amterias cursadas en el semestre actual

    def agregar_materias(self, materias):#atributo que agrega materias a la lista de materias
        self.materias_actuales.append(materias)

    def obtener_matricula(self):#Metodo que devuelve la matricula
        return self.matricula

    def obtener_carrera(self):#Metodo que decuelve la carrera
        return self.carrera

    def obtener_semestre(self):#MEtodo que devuelve el semestre
        return self.semestre

    def obtener_creditos_obtenidos(self):#Metodo que devuelve los creditos obtenidos
        return self.creditos_obtenidos

    def obtener_promedio_general(self):#Metodo que devuelve el promedio general
        return self.promedio_general

    def obtener_materias_pasadas(self):#Metodo que devuelve las materias pasadas
        return self.materias_pasadas

    def obtener_materias_actuales(self):#Metodo que devuelve las materias actuales
        return self.materias_actuales

