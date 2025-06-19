from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from werkzeug.security import check_password_hash
from auth import validar_usuario

app = Flask(__name__)
app.secret_key = 'clave_secreta_yessica'

def get_db():
    return sqlite3.connect('base.db')

@app.route('/')
def inicio():
    if 'usuario' not in session:
        return redirect('/login')
    return render_template('inicio.html', usuario=session['usuario'])

@app.route('/nueva_asistencia', methods=['GET', 'POST'])
def nueva_asistencia():
    if 'usuario' not in session or session['rol'] != 'admin':
        return redirect('/login')

    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        cliente = request.form['cliente']
        direccion = request.form['direccion']
        tipo = request.form['tipo']
        prioridad = request.form['prioridad']
        problema = request.form['problema']
        tecnico = request.form['tecnico']

        cursor.execute("""
            INSERT INTO asistencias (cliente, direccion, problema, tipo, prioridad, estado, tecnico)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (cliente, direccion, problema, tipo, prioridad, 'Pendiente', tecnico)
        )
        conn.commit()
        conn.close()
        return redirect('/asistencias')

    # ACÁ SE TRAEN LOS TÉCNICOS
    cursor.execute("SELECT usuario FROM usuarios WHERE rol = 'tecnico'")
    tecnicos = cursor.fetchall()
    conn.close()

    # LOS PASAMOS A LA PLANTILLA
    return render_template('nueva_asistencia.html', tecnicos=tecnicos)


@app.route('/asistencias')
def asistencias():
    if 'usuario' not in session:
        return redirect('/login')
    conn = get_db()
    cursor = conn.cursor()
    if session['rol'] == 'tecnico':
        cursor.execute("SELECT * FROM asistencias WHERE tecnico = ?", (session['usuario'],))
    else:
        cursor.execute("SELECT * FROM asistencias")
    data = cursor.fetchall()
    conn.close()
    return render_template('lista_asistencias.html', asistencias=data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        valido, rol = validar_usuario(usuario, contraseña)
        if valido:
            session['usuario'] = usuario
            session['rol'] = rol
            return redirect('/')
        return "Credenciales inválidas"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/')
def formulario():
    tecnicos = [
        (1, "Cristhian Alcaraz"),
        (2, "Richard Leckie"),
        (3, "Robert Leckie"),
        (4, "Néstor Villalba"),
        (5, "Otro Técnico")
    ]
    return render_template('formulario.html', tecnicos=tecnicos)

if __name__ == '__main__':
    app.run(debug=True)