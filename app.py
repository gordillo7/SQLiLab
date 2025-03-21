from flask import Flask, request, jsonify, session, redirect, url_for, render_template, flash
from setupOracle import dbConectarOracle, configuracionTablas_oracle, login_inseguro_blind_oracle, dbDesconectar
from setupPostgreSQL import dbConectarPostgreSQL, configuracion_tablas_postgresql, login_inseguro_blind_postgresql
import os
import webbrowser
import dynamic_html
import diccionarioInyecciones

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secreto para sesiones seguras

# Ruta para la página de índice del laboratorio
@app.route('/index')
def index():
    return render_template('index.html', sql_injections=diccionarioInyecciones.sql_injections)

# Rutas dinámicas para inicio de sesión de SQL Injection en Oracle y PostgreSQL
@app.route('/login/oracle/<tipo_sqli>', methods=['GET', 'POST'])
def login_oracle(tipo_sqli):
    return login_sqli(tipo_sqli, database="Oracle")

@app.route('/login/postgres/<tipo_sqli>', methods=['GET', 'POST'])
def login_postgres(tipo_sqli):
    return login_sqli(tipo_sqli, database="Postgres")

@app.route('/cookie', methods=['POST'])
def cookie_login():
    cookie_value = request.get_json().get('cookie_value') if request.is_json else request.form.get('cookie_value')
    tipo_sqli = request.get_json().get('tipo_sqli') if request.is_json else request.form.get('tipo_sqli')
    database = request.get_json().get('database') if request.is_json else request.form.get('database')

    if not cookie_value:
        flash("No se proporcionó ninguna cookie.", "error")
        return redirect(url_for('login_sqli', tipo_sqli=tipo_sqli, database=database))

    sqli_info = diccionarioInyecciones.sql_injections.get(tipo_sqli)
    if not sqli_info:
        flash("Tipo de SQL Injection no encontrado.", "error")
        return redirect(url_for('login_sqli', tipo_sqli=tipo_sqli, database=database))

    auth_function = None
    if database == "Oracle":
        auth_function = login_inseguro_blind_oracle
    elif database == "Postgres":
        auth_function = login_inseguro_blind_postgresql

    if not auth_function:
        flash("Función de autenticación no encontrada.", "error")
        return redirect(url_for('login_sqli', tipo_sqli=tipo_sqli, database=database))

    if tipo_sqli in ['blind_boolean', 'time_based']:
        result = auth_function(cookie_value)
    else:
        result = None

    if result and result.get('auth') == "true":
        usuario = result['resultado'][1] if isinstance(result['resultado'], tuple) and len(result['resultado']) > 1 else "Usuario"
        session['username'] = usuario
        print("Redirection to /welcome triggered")  # Add this line for logging
        return redirect(url_for('welcome'))
    else:
        return redirect(url_for(f'login_{database.lower()}', tipo_sqli=tipo_sqli, database=database))

@app.route('/welcome')
def welcome():
    username = session.get('username')
    if not username:
        flash("Debes iniciar sesión primero.", "error")
        return redirect(url_for('login_sqli', tipo_sqli=session.get('tipo_sqli'), database=session.get('database')))
    return render_template('welcome.html', username=username)

def login_sqli(tipo_sqli, database):
    sqli_info = diccionarioInyecciones.sql_injections.get(tipo_sqli)
    if not sqli_info:
        return "Tipo de SQL Injection no encontrado.", 404

    is_blind = tipo_sqli in ['time_based', 'blind_boolean']

    auth_function_blind = None
    if database == "Oracle":
        auth_function_blind = login_inseguro_blind_oracle
    elif database == "Postgres":
        auth_function_blind = login_inseguro_blind_postgresql

    auth_function = sqli_info.get("function_oracle") if database == "Oracle" else sqli_info.get("function_postgres")

    if request.method == 'POST':
        cookie_value = request.get_json().get('cookie_value') if request.is_json else request.form.get('cookie_value')

        if is_blind and cookie_value:
            result = auth_function_blind(cookie_value)
        else:
            username = request.get_json().get('username') if request.is_json else request.form.get('username')
            password = request.get_json().get('password') if request.is_json else request.form.get('password')
            result = auth_function(username, password)

        if result:
            cardSentencia = dynamic_html.generarTarjetaInformacion("Sentencia SQL", result.get('sentencia', ''))
            flash(cardSentencia, category='Sentencia')

            if 'resultado' in result:
                if result.get('auth') == "true":
                    flash("Bienvenido, sesión iniciada con éxito", category='welcome')
                flash(str(result['resultado']), category='Resultado')
            else:
                flash("Usuario o contraseña incorrectos", category='error')
                flash("Operación realizada con éxito", "success")
        else:
            flash("Error en la operación", "error")
            return redirect(url_for(f'login_{database.lower()}', tipo_sqli=tipo_sqli))

    session['tipo_sqli'] = tipo_sqli
    session['database'] = database

    return render_template(
        'login.html',
        title=sqli_info.get("title", ""),
        description=sqli_info.get("description", ""),
        dificultad=sqli_info.get("dificultad", ""),
        impacto=sqli_info.get("impacto", ""),
        database=database,
        tipo_sqli=tipo_sqli,
        credenciales=sqli_info.get("credenciales", {}),
        is_blind=is_blind
    )

# Ruta protegida de ejemplo
@app.route('/home')
def home():
    if 'user' in session:
        return jsonify({"message": f"Bienvenido, {session['user']}"})
    return redirect(url_for('login_oracle', tipo_sqli="database_error"))

def initialize_databaseOracle():
    conexionOracle = dbConectarOracle()
    if conexionOracle:
        configuracionTablas_oracle(conexionOracle)
        dbDesconectar(conexionOracle)
    else:
        print("Error al conectar con la base de datos Oracle")

def initialize_databasePostgreSQL():
    conexionPostgreSQL = dbConectarPostgreSQL()
    if conexionPostgreSQL:
        configuracion_tablas_postgresql(conexionPostgreSQL)
        dbDesconectar(conexionPostgreSQL)
    else:
        print("Error al conectar con la base de datos PostgreSQL")

if __name__ == '__main__':
    initialize_databaseOracle()
    initialize_databasePostgreSQL()
    webbrowser.open("http://127.0.0.1:5000/index")
    app.run(debug=False)
