#Librerias utilizadas
import flet as ft

#interfaz codficada
import interfaz_grafica as interfaz

#Importacion de las clases
from administrador import Administrador
from alumno import Alumno
from maestro import Maestro
from materia import Materia

#  IMPORTAR LA BASE DE DATOS
from database import GestionBD, SessionLocal, Usuario as UsuarioDB, Estudiante as EstudianteDB, Profesor as ProfesorDB, Materia as MateriaDB, Seccion as SeccionDB

#  FUNCIONES PARA CONVERTIR DE BD A OBJETOS 

def crear_alumno_desde_bd(estudiante_id):
    """Toma un estudiante de la BD y lo convierte en objeto Alumno (el de ellos)"""
    session = SessionLocal()
    try:
        # Obtener datos de la BD
        estudiante_db = session.query(EstudianteDB).filter(EstudianteDB.usuario_id == estudiante_id).first()
        if not estudiante_db:
            return None
        
        usuario_db = estudiante_db.usuario
        
        # Crear objeto Nombre 
        from nombre import Nombre
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
            creditos_obtenidos=estudiante_db.creditos_totales,
            promedio_general=estudiante_db.promedio_general
        )
        
        # Asignar atributos heredados de Usuario
        alumno.identificacion = usuario_db.identificacion
        alumno.nombre = nombre_obj
        alumno.correo = usuario_db.email
        alumno.contraseña = usuario_db.password
        alumno.rol = usuario_db.rol
        alumno.estado = usuario_db.estado
        
        return alumno
    finally:
        session.close()

def crear_maestro_desde_bd(profesor_id):
    """Toma un profesor de la BD y lo convierte en objeto Maestro (el de ellos)"""
    session = SessionLocal()
    try:
        profesor_db = session.query(ProfesorDB).filter(ProfesorDB.usuario_id == profesor_id).first()
        if not profesor_db:
            return None
        
        usuario_db = profesor_db.usuario
        
        from nombre import Nombre
        nombre_obj = Nombre(
            usuario_db.nombre,
            usuario_db.apellido_materno,
            usuario_db.apellido_paterno
        )
        
        maestro = Maestro(
            departamento=profesor_db.departamento
        )
        
        maestro.identificacion = usuario_db.identificacion
        maestro.nombre = nombre_obj
        maestro.correo = usuario_db.email
        maestro.contraseña = usuario_db.password
        maestro.rol = usuario_db.rol
        maestro.estado = usuario_db.estado
        
        return maestro
    finally:
        session.close()

def obtener_materias_desde_bd():
    """Obtiene todas las materias de la BD y las convierte a objetos Materia (los de ellos)"""
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
                facultad=m.facultad
            )
            materias.append(materia)
        
        return materias
    finally:
        session.close()



#  FUNCIÓN PRINCIPAL 

def main(pagina: ft.Page):
    pagina.title = "SIGHA"
    pagina.vertical_alignment = ft.MainAxisAlignment.CENTER
    pagina.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    pagina.padding = 5
    pagina.bgcolor = "#0f172a"

    #  CARGAR DATOS REALES DESDE LA BD
    # Por ahora, usamos el primer estudiante y primer profesor de la BD para pruebas
    # Después se cambiará ésto con un login real
    
    session = SessionLocal()
    try:
        primer_estudiante = session.query(EstudianteDB).first()
        primer_profesor = session.query(ProfesorDB).first()
        primer_admin = session.query(Administrador).first() if 'Administrador' in dir() else None
    finally:
        session.close()
    
    # Cargar materias desde BD
    db_materias = obtener_materias_desde_bd()
    
    # Cargar alumnos y maestros desde BD
    db_alumnos = []
    db_maestros = []
    
    session = SessionLocal()
    try:
        estudiantes_db = session.query(EstudianteDB).all()
        for e in estudiantes_db:
            alumno = crear_alumno_desde_bd(e.usuario_id)
            if alumno:
                db_alumnos.append(alumno)
        
        profesores_db = session.query(ProfesorDB).all()
        for p in profesores_db:
            maestro = crear_maestro_desde_bd(p.usuario_id)
            if maestro:
                db_maestros.append(maestro)
    finally:
        session.close()
    
    #  SELECCIONAR USUARIO PARA PRUEBA 
    # Temporal: usa el primer alumno para probar
    # Cambia a primer_profesor o primer_admin según se pueda probar
    
    if db_alumnos:
        usuario = db_alumnos[0]  # Usar el primer alumno de la BD
        print(f"✅ Usuario cargado: {usuario.nombre}")
        interfaz.interfaz_alumno(pagina, usuario, db_materias)
    elif db_maestros:
        usuario = db_maestros[0]
        print(f"✅ Usuario cargado: {usuario.nombre}")
        interfaz.interfaz_maestro(pagina, usuario)
    else:
        # Si no hay datos, crear uno de prueba
        print("⚠️ No hay datos en la BD. Crea algunos primero.")
        usuario = Maestro()
        interfaz.interfaz_maestro(pagina, usuario)


ft.run(main)
#Lo único que se debe hacer después, será reemplazar el usuario (El primer alumno de la bd)
# con el usuario que realmente inicio sesión cuando se implemente el login
