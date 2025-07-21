# config/settings.py

from pathlib import Path
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================================================================
# CONFIGURACIÓN DE SEGURIDAD Y PRODUCCIÓN
# ==============================================================================

# CORRECTO: Lee la SECRET_KEY desde las variables de entorno de Render.
# Si no la encuentra, usa una clave de desarrollo (no segura para producción).
SECRET_KEY = os.environ.get(
    'SECRET_KEY', 'django-insecure-fallback-key-for-development'
)

# ERROR CORREGIDO: Se eliminó la segunda definición de SECRET_KEY que estaba hardcodeada.

# DEBUG será 'False' en producción (cuando Render esté presente) y 'True' en tu PC.
DEBUG = 'RENDER' not in os.environ

# Configuración de hosts permitidos para Render.
ALLOWED_HOSTS = []

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


# ==============================================================================
# APLICACIONES Y MIDDLEWARE
# ==============================================================================

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary',
    'inventario',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # CORRECTO: Whitenoise debe ir justo después de SecurityMiddleware.
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# ==============================================================================
# BASE DE DATOS
# ==============================================================================

# Esta configuración está perfecta. Usará Neon en producción y SQLite en local.
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}


# ==============================================================================
# VALIDACIÓN DE CONTRASEÑAS Y LOCALIZACIÓN
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# SUGERENCIA: Ajustado para Chile.
LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True


# ==============================================================================
# ARCHIVOS ESTÁTICOS Y DE MEDIOS (CONFIGURACIÓN DEFINITIVA)
# ==============================================================================

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Esta línea asegura que Whitenoise pueda comprimir y cachear los archivos de forma eficiente.
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Se elimina la variable STATICFILES_DIRS para evitar confusiones, ya que no
# tenemos una carpeta 'static' propia. Django encontrará los archivos del admin
# automáticamente.

MEDIA_URL = '/media/'
# La siguiente línea no es necesaria en producción porque usamos Cloudinary,
# pero la dejamos para mantener la compatibilidad en desarrollo local.
MEDIA_ROOT = BASE_DIR / 'media'

# ==============================================================================
# CONFIGURACIÓN DE CLOUDINARY PARA ALMACENAMIENTO DE MEDIOS
# ==============================================================================
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'