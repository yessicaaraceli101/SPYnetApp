import sqlite3
from werkzeug.security import check_password_hash

def validar_usuario(usuario, contraseña):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute("SELECT contraseña, rol FROM usuarios WHERE usuario = ?", (usuario,))
    row = cursor.fetchone()
    conn.close()
    if row and check_password_hash(row[0], contraseña):
        return True, row[1]
    return False, None