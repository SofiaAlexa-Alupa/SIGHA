from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Time, Date, ForeignKey, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime, time, date

Base = declarative_base()
engine = create_engine('sqlite:///sigha.db', echo=True)
SessionLocal = sessionmaker(bind=engine)

# TABLA USUARIO (BASE) 

class Usuario(Base):
    """Tabla base para todos los usuarios del sistema"""
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
    
    # Relaciones
    estudiante = relationship("Estudiante", back_populates="usuario", uselist=False)
    profesor = relationship("Profesor", back_populates="usuario", uselist=False)
    administrador = relationship("Administrador", back_populates="usuario", uselist=False)


class Estudiante(Base):
    """Estudiante - hereda de Usuario"""
    __tablename__ = 'estudiantes'
    
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), primary_key=True)
    matricula = Column(String(20), unique=True, nullable=False)
    carrera = Column(String(100), nullable=False)
    semestre = Column(Integer, nullable=False)
    creditos_totales = Column(Integer, default=0)
    promedio_general = Column(Float, default=0.0)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="estudiante")
    alertas = relationship("Alerta", back_populates="estudiante")
    notificaciones = relationship("Notificacion", back_populates="estudiante")
    inscripciones = relationship("Inscripcion", back_populates="estudiante", cascade="all, delete-orphan")


class Profesor(Base):
    """Profesor - hereda de Usuario"""
    __tablename__ = 'profesores'
    
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), primary_key=True)
    departamento = Column(String(100), nullable=False)
    
    usuario = relationship("Usuario", back_populates="profesor")
    secciones = relationship("Seccion", back_populates="profesor")


class Administrador(Base):
    """Administrador - hereda de Usuario"""
    __tablename__ = 'administradores'
    
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), primary_key=True)
    
    usuario = relationship("Usuario", back_populates="administrador")


#  MATERIAS, AULAS Y SECCIONES 

class Materia(Base):
    """Materia académica"""
    __tablename__ = 'materias'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(20), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    creditos = Column(Integer, nullable=False)
    facultad = Column(String(100), nullable=False)
    
    secciones = relationship("Seccion", back_populates="materia")


class Aula(Base):
    """Aula física donde se imparten clases"""
    __tablename__ = 'aulas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    capacidad = Column(Integer, nullable=False)
    recursos = Column(String(200))
    edificio = Column(String(100), nullable=False)
    
    secciones = relationship("Seccion", back_populates="aula")


class Seccion(Base):
    """Sección de una materia (grupo con horario, aula, profesor)"""
    __tablename__ = 'secciones'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo_seccion = Column(String(10), nullable=False)
    dias = Column(String(50), nullable=False)  # Ej: "LUN,MIE,VIE"
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
    inscripciones = relationship("Inscripcion", back_populates="seccion")


# INSCRIPCIONES (KARDEX)

class Inscripcion(Base):
    """Registro de un estudiante en una sección (para kardex)"""
    __tablename__ = 'inscripciones'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    estudiante_id = Column(Integer, ForeignKey('estudiantes.usuario_id'), nullable=False)
    seccion_id = Column(Integer, ForeignKey('secciones.id'), nullable=False)
    periodo = Column(String(10), nullable=False)  # Ej: "2024A", "2024B"
    calificacion = Column(Float, default=0.0)  # 0-100
    estado = Column(String(20), default='CURSANDO')  # CURSANDO, APROBADA, REPROBADA
    fecha_inscripcion = Column(Date, default=date.today)
    
    # Relaciones
    estudiante = relationship("Estudiante", back_populates="inscripciones")
    seccion = relationship("Seccion", back_populates="inscripciones")


# ALERTAS Y NOTIFICACIONES 

class Alerta(Base):
    """Alerta que un estudiante activa para una sección"""
    __tablename__ = 'alertas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha_activacion = Column(DateTime, default=datetime.utcnow)
    activa = Column(Boolean, default=True)
    
    estudiante_id = Column(Integer, ForeignKey('estudiantes.usuario_id'), nullable=False)
    seccion_id = Column(Integer, ForeignKey('secciones.id'), nullable=False)
    
    estudiante = relationship("Estudiante", back_populates="alertas")
    seccion = relationship("Seccion", back_populates="alertas")
    notificacion = relationship("Notificacion", back_populates="alerta", uselist=False)


class Notificacion(Base):
    """Notificación enviada cuando se libera un cupo"""
    __tablename__ = 'notificaciones'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    mensaje = Column(Text, nullable=False)
    fecha_envio = Column(DateTime, default=datetime.utcnow)
    leida = Column(Boolean, default=False)
    
    alerta_id = Column(Integer, ForeignKey('alertas.id'), nullable=False)
    estudiante_id = Column(Integer, ForeignKey('estudiantes.usuario_id'), nullable=False)
    seccion_id = Column(Integer, ForeignKey('secciones.id'), nullable=False)
    
    alerta = relationship("Alerta", back_populates="notificacion")
    estudiante = relationship("Estudiante", back_populates="notificaciones")
    seccion = relationship("Seccion", back_populates="notificaciones")


# CLASE DE GESTIÓN (CRUD + KARDEX) 

class GestionBD:
    """Clase auxiliar para todas las operaciones de base de datos"""
    
    @staticmethod
    def get_session():
        return SessionLocal()
    
    #  USUARIOS 
    
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
    
    @staticmethod
    def obtener_usuario_por_id(id):
        session = SessionLocal()
        try:
            return session.query(Usuario).filter(Usuario.id == id).first()
        finally:
            session.close()
    
    # ESTUDIANTES 
    
    @staticmethod
    def crear_estudiante(usuario_data, estudiante_data):
        session = SessionLocal()
        try:
            usuario = Usuario(**usuario_data)
            session.add(usuario)
            session.flush()
            
            estudiante = Estudiante(usuario_id=usuario.id, **estudiante_data)
            session.add(estudiante)
            session.commit()
            return estudiante
        finally:
            session.close()
    
    @staticmethod
    def obtener_estudiante_por_matricula(matricula):
        session = SessionLocal()
        try:
            return session.query(Estudiante).filter(Estudiante.matricula == matricula).first()
        finally:
            session.close()
    
    @staticmethod
    def obtener_estudiante_por_id(estudiante_id):
        session = SessionLocal()
        try:
            return session.query(Estudiante).filter(Estudiante.usuario_id == estudiante_id).first()
        finally:
            session.close()
    
    #  MATERIAS 
    
    @staticmethod
    def crear_materia(data):
        session = SessionLocal()
        try:
            materia = Materia(**data)
            session.add(materia)
            session.commit()
            return materia
        finally:
            session.close()
    
    @staticmethod
    def obtener_materias():
        session = SessionLocal()
        try:
            return session.query(Materia).all()
        finally:
            session.close()
    
    @staticmethod
    def obtener_materia_por_id(id):
        session = SessionLocal()
        try:
            return session.query(Materia).filter(Materia.id == id).first()
        finally:
            session.close()
    
    # SECCIONES 
    
    @staticmethod
    def crear_seccion(data):
        session = SessionLocal()
        try:
            seccion = Seccion(**data)
            session.add(seccion)
            session.commit()
            return seccion
        finally:
            session.close()
    
    @staticmethod
    def obtener_secciones_disponibles():
        session = SessionLocal()
        try:
            return session.query(Seccion).filter(Seccion.cupos_disponibles > 0).all()
        finally:
            session.close()
    
    @staticmethod
    def obtener_secciones_por_materia(materia_id):
        session = SessionLocal()
        try:
            return session.query(Seccion).filter(Seccion.materia_id == materia_id).all()
        finally:
            session.close()
    
    # ========== INSCRIPCIONES (KARDEX) ==========
    
    @staticmethod
    def inscribir_estudiante(estudiante_id, seccion_id, periodo):
        """Inscribe a un estudiante en una sección"""
        session = SessionLocal()
        try:
            # Verificar si ya está inscrito
            existe = session.query(Inscripcion).filter(
                Inscripcion.estudiante_id == estudiante_id,
                Inscripcion.seccion_id == seccion_id,
                Inscripcion.estado.in_(['CURSANDO', 'APROBADA'])
            ).first()
            
            if existe:
                return None, "Ya está inscrito en esta sección"
            
            # Verificar cupo disponible
            seccion = session.query(Seccion).filter(Seccion.id == seccion_id).first()
            if not seccion or seccion.cupos_disponibles <= 0:
                return None, "No hay cupos disponibles"
            
            # Crear inscripción
            inscripcion = Inscripcion(
                estudiante_id=estudiante_id,
                seccion_id=seccion_id,
                periodo=periodo
            )
            session.add(inscripcion)
            
            # Reducir cupo
            seccion.cupos_disponibles -= 1
            session.commit()
            
            return inscripcion, "Inscripción exitosa"
        finally:
            session.close()
    
    @staticmethod
    def obtener_kardex(estudiante_id):
        """Obtiene todo el historial académico de un estudiante"""
        session = SessionLocal()
        try:
            resultados = session.query(
                Inscripcion,
                Materia,
                Seccion
            ).join(Seccion, Inscripcion.seccion_id == Seccion.id
            ).join(Materia, Seccion.materia_id == Materia.id
            ).filter(Inscripcion.estudiante_id == estudiante_id
            ).order_by(Inscripcion.periodo.desc()).all()
            
            kardex = []
            for inscripcion, materia, seccion in resultados:
                kardex.append({
                    "id": inscripcion.id,
                    "materia_id": materia.id,
                    "materia_nombre": materia.nombre,
                    "materia_codigo": materia.codigo,
                    "creditos": materia.creditos,
                    "periodo": inscripcion.periodo,
                    "calificacion": inscripcion.calificacion,
                    "estado": inscripcion.estado,
                    "horario": f"{seccion.dias} {seccion.hora_inicio.strftime('%H:%M')}-{seccion.hora_fin.strftime('%H:%M')}",
                    "fecha_inscripcion": inscripcion.fecha_inscripcion
                })
            return kardex
        finally:
            session.close()
    
    @staticmethod
    def obtener_materias_cursadas(estudiante_id):
        """Obtiene solo las materias ya cursadas (aprobadas o reprobadas)"""
        session = SessionLocal()
        try:
            resultados = session.query(
                Inscripcion,
                Materia
            ).join(Seccion, Inscripcion.seccion_id == Seccion.id
            ).join(Materia, Seccion.materia_id == Materia.id
            ).filter(
                Inscripcion.estudiante_id == estudiante_id,
                Inscripcion.estado.in_(['APROBADA', 'REPROBADA'])
            ).all()
            
            materias = []
            for inscripcion, materia in resultados:
                materias.append({
                    "id": inscripcion.id,
                    "materia_nombre": materia.nombre,
                    "materia_codigo": materia.codigo,
                    "creditos": materia.creditos,
                    "periodo": inscripcion.periodo,
                    "calificacion": inscripcion.calificacion,
                    "estado": inscripcion.estado
                })
            return materias
        finally:
            session.close()
    
    @staticmethod
    def obtener_materias_actuales(estudiante_id):
        """Obtiene las materias que el estudiante está cursando actualmente"""
        session = SessionLocal()
        try:
            resultados = session.query(
                Inscripcion,
                Materia,
                Seccion
            ).join(Seccion, Inscripcion.seccion_id == Seccion.id
            ).join(Materia, Seccion.materia_id == Materia.id
            ).filter(
                Inscripcion.estudiante_id == estudiante_id,
                Inscripcion.estado == 'CURSANDO'
            ).all()
            
            materias = []
            for inscripcion, materia, seccion in resultados:
                materias.append({
                    "id": inscripcion.id,
                    "materia_nombre": materia.nombre,
                    "materia_codigo": materia.codigo,
                    "creditos": materia.creditos,
                    "horario": f"{seccion.dias} {seccion.hora_inicio.strftime('%H:%M')}-{seccion.hora_fin.strftime('%H:%M')}",
                    "aula": seccion.aula_id
                })
            return materias
        finally:
            session.close()
    
    @staticmethod
    def registrar_calificacion(inscripcion_id, calificacion):
        """Registra calificación para una inscripción específica"""
        session = SessionLocal()
        try:
            inscripcion = session.query(Inscripcion).filter(Inscripcion.id == inscripcion_id).first()
            
            if not inscripcion:
                return None, "Inscripción no encontrada"
            
            inscripcion.calificacion = calificacion
            inscripcion.estado = "APROBADA" if calificacion >= 60 else "REPROBADA"
            session.commit()
            
            # Actualizar promedio y créditos del estudiante
            GestionBD.actualizar_promedio_estudiante(inscripcion.estudiante_id)
            
            return inscripcion, "Calificación registrada"
        finally:
            session.close()
    
    @staticmethod
    def actualizar_promedio_estudiante(estudiante_id):
        """Calcula y actualiza el promedio general y créditos totales del estudiante"""
        session = SessionLocal()
        try:
            # Obtener todas las inscripciones aprobadas
            inscripciones = session.query(Inscripcion).join(
                Seccion, Inscripcion.seccion_id == Seccion.id
            ).join(
                Materia, Seccion.materia_id == Materia.id
            ).filter(
                Inscripcion.estudiante_id == estudiante_id,
                Inscripcion.estado == 'APROBADA'
            ).all()
            
            if not inscripciones:
                return
            
            total_creditos = 0
            suma_ponderada = 0
            
            for inscripcion in inscripciones:
                materia = inscripcion.seccion.materia
                total_creditos += materia.creditos
                suma_ponderada += inscripcion.calificacion * materia.creditos
            
            promedio = suma_ponderada / total_creditos if total_creditos > 0 else 0
            
            # Actualizar estudiante
            estudiante = session.query(Estudiante).filter(Estudiante.usuario_id == estudiante_id).first()
            if estudiante:
                estudiante.creditos_totales = total_creditos
                estudiante.promedio_general = round(promedio, 2)
                session.commit()
        finally:
            session.close()
    
    @staticmethod
    def obtener_promedio_estudiante(estudiante_id):
        """Devuelve el promedio general del estudiante"""
        session = SessionLocal()
        try:
            estudiante = session.query(Estudiante).filter(Estudiante.usuario_id == estudiante_id).first()
            return estudiante.promedio_general if estudiante else 0.0
        finally:
            session.close()
    
    @staticmethod
    def obtener_creditos_obtenidos(estudiante_id):
        """Devuelve los créditos totales obtenidos por el estudiante"""
        session = SessionLocal()
        try:
            estudiante = session.query(Estudiante).filter(Estudiante.usuario_id == estudiante_id).first()
            return estudiante.creditos_totales if estudiante else 0
        finally:
            session.close()
    
    @staticmethod
    def obtener_resumen_kardex(estudiante_id):
        """Obtiene un resumen completo del kardex (promedio, créditos, materias cursadas)"""
        session = SessionLocal()
        try:
            kardex = GestionBD.obtener_kardex(estudiante_id)
            materias_cursadas = [m for m in kardex if m['estado'] != 'CURSANDO']
            materias_actuales = [m for m in kardex if m['estado'] == 'CURSANDO']
            aprobadas = [m for m in materias_cursadas if m['estado'] == 'APROBADA']
            reprobadas = [m for m in materias_cursadas if m['estado'] == 'REPROBADA']
            
            return {
                "promedio": GestionBD.obtener_promedio_estudiante(estudiante_id),
                "creditos_totales": GestionBD.obtener_creditos_obtenidos(estudiante_id),
                "materias_cursadas": len(materias_cursadas),
                "materias_actuales": len(materias_actuales),
                "aprobadas": len(aprobadas),
                "reprobadas": len(reprobadas),
                "detalle_kardex": kardex,
                "materias_actuales_detalle": materias_actuales
            }
        finally:
            session.close()
    
    #  ALERTAS 
    
    @staticmethod
    def activar_alerta(estudiante_id, seccion_id):
        session = SessionLocal()
        try:
            # Verificar si ya tiene alerta activa para esta sección
            existe = session.query(Alerta).filter(
                Alerta.estudiante_id == estudiante_id,
                Alerta.seccion_id == seccion_id,
                Alerta.activa == True
            ).first()
            
            if existe:
                return None, "Ya tienes una alerta activa para esta sección"
            
            alerta = Alerta(estudiante_id=estudiante_id, seccion_id=seccion_id)
            session.add(alerta)
            session.commit()
            return alerta, "Alerta activada"
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
    
    @staticmethod
    def desactivar_alerta(alerta_id):
        session = SessionLocal()
        try:
            alerta = session.query(Alerta).filter(Alerta.id == alerta_id).first()
            if alerta:
                alerta.activa = False
                session.commit()
                return True
            return False
        finally:
            session.close()


#  INICIALIZACIÓN 

def inicializar_bd():
    """Crea todas las tablas si no existen"""
    Base.metadata.create_all(bind=engine)
    print("✅ Base de datos SIGHA inicializada correctamente")
    print("📁 Archivo: sigha.db")
    print("\n📋 Tablas creadas:")
    for table in Base.metadata.tables.keys():
        print(f"   - {table}")


if __name__ == "__main__":
    inicializar_bd()
 





