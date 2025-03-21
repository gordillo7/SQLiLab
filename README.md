# Laboratorio de SQL Injection con Flask

Este proyecto es un laboratorio práctico creado para aprender desde cero sobre vulnerabilidades de tipo **inyección SQL (SQL Injection)** utilizando una aplicación web desarrollada en **Python con Flask**. La aplicación permite simular y explotar vulnerabilidades controladas en bases de datos Oracle y PostgreSQL, ayudando a los usuarios a entender los riesgos y cómo prevenir este tipo de ataques.

---

## 📋 Requisitos previos

Asegúrate de tener instalado:

- Python 3.8 o superior
- Oracle Database
- PostgreSQL

---

## 🛠️ Instalación

1. Clona el repositorio o descarga y descomprime el archivo ZIP del proyecto.

2. Accede al directorio del proyecto desde la terminal:
```bash
cd SQLiLab
```

3. Instala las dependencias necesarias ejecutando:
```bash
pip install -r requirements.txt
```

---

## 🚀 Ejecutar la aplicación

Para lanzar la aplicación, ejecuta el archivo principal `app.py` desde la terminal:

```bash
python app.py
```

La aplicación estará disponible en tu navegador web accediendo a:

```
http://localhost:5000
```

---

## 📖 Contenido del proyecto

- **app.py**: Aplicación principal de Flask.
- **setupOracle.py / setupPostgreSQL.py**: Scripts para configurar y poblar inicialmente las bases de datos Oracle y PostgreSQL.
- **diccionarioInyecciones.py**: Ejemplos y payloads útiles para practicar SQL Injection.
- **static/** y **templates/**: Archivos estáticos y plantillas HTML usadas por Flask.
- **scripts/**: Scripts para automatizar la explotación de las inyecciones de tipo *blind*.

---

## ⚠️ Advertencia

Este laboratorio está diseñado exclusivamente con fines educativos. Úsalo únicamente en entornos seguros y controlados. El autor no es responsable del mal uso de las herramientas proporcionadas.

Así mismo, se recomienda el uso de este laboratorio en entornos locales y no en servidores públicos, ya que la aplicación cuenta con vulnerabilidades intencionales que podrían ser explotadas por terceros.

---

## 📌 Licencia

Este proyecto se distribuye bajo una licencia *Creative Commons Atribución-NoComercial 4.0 Internacional (CC BY-NC 4.0)* [!Imagen de la licencia](https://mirrors.creativecommons.org/presskit/buttons/88x31/png/by-nc.png)
