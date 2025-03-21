import re

# Lista de palabras clave de SQL
SQL_KEYWORDS = [
    'SELECT', 'FROM', 'WHERE', 'INSERT', 'UPDATE', 'DELETE', 'JOIN',
    'INNER', 'LEFT', 'RIGHT', 'FULL', 'OUTER', 'ON', 'AS', 'GROUP',
    'BY', 'ORDER', 'HAVING', 'LIMIT', 'OFFSET', 'UNION', 'ALL',
    'DISTINCT', 'CREATE', 'TABLE', 'ALTER', 'DROP', 'TRUNCATE',
    'INDEX', 'VIEW', 'PROCEDURE', 'FUNCTION', 'DECLARE', 'SET',
    'VALUES', 'INTO', 'EXISTS', 'BETWEEN', 'LIKE', 'IS', 'NULL',
    'NOT', 'AND', 'OR', 'IN', 'CASE', 'WHEN', 'THEN', 'ELSE', 'END'
]

# Compilar una expresión regular para detectar las palabras clave, ignorando mayúsculas/minúsculas
pattern = re.compile(r'\b(' + '|'.join(SQL_KEYWORDS) + r')\b', re.IGNORECASE)


import re

import re

def generarTarjetaInformacion(title, code):
    """
    Genera el código HTML de una tarjeta con un título, descripción y bloque de código SQL con resaltado de sintaxis,
    incluyendo un tratamiento especial para los comentarios.

    :param title: Título de la tarjeta.
    :param description: Descripción o contenido explicativo.
    :param code: Bloque de código SQL como string.
    :return: String con el código HTML de la tarjeta.
    """

    # Lista de palabras clave de SQL
    SQL_KEYWORDS = [
        'SELECT', 'FROM', 'WHERE', 'INSERT', 'UPDATE', 'DELETE', 'JOIN',
        'INNER', 'LEFT', 'RIGHT', 'FULL', 'OUTER', 'ON', 'AS', 'GROUP',
        'BY', 'ORDER', 'HAVING', 'LIMIT', 'OFFSET', 'UNION', 'ALL',
        'DISTINCT', 'CREATE', 'TABLE', 'ALTER', 'DROP', 'TRUNCATE',
        'INDEX', 'VIEW', 'PROCEDURE', 'FUNCTION', 'DECLARE', 'SET',
        'VALUES', 'INTO', 'EXISTS', 'BETWEEN', 'LIKE', 'IS', 'NULL',
        'NOT', 'AND', 'OR', 'IN', 'CASE', 'WHEN', 'THEN', 'ELSE', 'END', 'DESC'
    ]

    # Compilar expresiones regulares para comentarios, palabras clave y números
    comment_pattern = re.compile(r'(--.*)', re.MULTILINE)
    keyword_pattern = re.compile(r'\b(' + '|'.join(SQL_KEYWORDS) + r')\b', re.IGNORECASE)
    number_pattern = re.compile(r'\b(\d+)\b')

    # Dividir el código en partes: comentarios y no comentarios
    parts = comment_pattern.split(code)

    processed_parts = []

    for i, part in enumerate(parts):
        if i % 2 == 1:
            # Es un comentario, envolver todo el comentario en un span 'comment'
            # No procesar palabras clave o números dentro del comentario
            part = f'<span class="comment">{escape_html(part)}</span>'
        else:
            # No es un comentario, procesar palabras clave y números
            # Reemplazar palabras clave
            part = keyword_pattern.sub(lambda match: f'<span class="keyword">{match.group(0).upper()}</span>', part)
            # Reemplazar números
            part = number_pattern.sub(lambda match: f'<span class="number">{match.group(0)}</span>', part)
            # Escapar caracteres especiales de HTML
            part = escape_html(part)
        processed_parts.append(part)

    # Unir todas las partes procesadas
    highlighted_code = ''.join(processed_parts)

    # Finalmente, insertar el código resaltado en la estructura HTML de la tarjeta
    html = f'''
<article class="card">
    <header class="card-header">
        <h2>{escape_html(title)}</h2>
    </header>
    <div class="card-body">
        <div class="code-block">
            <pre><code>{highlighted_code}</code></pre>
        </div>
    </div>
</article>
'''
    return html.strip()

def escape_html(text):
    """
    Escapa caracteres especiales de HTML en el texto, excepto los ya formateados con spans.

    :param text: Texto a escapar.
    :return: Texto con caracteres HTML escapados.
    """
    # Primero, protegemos los spans existentes para que no sean escapados
    span_pattern = re.compile(r'(<span class="(?:keyword|comment|number)">.*?</span>)', re.DOTALL)
    parts = span_pattern.split(text)
    escaped_parts = []
    for part in parts:
        if span_pattern.match(part):
            escaped_parts.append(part)  # No escapamos los spans
        else:
            escaped_parts.append(
                part.replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                    .replace('"', "&quot;")
                    .replace("'", "&#39;")
            )
    return ''.join(escaped_parts)



if __name__ == "__main__":
    titulo = "Consulta SQL Básica"
    descripcion = """
    A continuación se muestra un ejemplo de una consulta SQL básica que selecciona todos los usuarios de una tabla y los ordena por edad de forma descendente:
    """
    codigo_sql = """-- Seleccionar todos los usuarios y ordenarlos por edad
    SELECT id, nombre, apellido, edad
    FROM usuarios
    WHERE edad >= 18
    ORDER BY edad DESC
    LIMIT 10;"""

    tarjeta_html = generarTarjetaInformacion(titulo, descripcion, codigo_sql)
    print(tarjeta_html)


