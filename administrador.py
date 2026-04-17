from usuario import Usuario

class Administrador(Usuario):
    def __init__(self,
                 rango = "Directivo" #atributo con el cual podremos separar entre directivos, secretarios,y demas. De esta forma poniendo accesos acorde a su rango
    ):
        super().__init__()
        self.rango = rango

    def __str__(self):
        return (f"{super().__str__()} \n"
                f" Rango: {self.rango}")

    def poner_rango(self, rango):
        self.rango = rango

    def obtener_rango(self):
        return self.rango

