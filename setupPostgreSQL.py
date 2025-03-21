import psycopg2 as PBD

def dbConectarPostgreSQL():
    ip = "localhost"
    puerto = 5432
    basedatos = "Empresa"

    usuario = "postgres"
    contrasena = "12345"

    print("---dbConectarPostgreSQL---")
    print("---Conectando a Postgresql---")

    try:
        conexion = PBD.connect(user=usuario, password=contrasena, host=ip, port=puerto, database=basedatos)
        print("Conexión realizada a la base de datos",conexion)
        return conexion
    except PBD.DatabaseError as error:
        print("Error en la conexión")
        print(error)
        return None

#-------------------------------------------------------------------

def dbDesconectar(conexion):
    print("---dbDesconectar---")
    try:
        conexion.commit()  # Confirma los cambios
        conexion.close()
        print("Desconexión realizada correctamente")
        return True
    except PBD.DatabaseError as error:
        print("Error en la desconexión")
        print(error)
        return False

#-------------------------------------------------------------------

def configuracion_tablas_postgresql(conexion):
    print("---configuracion_tablas_postgresql---")
    try:
        cursor = conexion.cursor()

        # Crear la tabla Usuarios si no existe con columna session_cookie
        consulta = """
            CREATE TABLE IF NOT EXISTS Usuarios (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                password VARCHAR(50) NOT NULL,
                session_cookie VARCHAR(255)
            );
        """
        cursor.execute(consulta)

        # Insertar usuarios de ejemplo solo si la tabla está vacía
        cursor.execute("SELECT COUNT(*) FROM Usuarios")
        count = cursor.fetchone()[0]
        if count == 0:
            usuarios_ejemplo = [
                ("admin", "password123", "t4SpnpWyg76A3K2BqcFh2vODq0fqJGvs38ydh9"),
                ("user1", "password1", "d382yd8n21df4314fn817yf6834188ls023d8d"),
                ("user2", "password2", "u73dv226d726gh23fnjncuyg0q9udfjf47eueu")
            ]
            cursor.executemany(
                "INSERT INTO Usuarios (username, password, session_cookie) VALUES (%s, %s, %s)",
                usuarios_ejemplo
            )
            print("Usuarios de ejemplo insertados correctamente.")
        else:
            print("La tabla Usuarios ya contiene datos.")

        cursor.close()
        print("Tabla 'Usuarios' creada o verificada exitosamente en PostgreSQL")
        return True
    except PBD.DatabaseError as error:
        print("Error al crear la tabla o insertar usuarios en PostgreSQL")
        print(error)
        return False


#-------------------------------------------------------------------

def login_seguro_postgresql(username, password):
    print("---login---")
    conexion = dbConectarPostgreSQL()  # Abre la conexión para autenticación
    if not conexion:
        print("Error: no se pudo conectar para autenticar.")
        return False

    try:
        cursor = conexion.cursor()
        consulta = "SELECT * FROM Usuarios WHERE username = %s AND password = %s"
        cursor.execute(consulta, [username, password])
        usuario = cursor.fetchone()
        cursor.close()
        dbDesconectar(conexion)  # Cierra la conexión después de la autenticación
        if usuario:
            print("Usuario autenticado:", usuario)
            return True
        else:
            print("Usuario o contraseña incorrectos")
            return False
    except PBD.DatabaseError as error:
        print("Error al autenticar usuario")
        print(error)
        dbDesconectar(conexion)
        return False

#-------------------------------------------------------------------

# Función de autenticación insegura simple
def login_inseguro_base_postgresql(username, password):
    print("---login---")
    conexion = dbConectarPostgreSQL()  # Abre la conexión para autenticación
    if not conexion:
        print("Error: no se pudo conectar para autenticar.")
        return False

    try:
        cursor = conexion.cursor()
        sentencia =   "SELECT * FROM Usuarios WHERE username = '"+username+"' AND password = '"+password+"'"
        cursor.execute(sentencia)
        usuario = cursor.fetchall()
        cursor.close()
        if usuario:
            print("Usuario autenticado:", usuario)
            return {"resultado":usuario, "sentencia":sentencia, "auth": "true"}
        else:
            print("Usuario o contraseña incorrectos")
            return {"sentencia":sentencia}
        #dbDesconectar(conexion)  # Cierra la conexión después de la autenticación
    except PBD.DatabaseError as error:
        print("Error al autenticar usuario")
        print(error)
        dbDesconectar(conexion)
        return {"resultado":error, "sentencia":sentencia}

#-------------------------------------------------------------------

# Login inseguro para blind con username y password
def login_inseguro_blind_no_cookie_postgresql(username, password):
    print("---login---")
    print("login_inseguro_blind sin cookie")
    conexion = dbConectarPostgreSQL()  # Abre la conexión para autenticación
    if not conexion:
        print("Error: no se pudo conectar para autenticar.")
        return False

    sentencia =   "SELECT * FROM Usuarios WHERE username = '"+username+"' AND password = '"+password+"'"
    try:
        cursor = conexion.cursor()
        cursor.execute(sentencia)
        usuario = cursor.fetchone()
        cursor.close()
        #dbDesconectar(conexion)  # Cierra la conexión después de la autenticación
        if usuario:
            print("Usuario autenticado:", usuario)
            return {"resultado":usuario,"sentencia":sentencia, "auth": "true"}
        else:
            print("Usuario o contraseña incorrectos")
            return {"sentencia":sentencia}
    except PBD.DatabaseError as error:
        print("Error al autenticar usuario")
        print(error)
        dbDesconectar(conexion)
        return {"sentencia":sentencia}


# Login inseguro para errores
def login_inseguro_errors_postgresql(username, password):
    print("---login---")
    print ("---login_inseguro_errors---")
    conexion = dbConectarPostgreSQL()  # Abre la conexión para autenticación
    if not conexion:
        print("Error: no se pudo conectar para autenticar.")
        return False

    sentencia =   "SELECT * FROM Usuarios WHERE username = '"+username+"' AND password = '"+password+"'"
    try:
        cursor = conexion.cursor()
        cursor.execute(sentencia)
        usuario = cursor.fetchone()

        cursor.close()
        dbDesconectar(conexion)  # Cierra la conexión después de la autenticación
        if usuario:
            if isinstance(usuario, tuple) and len(usuario) == 3:
                return {"resultado": usuario, "sentencia": sentencia, "auth": "true"}
            else:
                print("Usuario autenticado:", usuario)
                return {"resultado": usuario, "sentencia": sentencia}
        else:
            print("Usuario o contraseña incorrectos")
            return {"sentencia": sentencia}
    except PBD.DatabaseError as error:
        print("Error al autenticar usuario")
        print(error)
        dbDesconectar(conexion)
        return {"resultado":error, "sentencia":sentencia}

# Función de autenticación insegura para blind injections via cookie
def login_inseguro_blind_postgresql(cookie_value):
    print("---login_inseguro_blind_postgresql---")
    conexion = dbConectarPostgreSQL()
    if not conexion:
        print("Error: no se pudo conectar para autenticar.")
        return False

    # Simular inyección SQL blind via cookie
    sentencia = "SELECT * FROM Usuarios WHERE session_cookie = '" + cookie_value + "'"
    try:
        cursor = conexion.cursor()
        """
        # Simular retraso si se detecta una función de tiempo en la inyección
        if "sleep(" in cookie_value.lower():
            print("Simulando retraso en la consulta por inyección de tiempo")
            time.sleep(5)  # Retraso de 5 segundos para simular una inyección de tiempo
        """
        cursor.execute(sentencia)
        usuario = cursor.fetchone()
        cursor.close()
        if usuario:
            print("Usuario autenticado:", usuario)
            return {"resultado": usuario, "sentencia": sentencia, "auth": "true"}
        else:
            print("Usuario o cookie incorrectos")
            return {"sentencia": sentencia}
    except PBD.DatabaseError as error:
        print("Error al autenticar usuario con cookie")
        print(error)
        return {"resultado": error, "sentencia": sentencia}
