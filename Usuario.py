class Usuario():
    def __init__(self,id, nombre, email,
                 contraseña, rol, fechaInscripcion, actvio):
        self.id = id #Identidicacion del usuario
        self.nombre = nombre# Nombre dde usuario, se usara la clase Nombre
        self.email = email#Correo del usuario
        self.contraseña = contraseña#Contraseñá del usuario
        self.rol = rol #Especificamos el rol para obtener diferentes funciones dependiendo del nivel (Prosefos no tendra los mismos privilegios que alumno)
        self.fechaInscripcion = fechaInscripcion#Cuando se inscribio el usuario en la plataforma
        self.activo = actvio#Variable booleana para saber si es una persona que actualmente desempeñé algun rol dentro de la institucion


        '''
        TODO:
        * Hacer la funcion que agregue el ID de los neuvos usuarios
        * Hacer el metodo de inscripcion
        '''

    def ponerNombre(self, nombre):#Ponemos el nombre ya
        self.nombre = nombre
    def ponerCorreo(self, email):#Metodo para agregar el correo
        self.email = email
    def ponerContraseña(self, contraseña):#metodo para agregar o cambiar la contraseñá
        self.contraseña = contraseña
    def ponerRol(self, tipoRol):#Metodo el cual pediremos un numero [1-3], si el numero supera este rango, no se podra
        if (tipoRol >=  1 or tipoRol <= 3):#Si esta dentro del rango, se usara el diccionario para identificar el tipo de rol
            tiposUsuarios = { #Los tipos de usuario disponibles
                1 : "Estudiante", #Si el numero es 1, entoces sera estudiante
                2 : "Profesor", #Si el numero es 2, Sera profesor
                3 : "Administrativo" #Si el numero 3 es Administrador
            }
            self.rol = tiposUsuarios[tipoRol] #Una vez definido, usamos el numero para dictaminar el rol definido en el diccionario
        else:
            self.rol = None #En caso de algun error, se pondra en Nulo.
    def ponerFechaInscripcion(self, fechaInscripcion):#Tomamos la fecha de inscripcion y la aregamos
        self.fechaInscripcion = fechaInscripcion
    def ponerActivo(self, activo): #Definimos si esta activo o no, es un booleano
        self.activo = activo


    def obtenerId(self):#Metodo  para obtener el id
        return self.id
    def obtenerNombre(self):#Metodo para obtener el nombre del usuario
        return self.nombre
    def obtenerCorreo(self):#Metodo para obtener el correo
        return self.email
    def obtenerRol(self):#Metodo para obtener el rol del usuario
        return self.rol
    def obtenerFechaInscripcion(self):#Metodo para obtener la fecha cuando se activo el usuario
        return self.fechaInscripcion
    def obtenerActivo(self):#Funcion para obtener un booleano para comporbar si es activo o no
        return self.activo

    def __str__(self):
        estatus = ""
        if self.rol is True:
            estatus = "ACTIVO"
        if self.rol is False:
            estatus = "INACTIVO"

        return (f"Estado: {estatus}"
                f"Idenficacion: {self.id}"
                f"Nombre: {self.nombre}"
                f"Correo electronico: {self.email}"
                f"{self.rol}"
                f"Fecha de inscripcion: {self.fechaInscripcion}")

