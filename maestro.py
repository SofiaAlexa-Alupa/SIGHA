import alertas
from materia import Materia
from usuario import Usuario
from alertas import Alerta

class Maestro(Usuario):
    def __init__(self,
                 departamento:str = "Computacion",
                 disponibilidad = None,
                 materias:list[Materia] = [],
                 notificaciones: list[Alerta] = None,):


        super().__init__()
        self.departamento = departamento
        self.disponibilidad = disponibilidad if disponibilidad is not None else [[0]*7 for _ in range(7)]
        self.materias = materias if materias is not None else []
        self.alertas = notificaciones if notificaciones is not None else []

    def __str__(self):
        return (f"{super().__str__()} \n"
                f"Departamento: {self.departamento}")

    def poner_departamento(self, departamento):
        self.departamento = departamento

    def agregar_materia(self, materia):
        self.materias.append(materia)


    def eliminar_materia(self, materia):
        self.materias.remove(materia)

    def limpiar_materias(self):
        self.materias.clear()

    def agregar_alerta(self, alerta):
        self.alertas.append(alerta)

    def depurar_alertas(self):

        if self.alertas is None:
            return

        self.alertas = [alerta for alerta in self.alertas if not alerta.obtener_visto()]

    def poner_disponibilidad(self, disponibilidad):
        self.disponibilidad = disponibilidad

    def obtener_departamento(self):
        return self.departamento

    def obtener_disponibilidad(self):
        return self.disponibilidad
