#Librerias utilizadas
import flet as ft

# Interfaz gráfica
import interfaz_grafica as interfaz

# Importar clases del proyecto
from administrador import Administrador
from alumno import Alumno
from maestro import Maestro
from materia import Materia
from nombre import Nombre

#  IMPORTAR BASE DE DATOS 
from database import SessionLocal, Estudiante, Profesor, Materia

#  FUNCIONES PARA CONVERTIR DE BD A OBJETOS
def crear_alumno_desde_bd(estudiante_id):
    """Convierte un registro de BD a objeto Alumno (el que usa la interfaz)"""
    session = SessionLocal()
    try:
        estudiante_db = session.query(Estudiante).filter(Estudiante.usuario_id == estudiante_id).first()
        if not estudiante_db:
            return None
        
        usuario_db = estudiante_db.usuario
        
        # Crear objeto Nombre
        nombre_obj = Nombre(
            usuario_db.nombre,
            usuario_db.apellido_materno,
            usuario_db.apellido_paterno
        )
        
        # Crear objeto Alumno
        alumno = Alumno(
            matricula=estudiante_db.matricula,
            carrera=estudiante_db.carrera,
            semestre=estudiante_db.semestre,
            creditos_obtenidos=estudiante_db.creditos_totales or 0,
            promedio_general=estudiante_db.promedio_general or 0
        )
        
        # Asignar atributos heredados
        alumno.identificacion = usuario_db.identificacion
        alumno.nombre = nombre_obj
        alumno.correo = usuario_db.email
        alumno.contraseña = usuario_db.password
        alumno.rol = usuario_db.rol
        alumno.estado = usuario_db.estado
        alumno.fecha_creacion = usuario_db.fecha_creacion
        
        return alumno
    finally:
        session.close()

def obtener_materias_desde_bd():
    """Obtiene todas las materias de la BD y las convierte a objetos Materia"""
    from hora import Hora
    
    session = SessionLocal()
    try:
        materias_db = session.query(Materia).all()
        materias = []
        
        for m in materias_db:
            # Crear objeto Materia con TODOS los parámetros que espera
            materia = Materia(
                identificacion=str(m.id),
                codigo=m.codigo,
                nombre=m.nombre,
                creditos=m.creditos,
                facultad=m.facultad,
                promedio=0,
                aula=0,
                edificio="",
                dias_clase=[],
                alumnos=[],
                modalidad="Presencial",
                prerequisitos=[],
                profesor_nombre="Sin asignar",
                profesor_correo="correo@udg.mx",
                seccion_nombre="A00",
                cupos_totales=40,
                cupos_disponibles=40,
                hora_inicio=Hora(8, 0),
                hora_fin=Hora(10, 0)
            )
            materias.append(materia)
        
        print(f"✅ Cargadas {len(materias)} materias desde la BD")
        return materias
    finally:
        session.close()

def obtener_alumnos_desde_bd():
    """Obtiene todos los alumnos de la BD"""
    session = SessionLocal()
    try:
        estudiantes_db = session.query(Estudiante).all()
        alumnos = []
        
        for e in estudiantes_db:
            alumno = crear_alumno_desde_bd(e.usuario_id)
            if alumno:
                alumnos.append(alumno)
        
        print(f"✅ Cargados {len(alumnos)} alumnos desde la BD")
        return alumnos
    finally:
        session.close()

def obtener_maestros_desde_bd():
    """Obtiene todos los maestros de la BD"""
    session = SessionLocal()
    try:
        
        profesores_db = session.query(Profesor).all()
        maestros = []
        
        for p in profesores_db:
            usuario_db = p.usuario
            nombre_obj = Nombre(
                usuario_db.nombre,
                usuario_db.apellido_materno,
                usuario_db.apellido_paterno
            )
            
            maestro = Maestro(departamento=p.departamento)
            maestro.identificacion = usuario_db.identificacion
            maestro.nombre = nombre_obj
            maestro.correo = usuario_db.email
            maestro.rol = usuario_db.rol
            
            maestros.append(maestro)
        
        print(f"✅ Cargados {len(maestros)} maestros desde la BD")
        return maestros
    finally:
        session.close()


# FUNCIÓN PRINCIPAL

def main(pagina: ft.Page):
    pagina.title = "SIGHA"
    pagina.vertical_alignment = ft.MainAxisAlignment.CENTER
    pagina.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    pagina.padding = 5
    pagina.bgcolor = "#0f172a"

    print("🔄 Cargando datos desde la base de datos...")
    
    # Cargar datos desde la BD
    db_materias = obtener_materias_desde_bd()
    db_alumnos = obtener_alumnos_desde_bd()
    db_maestros = obtener_maestros_desde_bd()
    
    # Seleccionar el primer alumno para probar (después se integrará con el login)
    if db_alumnos:
        usuario = db_alumnos[0]  # Primer alumno de la BD
        print(f"👤 Usuario cargado: {usuario.nombre} (Alumno)")
        interfaz.interfaz_alumno(pagina, usuario, db_materias)
    elif db_maestros:
        usuario = db_maestros[0]
        print(f"👤 Usuario cargado: {usuario.nombre} (Maestro)")
        interfaz.interfaz_maestro(pagina, usuario)
    else:
        print("❌ No hay usuarios en la BD")
        pagina.add(ft.Text("No hay datos en la base de datos", color="red"))

ft.app(main)

