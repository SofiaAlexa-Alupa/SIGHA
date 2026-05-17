import sqlite3

# Conectar directamente a la base de datos (sin SQLAlchemy)
conn = sqlite3.connect('sigha.db')
cursor = conn.cursor()

# Ver cuántas fechas tienen formato con barras
cursor.execute("SELECT id, nombre, fecha_creacion FROM usuarios WHERE fecha_creacion LIKE '%/%'")
rows = cursor.fetchall()
print(f"📅 Se encontraron {len(rows)} fechas con formato de barras:")

for row in rows:
    print(f"   ID: {row[0]}, Nombre: {row[1]}, Fecha original: {row[2]}")

# Actualizar las fechas: reemplazar '/' por '-'
cursor.execute("UPDATE usuarios SET fecha_creacion = REPLACE(fecha_creacion, '/', '-') WHERE fecha_creacion LIKE '%/%'")
conn.commit()

print(f"\n✅ Corregidas {cursor.rowcount} fechas")

# Verificar el resultado
cursor.execute("SELECT id, nombre, fecha_creacion FROM usuarios LIMIT 5")
print("\n📋 Ejemplo de fechas corregidas:")
for row in cursor.fetchall():
    print(f"   {row[0]} - {row[1]}: {row[2]}")

conn.close()
