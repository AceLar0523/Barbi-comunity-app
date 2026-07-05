# Guía de Configuración del Backend (Django)

Esta guía explica cómo configurar e iniciar el servidor local para el desarrollo.

## Requisitos Previos
- Python 3.10 o superior.
- PostgreSQL (Base de datos).
- Entorno virtual activado (`venv`).

## 1. Instalación de Dependencias
Abre una terminal en la carpeta `/backend` y ejecuta:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 2. Configuración de Base de Datos y Variables de Entorno (.env)
1. Asegúrate de tener PostgreSQL instalado e iniciado, y crea una base de datos local (por ejemplo `barbidb`).
2. Copia el archivo de ejemplo para crear tus propias variables de entorno:
```bash
cp "example .env" .env
```
3. Edita el archivo `.env` agregando tu clave de OpenAI (necesaria para la visión por computadora) y las credenciales de la base de datos de PostgreSQL.

## 3. Migraciones
Aplica las migraciones para inicializar las tablas en tu base de datos:
```bash
python manage.py makemigrations
python manage.py migrate
```

## 4. Iniciar el Servidor Local
Para permitir que la app móvil se conecte al servidor desde un teléfono físico, debes iniciarlo escuchando en todas las interfaces de red (`0.0.0.0`):

```bash
python manage.py runserver 0.0.0.0:8000
```

> [!NOTE]
> La IP local (ej. `192.168.1.224`) de la computadora donde corre este servidor se utilizará en el frontend para realizar las peticiones a esta API.
