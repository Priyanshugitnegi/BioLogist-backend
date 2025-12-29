from pathlib import Path
import os
import dj_database_url
from corsheaders.defaults import default_headers

BASE_DIR = Path(__file__).resolve().parent.parent

# ──────────────────────────────────────
# SECURITY
# ──────────────────────────────────────
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-change-this-in-production-please!!"
)

DEBUG = False

ALLOWED_HOSTS = [
    "api.biologistinfo.com",
    "biologist-backend-1.onrender.com",
    "localhost",
    "127.0.0.1",
]

# ──────────────────────────────────────
# INSTALLED APPS
# ──────────────────────────────────────
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "rest_framework",
    "django_filters",
    "corsheaders",

    # Local
    "biologist_app.apps.BiologistAppConfig",
]

# ──────────────────────────────────────
# MIDDLEWARE (ORDER IS CRITICAL)
# ──────────────────────────────────────
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # ✅ MUST BE FIRST

    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "biologist_project.urls"

# ──────────────────────────────────────
# TEMPLATES
# ──────────────────────────────────────
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "biologist_project.wsgi.application"

# ──────────────────────────────────────
# DATABASE
# ──────────────────────────────────────
if os.environ.get("DATABASE_URL"):
    DATABASES = {
        "default": dj_database_url.parse(
            os.environ["DATABASE_URL"],
            conn_max_age=600,
            ssl_require=True,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ──────────────────────────────────────
# STATIC & MEDIA
# ──────────────────────────────────────
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
)

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ──────────────────────────────────────
# ✅ CORS (FINAL + PREFLIGHT SAFE)
# ──────────────────────────────────────
CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOWED_ORIGINS = [
    "https://bio-logist-frontend.vercel.app",
    "https://biologistinfo.com",
    "https://www.biologistinfo.com",
]

CORS_ALLOW_CREDENTIALS = True

# 🔥 ALLOW PREFLIGHT HEADERS
CORS_ALLOW_HEADERS = list(default_headers) + [
    "authorization",
]

# 🔥 ALLOW PREFLIGHT METHODS
CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]

# ──────────────────────────────────────
# CSRF
# ──────────────────────────────────────
CSRF_TRUSTED_ORIGINS = [
    "https://bio-logist-frontend.vercel.app",
    "https://biologistinfo.com",
    "https://www.biologistinfo.com",
]

# ──────────────────────────────────────
# DEFAULTS
# ──────────────────────────────────────
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}
