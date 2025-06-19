import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect('base.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS asistencias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente TEXT,
    direccion TEXT,
    problema TEXT,
    tipo TEXT,
    prioridad TEXT,
    estado TEXT,
    tecnico TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    usuario TEXT PRIMARY KEY,
    contraseña TEXT,
    rol TEXT,
    nombre TEXT
)
''')

cursor.execute("INSERT OR REPLACE INTO usuarios VALUES (?, ?, ?, ?)", (
    'admin', generate_password_hash('admin123'), 'admin', 'Administrador'
))
cursor.execute("INSERT OR REPLACE INTO usuarios VALUES (?, ?, ?, ?)", (
    'tecnico1', generate_password_hash('tecnico123'), 'tecnico', 'Cristhian Alcaraz'
))
cursor.execute("INSERT OR REPLACE INTO usuarios VALUES (?, ?, ?, ?)", (
    'tecnico2', generate_password_hash('clave456'), 'tecnico', 'Richard Leckie'
))
cursor.execute("INSERT OR REPLACE INTO usuarios VALUES (?, ?, ?, ?)", (
    'tecnico3', generate_password_hash('clave789'), 'tecnico', 'Robert Leckie'
))
cursor.execute("INSERT OR REPLACE INTO usuarios VALUES (?, ?, ?, ?)", (
    'tecnico4', generate_password_hash('clave321'), 'tecnico', 'Néstor Villalba'
))
cursor.execute("INSERT OR REPLACE INTO usuarios VALUES (?, ?, ?, ?)", (
    'tecnico5', generate_password_hash('clave654'), 'tecnico', 'Otro Técnico'
))

conn.commit()
conn.close()
print("Base de datos creada con éxito")