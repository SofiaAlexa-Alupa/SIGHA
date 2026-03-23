class Nombre:
    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido

    def ponerNombre(self, nombre): #Funcion recibe un nombre, pone el nombre dentro de la clase
        self.nombre = nombre

    def ponerApellido(self, apellido):#Funcion para poner apellido dentro de la clase
        self.apellido = apellido

    def obtenerNombre(self): #Funcion para recuperar solo el nombre de manera individual
        return self.nombre

    def obtenerApellido(self):#Funcion para recuperar el apellido de manera individual
        return self.apellido

    def __str__(self):
        return (f"Apellido(s): {self.apellido} \n" 
                f"Nombre: {self.nombre} \n")

