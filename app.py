from flask import Flask, request, jsonify, session
from database import GestionBD, Usuario, Materia, Aula, Seccion, Inscripcion
from datetime import date
import bcrypt

app = Flask(__name__)
app.secret_key = "clave_secreta"


# ================= UTIL =================

def get_db():
    return GestionBD.get_session()


# ================= AUTH =================

@app.route("/register", methods=["POST"])
def register():
    db = get_db()
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON"}), 400

        if GestionBD.obtener_usuario_por_email(data["email"]):
            return jsonify({"error": "Usuario existe"}), 400

        nuevo = {
            "identificacion": data["identificacion"],
            "nombre": data["nombre"],
            "apellido_paterno": data["apellido_paterno"],
            "apellido_materno": data["apellido_materno"],
            "email": data["email"],
            "password": data["password"],
            "rol": data.get("rol", "estudiante"),
            "fecha_creacion": date.today()
        }

        user_id = GestionBD.crear_usuario(nuevo)
        return jsonify({"msg": "Usuario creado", "id": user_id}), 201

    finally:
        db.close()


@app.route("/login", methods=["POST"])
def login():
    db = get_db()
    try:
        data = request.get_json()

        user = GestionBD.login(data["email"], data["password"])

        if not user:
            return jsonify({"error": "Credenciales incorrectas"}), 401

        session["user_id"] = user.id
        session["rol"] = user.rol

        return jsonify({"msg": "Login exitoso", "rol": user.rol})

    finally:
        db.close()


@app.route("/logout")
def logout():
    session.clear()
    return jsonify({"msg": "Sesion cerrada"})


# ================= USUARIOS =================

@app.route("/usuarios", methods=["GET"])
def get_usuarios():
    db = get_db()
    try:
        usuarios = db.query(Usuario).all()

        return jsonify([
            {
                "id": u.id,
                "identificacion": u.identificacion,
                "nombre": u.nombre,
                "apellido_paterno": u.apellido_paterno,
                "email": u.email,
                "rol": u.rol
            }
            for u in usuarios
        ])

    finally:
        db.close()


# ================= PERFIL =================

@app.route("/perfil")
def perfil():
    db = get_db()
    try:
        if "user_id" not in session:
            return jsonify({"error": "No login"}), 401

        user = db.query(Usuario).get(session["user_id"])

        return jsonify({
            "id": user.id,
            "nombre": user.nombre,
            "apellido_paterno": user.apellido_paterno,
            "apellido_materno": user.apellido_materno,
            "email": user.email,
            "rol": user.rol
        })

    finally:
        db.close()


# ================= MATERIAS =================

@app.route("/materias", methods=["POST"])
def crear_materia():
    db = get_db()
    try:
        if session.get("rol") != "admin":
            return jsonify({"error": "Solo admin"}), 403

        data = request.get_json()

        m = Materia(
            codigo=data["codigo"],
            nombre=data["nombre"],
            creditos=data.get("creditos", 0),
            facultad=data.get("facultad", "General")
        )

        db.add(m)
        db.commit()

        return jsonify({"msg": "Materia creada"})

    finally:
        db.close()


@app.route("/materias", methods=["GET"])
def ver_materias():
    db = get_db()
    try:
        materias = db.query(Materia).all()

        return jsonify([
            {
                "id": m.id,
                "codigo": m.codigo,
                "nombre": m.nombre,
                "creditos": m.creditos,
                "facultad": m.facultad
            }
            for m in materias
        ])

    finally:
        db.close()


@app.route("/materias/<int:id>", methods=["DELETE"])
def eliminar_materia(id):
    db = get_db()
    try:
        if session.get("rol") != "admin":
            return jsonify({"error": "Solo admin"}), 403

        materia = db.query(Materia).get(id)

        if not materia:
            return jsonify({"error": "No existe"}), 404

        db.delete(materia)
        db.commit()

        return jsonify({"msg": "Materia eliminada"})

    finally:
        db.close()


# ================= MAESTROS =================

@app.route("/maestros", methods=["POST"])
def crear_maestro():
    db = get_db()
    try:
        if session.get("rol") != "admin":
            return jsonify({"error": "Solo admin"}), 403

        data = request.get_json()

        hashed = bcrypt.hashpw(
            data["password"].encode("utf-8"),
            bcrypt.gensalt()
        )

        maestro = Usuario(
            nrc=data["nrc"],
            nombre=data["nombre"],
            apellido_paterno=data["apellido_paterno"],
            apellido_materno=data["apellido_materno"],
            email=data["email"],
            password=hashed.decode("utf-8"),
            rol="maestro",
            fecha_creacion=date.today()
        )

        db.add(maestro)
        db.commit()
        db.refresh(maestro)

        return jsonify({"msg": "Maestro creado", "id": maestro.id})

    finally:
        db.close()


@app.route("/maestros", methods=["GET"])
def ver_maestros():
    db = get_db()
    try:
        maestros = db.query(Usuario).filter(Usuario.rol == "maestro").all()

        return jsonify([
            {
                "id": m.id,
                "nrc": m.nrc,
                "nombre": m.nombre,
                "apellido_paterno": m.apellido_paterno,
                "email": m.email
            }
            for m in maestros
        ])

    finally:
        db.close()


@app.route("/maestros/<int:id>", methods=["DELETE"])
def eliminar_maestro(id):
    db = get_db()
    try:
        if session.get("rol") != "admin":
            return jsonify({"error": "Solo admin"}), 403

        m = db.query(Usuario).get(id)

        if not m or m.rol != "maestro":
            return jsonify({"error": "No valido"}), 404

        db.delete(m)
        db.commit()

        return jsonify({"msg": "Maestro eliminado"})

    finally:
        db.close()


# ================= AULAS =================

@app.route("/aulas", methods=["POST"])
def crear_aula():
    db = get_db()
    try:
        data = request.get_json()

        a = Aula(
            nombre=data["nombre"],
            capacidad=data.get("capacidad", 0),
            recursos=data.get("recursos", "Ninguno"),
            edificio=data["edificio"],
            claves=data.get("claves")
        )

        db.add(a)
        db.commit()

        return jsonify({"msg": "Aula creada"})

    finally:
        db.close()


@app.route("/aulas", methods=["GET"])
def ver_aulas():
    db = get_db()
    try:
        aulas = db.query(Aula).all()

        return jsonify([
            {
                "id": a.id,
                "nombre": a.nombre,
                "capacidad": a.capacidad,
                "edificio": a.edificio,
                "claves": a.claves
            }
            for a in aulas
        ])

    finally:
        db.close()


@app.route("/aulas/<int:id>", methods=["DELETE"])
def eliminar_aula(id):
    db = get_db()
    try:
        aula = db.query(Aula).get(id)

        if not aula:
            return jsonify({"error": "No existe"}), 404

        db.delete(aula)
        db.commit()

        return jsonify({"msg": "Aula eliminada"})

    finally:
        db.close()


# ================= SECCIONES =================

@app.route("/secciones", methods=["POST"])
def crear_seccion():
    db = get_db()
    try:
        s = Seccion(**request.get_json())
        db.add(s)
        db.commit()

        return jsonify({"msg": "Seccion creada"})

    finally:
        db.close()


@app.route("/secciones", methods=["GET"])
def ver_secciones():
    db = get_db()
    try:
        secciones = db.query(Seccion).all()

        return jsonify([
            {
                "id": s.id,
                "materia_id": s.materia_id,
                "maestro_id": s.maestro_id,
                "dias": s.dias,
                "hora_inicio": str(s.hora_inicio),
                "hora_fin": str(s.hora_fin),
                "cupos_disponibles": s.cupos_disponibles
            }
            for s in secciones
        ])

    finally:
        db.close()


@app.route("/secciones/<int:id>", methods=["DELETE"])
def eliminar_seccion(id):
    db = get_db()
    try:
        s = db.query(Seccion).get(id)

        if not s:
            return jsonify({"error": "No existe"}), 404

        db.delete(s)
        db.commit()

        return jsonify({"msg": "Seccion eliminada"})

    finally:
        db.close()


# ================= MAIN =================

if __name__ == "__main__":
    app.run(debug=True)