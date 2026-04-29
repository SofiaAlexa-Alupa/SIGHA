from fecha import Fecha
from nombre import Nombre
import secrets
import string


class Usuario:
    def __init__(self,
                 identificacion = "000000",
                 estado = "ACTIVO",
                 nombre = Nombre(),
                 correo = "Kuakitikuak@alumnos.udg.mx",
                 numero_telefono = 22039164,
                 contraseña = "FJH4tfgv:{;",
                 rol = "Creado",
                 fecha_creacion = Fecha(),
                 notificaciones = []):

        self.identificacion = identificacion
        self.estado = estado
        self.nombre = nombre
        self.correo = correo
        self.numero_telefono = numero_telefono
        self.contraseña = contraseña
        self.rol = rol
        self.fecha_creacion = fecha_creacion
        self.notificaciones = notificaciones

    def __str__(self):
        return (f"Codigo:  {self.identificacion}\n"
                f"Nombre:  {self.nombre}\n"
                f"Estado: {self.estado}\n"
                f"Correo: {self.correo}\n"
                f"Rol: {self.rol}\n"
                f"Activo desde: {self.fecha_creacion}\n")


    '''
       ##########################################
       #Metodos operacionales dentro de la clase#
       ##########################################
     '''

    def generarContraseñaAleatoria(self):#Funcion que genera una contraseña aleatoria
        #Definir caracteres posibles de la contraseña
        caracteres = string.ascii_letters + string.digits + string.punctuation
        #Generar la contraseña utilizando los caracteres de forma aleatoria
        contraseña = "".join(secrets.choice(caracteres) for _ in range(12))
        return contraseña


    '''
      #################################
      #METODOS QUE MODIFICAN ATRIBUTOS#
      #################################
      '''

    def ponerIdentificacion(self, identificacion):#Metodo que modifica el id del usuario
        self.identificacion = identificacion

    def ponerNombre(self, nombre): #Metodo que cambia el nombre del usuario
        self.nombre = nombre

    def ponerCorreo(self, correo):#Metodo que modifica el correo
        self.correo = correo

    def ponerContraseña(self, contraseña): #Metodo que modifica la contraseña
        self.contraseña = contraseña

    def ponerRol(self, rol): #Metodo que modifica el rol del usuario
        self.rol = rol

    def ponerFecha_Creacion(self, fecha):#Metodo que modifica la fecha de creacion
        self.fecha_creacion = fecha

    def ponerNumeroTelefono(self, telefono):
        self.numero_telefono = telefono

    def agregarNotificacion(self, notificacion):
        self.notificaciones.append(notificacion)

    '''
     #####################################
     #Metodos para devolver los atributos#
     #####################################
     '''

    def obtenerIdentificacion(self):#Metodo que devuelve el codigo del usuario
        return self.identificacion

    def obtenerEstado(self):#Metodo que devuelve el estado del usuario
        return self.estado

    def obtenerNombre(self):#Metodo que devuelve el nombre de usuario
        return self.nombre

    def obtenerCorreo(self):#Metodo que devuelve el correo del usuario
        return self.correo

    def obtenerContraseña(self):#Metodo que devuelve la contraseña del usuario
        return self.contraseña

    def obtenerRol(self): #Metodo que devuelve el rol del usuario
        return self.rol

    def obtenerFecha_Creacion(self):#Metodo que devuelve la fecha de creacion de la cuenta del usuario
        return self.fecha_creacion

    def obtenerNumeroTelefono(self):
        return self.numero_telefono

    def quitar_todas_notificacion(self):
        self.notificaciones.clear()

    def quitar_vistos(self):
        if self.notificaciones:
            notificaciones_activas = [notificacion for notificacion in self.notificaciones if not notificacion.]
            return notificaciones_activas

