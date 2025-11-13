"""
Django settings for AssociationDFD project - Optimisé pour Render
"""

from pathlib import Path
from decouple import Config, RepositoryEnv
from dotenv import load_dotenv
import dj_database_url
import os

# -------------------------------------------------------------------
# Chemins & .env
# -------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '.env')
env_path = BASE_DIR / '.env'
if env_path.exists():
    config = Config(RepositoryEnv(str(env_path)))
else:
    from decouple import config  # fallback si .env absent

def env_bool(name: str, default: bool = False) -> bool:
    return os.getenv(name, str(default)).strip().lower() in {"1", "true", "yes", "on"}

# -------------------------------------------------------------------
# Debug & Secret Key
# -------------------------------------------------------------------
DEBUG = env_bool("DEBUG", False)

SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = 'dev-secret-key-for-local-only'
    else:
        raise ValueError("SECRET_KEY environment variable must be set in production")

# -------------------------------------------------------------------
# Hôtes & proxy TLS (Render)
# -------------------------------------------------------------------
ALLOWED_HOSTS = ["localhost", "127.0.0.1", ".onrender.com", "0.0.0.0"]
# Si Render expose un hostname dédié, on l'ajoute
_render_host = os.getenv("RENDER_EXTERNAL_HOSTNAME")
if _render_host:
    ALLOWED_HOSTS.append(_render_host)

# Django 4.x exige le schéma pour CSRF_TRUSTED_ORIGINS
CSRF_TRUSTED_ORIGINS = ["https://*.onrender.com"]

# Sur Render, TLS est terminé en amont ; on fait confiance à cet en-tête
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# -------------------------------------------------------------------
# Applications & Middleware
# -------------------------------------------------------------------
APPEND_SLASH = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'paypal.standard.ipn', 
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # WhiteNoise doit être haut
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = 'AssociationDFD.urls'

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

WSGI_APPLICATION = 'AssociationDFD.wsgi.application'

# -------------------------------------------------------------------
# Base de données : PostgreSQL via DATABASE_URL (Render) sinon SQLite
# -------------------------------------------------------------------
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# -------------------------------------------------------------------
# Auth
# -------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -------------------------------------------------------------------
# Internationalisation
# -------------------------------------------------------------------
LANGUAGE_CODE = 'fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('fr', 'Français'),
    ('en', 'English'),
    ('it', 'Italiano'),
]

LOCALE_PATHS = [BASE_DIR / 'locale']

# -------------------------------------------------------------------
# Fichiers statiques & médias (WhiteNoise)
# -------------------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Ne référence le dossier "static" que s'il existe (évite une erreur en prod)
_static_dir = BASE_DIR / "static"
STATICFILES_DIRS = [_static_dir] if _static_dir.exists() else []

# WhiteNoise
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
WHITENOISE_AUTOREFRESH = DEBUG           # auto-reload en dev
WHITENOISE_MAX_AGE = 0 if DEBUG else 31536000  # cache agressif en prod

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -------------------------------------------------------------------
# Email
# -------------------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# -------------------------------------------------------------------
# Sécurité (prod uniquement)
# -------------------------------------------------------------------
SECURE_SSL_REDIRECT = not DEBUG  # un seul endroit ; évite les doublons

if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    # SECURE_BROWSER_XSS_FILTER supprimé en Django 4+ (ne rien définir)
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# -------------------------------------------------------------------
# Logging
# -------------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {'console': {'class': 'logging.StreamHandler'}},
    'root': {'handlers': ['console'], 'level': 'INFO'},
    # Optionnel : verbeux pour le serveur de dev
    'loggers': {
        'django.server': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}


# ===================================
# PAYPAL CONFIGURATION
# ===================================

# PayPal Settings
PAYPAL_TEST = os.getenv('PAYPAL_TEST', 'True') == 'True'  # True pour sandbox, False pour production

# Identifiants PayPal (à mettre dans .env)
PAYPAL_RECEIVER_EMAIL = os.getenv('PAYPAL_RECEIVER_EMAIL', 'sb-youremail@business.example.com')
PAYPAL_CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID', '')
PAYPAL_SECRET = os.getenv('PAYPAL_SECRET', '')

# URLs de retour PayPal
PAYPAL_RETURN_URL = 'http://localhost:8000/paypal-return/'
PAYPAL_CANCEL_URL = 'http://localhost:8000/paypal-cancel/'
PAYPAL_NOTIFY_URL = 'http://localhost:8000/paypal-ipn/'  # Pour IPN



