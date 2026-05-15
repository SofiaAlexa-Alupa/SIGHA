from usuario import Usuario

class Alumno(Usuario):
    def __init__(self,
                 matricula = "*J#NF*#H",#Matricula del estudiante, es un string
                 carrera = "Ingenieria en ingeniosidad", #Carrera del estudiante
                 semestre = 1, #Memestre que cursa el estudiante, al iniciar sera el primer semestre
                 creditos_obtenidos = 0,#Creditos obtenidos de las materias que ya curso
                 promedio_general = 0,#Promedio, calculado por las materias que ya curso
                 materias_actuales = None,#Una lista de las materias que cursa en el grado actual
                 materias_pasadas = None,#Las materias que ya paso, se guardaran aqui como un record
                 materias_simuladas = None):#Materias agregadas al simulador

        super().__init__()

        self.matricula = matricula
        self.carrera = carrera
        self.semestre = semestre
        self.creditos_obtenidos = creditos_obtenidos
        self.promedio_general = promedio_general

        #Evita compartir listas entre objetos
        self.materias_actuales = (
            materias_actuales
            if materias_actuales is not None
            else []
        )

        self.materias_pasadas = (
            materias_pasadas
            if materias_pasadas is not None
            else []
        )

        #Lista exclusiva para el simulador de horarios
        self.materias_simuladas = (
            materias_simuladas
            if materias_simuladas is not None
            else []
        )


    def __str__(self):#Devuelve un string con la informacion EXCLUSIVA del estudiante
        return (f"Estudiante: {self.nombre}\n"
                f"Matricula: {self.matricula}\n"
                f"Carrera: {self.carrera}\n"
                f"Promedio general: {self.promedio_general}\n"
                )

    def obtener_string_usuario(self):#Devuelve un string con la informacion de la clase usuario
        return super().__str__()


    
       
       #METODOS QUE MODIFICAN ATRIBUTOS#
       
    

    def poner_matricula(self, matricula):#Modifica el atributo matricula
        self.matricula = matricula

    def poner_carrera(self, carrera):#Modifica el atributo carrera
        self.carrera = carrera

    def poner_semestre(self, semestre):#Modifica el atributo semestre
        self.semestre = semestre


    
       #METODOS OPERACIONALES#
       

    def calcular_creditos_obtenidos(self):#Calcula los creditos obtenidos

        self.creditos_obtenidos = 0

        for materia in self.materias_pasadas:

            self.creditos_obtenidos += (
                materia.obtener_creditos()
            )


    def calcular_promedio_general(self):#Calcula el promedio general

        if len(self.materias_pasadas) == 0:
            self.promedio_general = 0
            return

        promedio = 0

        for materia in self.materias_pasadas:#Recorre cada materia

            promedio += (
                materia.obtener_promedio()
            )#Suma los promedios

        self.promedio_general = (
            promedio / len(self.materias_pasadas)
        )#Promedia todas las materias


    def limpiar_materias_actuales(self):#Limpia materias actuales

        for materia in self.materias_actuales:

            if materia not in self.materias_pasadas:

                self.materias_pasadas.append(materia)

        self.materias_actuales.clear()


    def agregar_materia(self, materia):#Agrega materia actual

        if materia not in self.materias_actuales:

            self.materias_actuales.append(materia)


    def eliminar_materia(self, materia):#Elimina materia actual

        if materia in self.materias_actuales:

            self.materias_actuales.remove(materia)


       #SIMULADOR DE HORARIOS#
      

    def agregar_materia_simulada(self, materia):#Agrega materia al simulador

        if materia not in self.materias_simuladas:

            self.materias_simuladas.append(materia)


    def eliminar_materia_simulada(self, materia):#Elimina materia del simulador

        if materia in self.materias_simuladas:

            self.materias_simuladas.remove(materia)


    def limpiar_simulacion(self):#Limpia simulador

        self.materias_simuladas.clear()


    def verificar_conflictos_horario(self):#Detecta empalmes de horario

        conflictos = []

        for i in range(len(self.materias_simuladas)):

            materia1 = self.materias_simuladas[i]

            for j in range(i + 1, len(self.materias_simuladas)):

                materia2 = self.materias_simuladas[j]

                dias1 = materia1.obtener_dias_clase()
                dias2 = materia2.obtener_dias_clase()

                coincidencias = (
                    set(dias1) & set(dias2)
                )

                if coincidencias:

                    inicio1 = (
                        materia1.obtenerHoraInicio().hora
                    )

                    fin1 = (
                        materia1.obtenerHoraFin().hora
                    )

                    inicio2 = (
                        materia2.obtenerHoraInicio().hora
                    )

                    fin2 = (
                        materia2.obtenerHoraFin().hora
                    )

                    if (
                        inicio1 < fin2
                        and inicio2 < fin1
                    ):

                        conflictos.append(
                            (materia1, materia2)
                        )

        return conflictos


   
       #NOTIFICACIONES#
       
    def recibir_notificacion(self, notificacion):#Agrega notificacion

        self.notificaciones.append(notificacion)


   
       #METODOS QUE DEVUELVEN ATRIBUTOS#
      

    def obtener_matricula(self):#Metodo que devuelve la matricula
        return self.matricula

    def obtener_carrera(self):#Metodo que devuelve la carrera
        return self.carrera

    def obtener_semestre(self):#Metodo que devuelve el semestre
        return self.semestre

    def obtener_creditos_obtenidos(self):#Metodo que devuelve creditos
        return self.creditos_obtenidos

    def obtener_promedio_general(self):#Metodo que devuelve promedio
        return self.promedio_general

    def obtener_materias_pasadas(self):#Metodo que devuelve materias pasadas
        return self.materias_pasadas

    def obtener_materias_actuales(self):#Metodo que devuelve materias actuales
        return self.materias_actuales

    def obtener_materias_simuladas(self):#Metodo que devuelve simulador
        return self.materias_simuladas