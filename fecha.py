from datetime import date

class Fecha:
    def __init__(self, dia = 24, mes = 5, año = 2026):
        self.dia = dia #Dia es un atributo tipo entero
        self.mes = mes #Mes es un atributo entero
        self.año = año #año tambien es un atributo entero

    def __str__(self):
        return f"{self.dia}/{self.mes}/{self.año}"

    '''
       ##########################################
       #Metodos operacionales dentro de la clase#
       ##########################################
     '''

    def validar(self, dia, mes, año):
        # 1. Comprobamos el año
        if año < 1:
            return False

        # 2. Comprobamos el mes (debe ser entre 1 y 12)
        if mes <= 0 or mes > 12:
            return False

        # 3. Lista con los días máximos de cada mes
        dias = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        # 4. Comprobamos si el AÑO es bisiesto
        if self.esBisiesto(año):
            dias[1] = 29   # Si es bisiesto, cambiamos los días de febrero a 29


        # 5. Comprobamos que el día sea mayor que 0 y no supere el límite de su mes
        if dia <= 0 or dia > dias[mes - 1]:
            return False

        # Si sobrevive a todos los 'if', la fecha es válida
        return True

    def esBisiesto(self, año):#Funcion  que retorna si es biciesto o no
        return año % 4 == 0 and (año % 100 != 0 or año % 400 == 0)

    def diasTotales(self):
        dias = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]#Agregamos un arreglo con  los dias del año
        total = 0 #Nuestra variable que se ira actualizando con los diastotales desde el año 1 hasta la fecha que tenga el objeto

        for ciclo in range(1, self.año):#Recorremos Año por año para agregar los dias
            if(self.esBisiesto(ciclo)):#En caso de qe sea biciesto
                total += 366#Se agregara un dia extra
            else:#En caso de que no
                total += 365#Se agregaran los dias como un año normal

        for ciclo in range(1, self.mes):#Ahora recoreremos los dias de los meses hasta el mes del año actual
            if self.esBisiesto(self.año) and ciclo == 2:#Si es biciesto el año que tiene el objeto
                total += 29#Se agregara 29 dias por ser biciesto
            else:#En caso de qe
                total += dias[ciclo-1]

        total += self.dia#Sumamos los dias de nuestra fecha actual

        return total

    def calculoDiferenciaDias(self, Fecha):#Recibe una fecha y trabaja con la fecha del objeto y la fecha que le pasemos
        return abs(self.diasTotales() - Fecha.diasTotales()) #Calcula la diferencia absoluta entre una fecha y nuestra fecha

    '''
    #################################
    #METODOS QUE MODIFICAN ATRIBUTOS#
    #################################
    '''
    def ponerDia(self, dia):#Cambia el atributo Dia
        self.dia = dia

    def ponerMes(self, mes):#Cambia el atributo mes
        self.mes = mes

    def ponerAño(self, año):#Cambia el atributo año
        self.año = año



    '''
    #################################
    #METODOS QUE DEVULEVEN ATRIBUTOS#
    #################################
    '''

    def obtenerDia(self):#Devuelve el atributo dia
        return self.dia

    def obtenerMes(self):#Devuelve el atributo mes
        return self.mes

    def obtenerAño(self):#Devuelve el atributo año
        return self.año






