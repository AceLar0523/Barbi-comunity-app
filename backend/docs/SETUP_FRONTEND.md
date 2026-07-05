# Guía de Configuración del Frontend (Flutter)

Esta aplicación móvil está desarrollada con Flutter y permite la interacción directa con el backend para guardar y clasificar la colección de muñecas.

## Requisitos Previos
- [Flutter SDK](https://docs.flutter.dev/get-started/install) (versión 3.x+).
- Android Studio o Xcode (para simuladores/emuladores o compilación).
- Un celular físico o un emulador.

## 1. Instalación de Dependencias
Abre una terminal en la carpeta `/frontend` y ejecuta:
```bash
flutter pub get
```

## 2. Configurar la IP del Servidor Backend
Para que tu celular físico pueda conectarse a tu computadora (donde corre Django localmente), ambas deben estar en la misma red Wi-Fi.

En desarrollo, la IP estática está configurada en `frontend/lib/services/api_service.dart`.
Si cambiaste de red Wi-Fi o te fuiste a otro lugar, tu IP local cambiará. Tienes dos opciones para solucionarlo:
1. **Opción Dinámica (Recomendada)**: Compila la aplicación pasando tu nueva IP desde la terminal sin modificar código:
   ```bash
   flutter run --dart-define=API_URL=http://NUEVA_IP_DE_TU_PC:8000/api
   ```
2. **Opción Manual**: Edita el archivo `frontend/lib/services/api_service.dart` y cambia la constante `baseUrl` de forma manual.

## 3. Ejecutar la Aplicación
Conecta tu dispositivo celular mediante USB (o Wi-Fi debugging), y ejecuta:
```bash
flutter run
```

## 4. Personalización del Icono
El icono de la aplicación ha sido configurado usando `flutter_launcher_icons`. Si deseas cambiar el logotipo en el futuro:
1. Reemplaza la imagen en `frontend/assets/logo.png`.
2. Luego ejecuta en la carpeta `frontend`:
   ```bash
   dart run flutter_launcher_icons
   ```
