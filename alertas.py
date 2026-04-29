from poetry.console.commands import self

from materia import Materia

class Alerta_Materia:
    def __init__(self,
                 mensaje = "Mensaje",
                 visto = False,
                 materia = Materia()
    ):
        self.mensaje = mensaje
        self.visto = visto
        self.materia = materia

    def __str__(self):
        return (f"{self.materia.obtener_nombre()}, {self.materia.obtenerHoraInicio() - self.materia.obtenerHoraFin()}\n"
                f"Aula: {self.materia.obtener_aula()} Edificio: {self.materia.obtener_edificio()}")
        '''
        Lo que se moestrara en e string
        Calculo Diferencial 11:00 - 12:10
        Aula: 12 Edificio B
        '''
    def obtener_mensaje(self):
        return self.mensaje

    def obtener_aula(self):
        return self.materia.obtener_aula()

    def obtener_visto(self):
        return self.visto

    def poner_mensaje(self, mensaje):
        self.mensaje = mensaje

    def poner_aula(self, aula):
        self.aula = aula

    def poner_visto(self, visto):
        self.visto = visto



class Alerta:
    def __init__(self,
                 mensaje,
                 visto = False,):

        self.mensaje = mensaje
        self.visto = visto

    def obtener_mensaje(self):
        return self.mensaje

    def obtener_visto(self):
        return self.visto

    def poner_mensaje(self, mensaje):
        self.mensaje = mensaje

    def poner_visto(self, visto):
        self.visto = visto