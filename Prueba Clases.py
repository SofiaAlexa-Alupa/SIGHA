from fecha import Fecha
from hora import Hora
from nombre import Nombre
from seccion import Seccion
#Prueba metodo init
date = Fecha(1,12,2024)
#Prueba metodo str
print(date)
 #Prueva de validacion
 #Casos negativos
print(date.validar(0,12,2012))#Si el dia es menor a 1
print(date.validar(32,12,2012))#Si el dia es mayor al dia maximo de su dia correspondiente
print(date.validar(1,13,2012))#Si el mes es mayor a 12
print(date.validar(1, 0, 2000))#Si el mes en menor a 1
print(date.validar(29,2,2015))#En caso  de que no sea bicisesto
print(date.validar(29,2,2100))#Si es biciesto pero divicible entre 100
print(date.validar(1, 1, 0))#Si el año es menor a 1
 #Casos positivos
print(date.validar(1, 1, 1))#Si todo es mayor a 1
print(date.validar(31, 1, 2))#Si el dia esta entre el rango de su mes correspondiente
print(date.validar(29, 2, 2016))#Si el año es biciesto, febrero tiene 29 dias
print(date.validar(29, 2, 2000))#Si el añó es divicible entre 100 y 400

date2 = Fecha(1,12,2025)

print(date.calculoDiferenciaDias(date2))#Comporbacion de la diferencia entre dos fechas

#Comporabmos los  metodos que ponen las fechas
date.ponerDia(23)
date.ponerMes(5)
date.ponerAño(9)
print(date)

print(date.obtenerAño())
print(date.obtenerMes())
print(date.obtenerDia())

#Purueba de Hora
hora = Hora()
print(hora)
hora = Hora(1,12,)
print(hora)

#Validaciones
print(hora.validar(0,0))
print(hora.validar(12,60))
print(hora.validar(-1,59))
print(hora.validar(24,59))
print(hora.validar(23,59))
print(hora.validar(0,0))
print(hora.validar(11,59))
print(hora.validar(23,59))

hora.ponerHora(12)
hora.ponerMinuto(12)
print(hora)

print(hora.obtenerHora())
print(hora.obtenerMinuto())

#Pruebas nombre
nombre = Nombre()
print(nombre)
nombre = Nombre("Joshua Ramon", "Rivas Rosales")
print(nombre)
nombre.ponerNombre("Mesuda")
nombre.ponerApellido("Hidrosooo")
print(nombre)
print(nombre.obtenerApellido())
print(nombre.obtenerNombre())

seccion = Seccion()
print(seccion)