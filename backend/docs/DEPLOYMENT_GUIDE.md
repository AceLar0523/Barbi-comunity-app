# Guía de Despliegue en Producción

Estos son los pasos recomendados para llevar tu aplicación (Backend y Frontend) de un entorno local a uno público y productivo.

## 1. Backend (Django REST)
El servidor de Django **no debe** ejecutarse con `runserver` en producción, ya que no es seguro ni escalable.

1. **Hosting**: Sube el código de la carpeta `/backend` a plataformas en la nube como Render, AWS, DigitalOcean o Heroku.
2. **Base de Datos**: Utiliza un servicio administrado de PostgreSQL (ej. Amazon RDS, Supabase o Neon) en lugar de una base de datos local, para garantizar respaldos y alta disponibilidad.
3. **Servidores WSGI**: Usa **Gunicorn** u **uWSGI** para servir la aplicación de Python.
4. **Proxy Inverso**: Configura **Nginx** por delante de Gunicorn para manejar las peticiones HTTPS y servir archivos estáticos/media.
5. **Ajustes de Seguridad Críticos en `settings.py`**:
   - `DEBUG = False` (Evita revelar código en caso de error).
   - Genera una nueva variable de entorno para `SECRET_KEY` exclusiva para producción.
   - En `ALLOWED_HOSTS`, reemplaza `['*']` por tu dominio real (ej. `['api.tu-app.com']`).
   - Configura HTTPS mediante certificados SSL gratuitos de Let's Encrypt.

## 2. Frontend (Aplicación Flutter)
Una vez que tu backend esté publicado en internet bajo un dominio real (ej. `https://api.tu-app.com`), debes enlazar el frontend.

El archivo `api_service.dart` ya está programado para utilizar la URL productiva de forma automática si compilas en "Release Mode" (`kReleaseMode`). Asegúrate de editar allí el String `https://api.tu-dominio-produccion.com/api` con tu dominio real.

Para compilar la aplicación final y distribuirla en tiendas:
- **Para Android**:
  ```bash
  flutter build appbundle
  ```
- **Para iOS**:
  ```bash
  flutter build ipa
  ```

Sube los archivos generados a **Google Play Console** y **Apple App Store Connect** respectivamente.
