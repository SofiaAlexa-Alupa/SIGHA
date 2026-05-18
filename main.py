#Librerias utilizadas
import flet as ft

# Interfaz gráfica
import interfaz_grafica as interfaz

# Importar clases del proyecto
from administrador import Administrador as Administrador_logico
from alumno import Alumno
from maestro import Maestro
from materia import Materia
from nombre import Nombre

# IMPORTAR BASE DE DATOS
from database import SessionLocal, Estudiante, Profesor, Administrador, MateriaDB

#  FUNCIONES DE CONVERSIÓN 

def crear_alumno_desde_bd(estudiante_id):
    """Convierte un registro de BD a objeto Alumno"""
    session = SessionLocal()
    try:
        estudiante_db = session.query(Estudiante).filter(Estudiante.usuario_id == estudiante_id).first()
        if not estudiante_db:
            return None
        
        usuario_db = estudiante_db.usuario
        
        nombre_obj = Nombre(
            usuario_db.nombre,
            usuario_db.apellido_materno,
            usuario_db.apellido_paterno
        )
        
        alumno = Alumno(
            matricula=estudiante_db.matricula,
            carrera=estudiante_db.carrera,
            semestre=estudiante_db.semestre,
            creditos_obtenidos=estudiante_db.creditos_totales or 0,
            promedio_general=estudiante_db.promedio_general or 0
        )
        
        alumno.identificacion = usuario_db.identificacion
        alumno.nombre = nombre_obj
        alumno.correo = usuario_db.email
        alumno.contraseña = usuario_db.password
        alumno.rol = usuario_db.rol
        alumno.estado = usuario_db.estado
        
        return alumno
    except Exception as e:
        print(f"Error al crear alumno: {e}")
        return None
    finally:
        session.close()


def obtener_materias_desde_bd():
    """Obtiene todas las materias de la BD y las convierte a objetos Materia"""
    from hora import Hora
    
    session = SessionLocal()
    try:
        materias_db = session.query(MateriaDB).all()
        materias = []
        
        for m in materias_db:
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
        
        print(f" Cargadas {len(materias)} materias desde la BD")
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
        
        print(f"Cargados {len(alumnos)} alumnos desde la BD")
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
        
        print(f" Cargados {len(maestros)} maestros desde la BD")
        return maestros
    finally:
        session.close()


def obtener_administradores_desde_bd():
    """Obtiene todos los administradores de la BD"""
    session = SessionLocal()
    try:
        admins_db = session.query(Administrador).all()
        administradores = []
        
        for a in admins_db:
            usuario_db = a.usuario
            nombre_obj = Nombre(
                usuario_db.nombre,
                usuario_db.apellido_materno,
                usuario_db.apellido_paterno
            )
            
            admin = Administrador_logico()
            admin.identificacion = usuario_db.identificacion
            admin.nombre = nombre_obj
            admin.correo = usuario_db.email
            admin.contraseña = usuario_db.password
            admin.rol = usuario_db.rol
            admin.estado = usuario_db.estado
            
            administradores.append(admin)
        
        print(f"✅ Cargados {len(administradores)} administradores desde la BD")
        return administradores
    finally:
        session.close()


# FUNCIÓN PRINCIPAL 

def main(pagina: ft.Page):
    pagina.title = "SIGHA"
    pagina.vertical_alignment = ft.MainAxisAlignment.CENTER
    pagina.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    pagina.padding = 5
    pagina.bgcolor = "#0f172a"
    pagina.window_prevent_close = True

    print("🔄 Cargando datos desde la base de datos...")
    
    # Cargar datos desde la BD
    db_materias = obtener_materias_desde_bd()
    db_alumnos = obtener_alumnos_desde_bd()
    db_maestros = obtener_maestros_desde_bd()
    db_administradores = obtener_administradores_desde_bd()


    interfaz.login(pagina=pagina,
                   alumnos=db_alumnos,
                   maestros=db_maestros,
                   administradores=db_administradores,
                   materias = db_materias)


ft.app(main)
