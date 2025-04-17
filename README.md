# 🏋️‍♂️ Report

**Repórtense banda CHANGE**

Report es una aplicación web ligera que permite a un grupo de amigos registrar y ver su actividad en el gimnasio a través de una interfaz simple y adaptada a dispositivos móviles. Los usuarios pueden registrarse diariamente, opcionalmente subir detalles de su entrenamiento y una foto, y ver un informe diario/semanal de la actividad de todos.

## Características

- **Identificación Simple**: Los usuarios se identifican ingresando un nombre o seleccionando de una lista desplegable de usuarios existentes. Grupos predefinidos incluyendo "Cabritinhas".
- **Registro Diario**: Seguimiento de asistencia al gimnasio con un proceso de registro simple.
- **Detalles Opcionales**: Comparte qué entrenaste y sube fotos de tu entrenamiento.
- **Feed de Grupo**: Visualiza los registros recientes de todos, ordenables por fecha o persona.
- **Interfaz Optimizada para Móviles**: Diseño responsive que funciona bien en cualquier dispositivo.
- **Captura de Fotos**: Usa la cámara de tu dispositivo directamente desde la aplicación.

## Backend

La aplicación utiliza Google Sheets como base de datos y Google Drive para almacenamiento de imágenes:

- Google Sheets almacena datos de registros (marca de tiempo, nombre de usuario, descripción del entrenamiento, URL de imagen)
- Google Drive aloja fotos de entrenamientos subidas
- Ambos se acceden a través de clientes de API de Google en el backend de Flask

## Configuración Local

### Variables de Entorno Requeridas

Para usar las APIs de Google Sheets y Drive, se necesitan las siguientes variables de entorno:

- `GOOGLE_SHEETS_API_KEY`: Credenciales JSON para acceso a la API de Google Sheets
- `GOOGLE_DRIVE_API_KEY`: Credenciales JSON para acceso a la API de Google Drive
- `GOOGLE_SHEET_ID`: ID de la hoja de Google Sheets a utilizar para almacenar datos
- `GOOGLE_DRIVE_FOLDER_ID`: ID de la carpeta de Google Drive para almacenar imágenes
- `SESSION_SECRET`: Clave secreta para cifrado de sesión de Flask

Sin estas variables, la aplicación funciona en modo desarrollo con datos locales temporales.

### Ejecución de la Aplicación Local

Para iniciar el servidor:

```bash
gunicorn --bind 0.0.0.0:5000 main:app
```

## Despliegue en Render

Para desplegar esta aplicación en Render, sigue estos pasos:

### Método 1: Despliegue manual con Poetry

1. **Fork o clona este repositorio** en tu cuenta de GitHub

2. **Crea un nuevo Web Service en Render**:
   - Conecta tu cuenta de GitHub a Render
   - Selecciona el repositorio
   - Configura el servicio:
     - **Nombre**: Elige un nombre para tu app
     - **Environment**: Python 3
     - **Build Command**: `poetry install`
     - **Start Command**: `gunicorn main:app`

3. **Configura las variables de entorno** en la sección Environment Variables:
   - `GOOGLE_SHEETS_API_KEY`
   - `GOOGLE_DRIVE_API_KEY`
   - `GOOGLE_SHEET_ID`
   - `GOOGLE_DRIVE_FOLDER_ID`
   - `SESSION_SECRET`
   - `PYTHON_VERSION`: 3.11.11
   - `POETRY_VERSION`: 1.7.1

4. **Despliega** haciendo clic en "Create Web Service"

### Método 2: Despliegue automático con Blueprint

Este repositorio incluye un archivo `render.yaml` que configura automáticamente el despliegue con Poetry. Para usarlo:

1. **Fork o clona este repositorio** en tu cuenta de GitHub

2. Ve a [Render Dashboard](https://dashboard.render.com/) y selecciona "Blueprint" en el menú

3. Conecta tu repositorio de GitHub

4. Render detectará el archivo `render.yaml` y configurará automáticamente el servicio con Poetry

5. **Configura las variables de entorno** en la sección Environment Variables del servicio creado

Tu aplicación estará disponible en la URL asignada por Render: `https://tu-app.onrender.com`

## Desarrollo

La aplicación está construida con:

- **Flask**: Framework web de Python
- **Bootstrap 5**: Componentes UI responsive
- **Google API Client**: Para integración con Sheets y Drive

## Licencia

Este proyecto está licenciado bajo la Licencia MIT.
