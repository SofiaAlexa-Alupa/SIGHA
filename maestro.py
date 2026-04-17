from usuario import Usuario

class Maestro(Usuario):
    def __init__(self,
                 departamento = "Computacion"):

        super().__init__()
        self.departamento = departamento

    def __str__(self):
        return (f"{super().__str__()} \n"
                f"Departamento: {self.departamento}")

    def poner_departamento(self, departamento):
        self.departamento = departamento

    def obtener_departamento(self):
        return self.departamento