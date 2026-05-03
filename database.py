from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Time, Date, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime, time, date

Base = declarative_base()
engine = create_engine('sqlute:///sigha.db' , echo=True)
SessionLocal = sessionmaker (bind = engine)

#Tabla Usuario (Base)
class Usuario(Base):
  "Tabla base para todos los usuarios del sistema"
  __tablename__ = 'usuarios'

  id = Column(Integer, primary_key=True, autoincrement=True)
    identificacion = Column(String(20), unique=True, nullable=False) 
    nombre = Column(String(100), nullable=False)
    apellido_paterno = Column(String(50), nullable=False)
    apellido_materno = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    rol = Column(String(20), nullable=False)  # 'estudiante', 'profesor', 'administrador'
    estado = Column(String(20), default='ACTIVO')
    fecha_creacion = Column(Date, nullable=False)
    
    # Relaciones (una fila en Usuario puede tener una fila en las tablas hijas)
    estudiante = relationship("Estudiante", back_populates="usuario", uselist=False)
    profesor = relationship("Profesor", back_populates="usuario", uselist=False)
    administrador = relationship("Administrador", back_populates="usuario", uselist=False)

class Estudiante(Base):
    """Estudiante - hereda de Usuario"""
    _tablename_ = 'estudiantes'
    
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), primary_key=True)
    matricula = Column(String(20), unique=True, nullable=False)
    carrera = Column(String(100), nullable=False)
    semestre = Column(Integer, nullable=False)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="estudiante")
    alertas = relationship("Alerta", back_populates="estudiante")
    notificaciones = relationship("Notificacion", back_populates="estudiante")

class Profesor(Base):
    """Profesor - hereda de Usuario"""
    _tablename_ = 'profesores'
    
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), primary_key=True)
    departamento = Column(String(100), nullable=False)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="profesor")
    secciones = relationship("Seccion", back_populates="profesor")

class Administrador(Base):
    """Administrador - hereda de Usuario"""
    _tablename_ = 'administradores'
    
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), primary_key=True)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="administrador")

# MATERIAS Y SECCIONES 

class Materia(Base):
    """Materia académica"""
    _tablename_ = 'materias'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(20), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    creditos = Column(Integer, nullable=False)
    facultad = Column(String(100), nullable=False)
    
    # Relaciones
    secciones = relationship("Seccion", back_populates="materia")

class Aula(Base):
    """Aula física donde se imparten clases"""
    _tablename_ = 'aulas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    capacidad = Column(Integer, nullable=False)
    recursos = Column(String(200))  # Proyector, pizarrón, etc.
    edificio = Column(String(100), nullable=False)
    
    # Relaciones
    secciones = relationship("Seccion", back_populates="aula")

class Seccion(Base):
    """Sección de una materia (grupo con horario, aula, profesor)"""
    _tablename_ = 'secciones'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo_seccion = Column(String(10), nullable=False)  # Ej: "A00", "B01"
    dias = Column(String(50), nullable=False)  # Ej: "LUN,MIE,VIE" o "LUN,MAR,MIE,JUE,VIE"
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    cupos_totales = Column(Integer, nullable=False)
    cupos_disponibles = Column(Integer, nullable=False)
    
    # Claves foráneas
    materia_id = Column(Integer, ForeignKey('materias.id'), nullable=False)
    profesor_id = Column(Integer, ForeignKey('profesores.usuario_id'), nullable=False)
    aula_id = Column(Integer, ForeignKey('aulas.id'), nullable=False)
    
    # Relaciones
    materia = relationship("Materia", back_populates="secciones")
    profesor = relationship("Profesor", back_populates="secciones")
    aula = relationship("Aula", back_populates="secciones")
    alertas = relationship("Alerta", back_populates="seccion")
    notificaciones = relationship("Notificacion", back_populates="seccion")

#  ALERTAS Y NOTIFICACIONES 

class Alerta(Base):
    """Alerta que un estudiante activa para una sección"""
    _tablename_ = 'alertas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha_activacion = Column(DateTime, default=datetime.utcnow)
    activa = Column(Boolean, default=True)
    
    # Claves foráneas
    estudiante_id = Column(Integer, ForeignKey('estudiantes.usuario_id'), nullable=False)
    seccion_id = Column(Integer, ForeignKey('secciones.id'), nullable=False)
    
    # Relaciones
    estudiante = relationship("Estudiante", back_populates="alertas")
    seccion = relationship("Seccion", back_populates="alertas")
    notificacion = relationship("Notificacion", back_populates="alerta", uselist=False)

class Notificacion(Base):
    """Notificación enviada cuando se libera un cupo"""
    _tablename_ = 'notificaciones'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    mensaje = Column(Text, nullable=False)
    fecha_envio = Column(DateTime, default=datetime.utcnow)
    leida = Column(Boolean, default=False)
    
    # Claves foráneas
    alerta_id = Column(Integer, ForeignKey('alertas.id'), nullable=False)
    estudiante_id = Column(Integer, ForeignKey('estudiantes.usuario_id'), nullable=False)
    seccion_id = Column(Integer, ForeignKey('secciones.id'), nullable=False)
    
    # Relaciones
    alerta = relationship("Alerta", back_populates="notificacion")
    estudiante = relationship("Estudiante", back_populates="notificaciones")
    seccion = relationship("Seccion", back_populates="notificaciones")

# ==================== FUNCIONES CRUD BÁSICAS ====================

class GestionBD:
    """Clase auxiliar para operaciones básicas de BD"""
    
    @staticmethod
    def get_session():
        return SessionLocal()
    
    # Usuarios
    @staticmethod
    def crear_usuario(data):
        session = SessionLocal()
        try:
            usuario = Usuario(**data)
            session.add(usuario)
            session.commit()
            return usuario
        finally:
            session.close()
    
    @staticmethod
    def obtener_usuario_por_email(email):
        session = SessionLocal()
        try:
            return session.query(Usuario).filter(Usuario.email == email).first()
        finally:
            session.close()
    
    # Estudiantes
    @staticmethod
    def crear_estudiante(usuario_data, estudiante_data):
        session = SessionLocal()
        try:
            usuario = Usuario(**usuario_data)
            session.add(usuario)
            session.flush()  # Para obtener el id
            
            estudiante = Estudiante(usuario_id=usuario.id, **estudiante_data)
            session.add(estudiante)
            session.commit()
            return estudiante
        finally:
            session.close()
    
    # Materias
    @staticmethod
    def obtener_materias():
        session = SessionLocal()
        try:
            return session.query(Materia).all()
        finally:
            session.close()
    
    # Secciones disponibles
    @staticmethod
    def obtener_secciones_disponibles():
        session = SessionLocal()
        try:
            return session.query(Seccion).filter(Seccion.cupos_disponibles > 0).all()
        finally:
            session.close()
    
    # Alertas
    @staticmethod
    def activar_alerta(estudiante_id, seccion_id):
        session = SessionLocal()
        try:
            alerta = Alerta(estudiante_id=estudiante_id, seccion_id=seccion_id)
            session.add(alerta)
            session.commit()
            return alerta
        finally:
            session.close()
    
    @staticmethod
    def obtener_alertas_activas_por_estudiante(estudiante_id):
        session = SessionLocal()
        try:
            return session.query(Alerta).filter(
                Alerta.estudiante_id == estudiante_id,
                Alerta.activa == True
            ).all()
        finally:
            session.close()

# CREAR TABLAS
def inicializar_bd():
  "Crea las tablas, si no existen"
  Base.metadata.create_all(bind = engine)
print("Archivo: sigha.db")
print("\n Tablas creadas:")
for table in Base.metadata.tables.keys():
  print(f"    - {Table}")

if __name__ == "__main__":
  inicializar_bd()



  





