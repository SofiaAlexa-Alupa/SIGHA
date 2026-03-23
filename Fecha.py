class Fecha: #Clase fecha
    def __init__(self, dia, mes, año):#Nuestra inicializacion de la fecha
        self.dia = dia
        self.mes = mes
        self.año = año

    def ponerDia(self, dia): #Metodo para poner el dia poner el dia dentro de la clase
        self.dia = dia
    def ponerMes(self, mes):#Metodo para poner el mes adentro de la clase
        self.mes = mes
    def ponerAño(self, año):#Metodo para agregar el año adentro de la clase
        self.año = año

    def ObtenerDia(self):#Regresa el dia
        return self.dia
    def ObtenerMes(self):#Regresa el mes
        return self.mes
    def ObtenerAño(self):#Refresa el año
        return self.año

    def __str__(self):#Nos da la fecha formateada en 12/9/2028
        return f"{self.dia}/{self.mes}/{self.año}"