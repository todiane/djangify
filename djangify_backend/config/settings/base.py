from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party apps
    "rest_framework",
    "corsheaders",
    "django_filters",
    "drf_spectacular",
    "django_summernote",
    # Local apps
    "djangify_backend.apps.blog",
    "djangify_backend.apps.portfolio",
    "djangify_backend.apps.core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Add this line
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "djangify_backend.config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # Updated path
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


WSGI_APPLICATION = "djangify_backend.config.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "djangify"),
        "USER": os.getenv("DB_USER", "djangify_user"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5434"),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "djangify_backend" / "static"

# Media files configuration

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "djangify_backend" / "media"

# Maximum upload size (5MB)
MAX_UPLOAD_SIZE = 5242880

# Image optimization settings
IMAGE_OPTIMIZATION = {
    "MAX_DIMENSION": (1920, 1080),  # Maximum dimensions for project images
    "THUMBNAIL_SIZE": (200, 200),  # Thumbnail dimensions
    "QUALITY": 85,  # JPEG quality
    "FORMATS": ["JPEG", "PNG"],  # Allowed formats
}

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# CORS settings
CORS_ALLOW_ALL_ORIGINS = DEBUG  # Allows all origins in development

if not DEBUG:
    # In production, explicitly list allowed origins
    CORS_ALLOWED_ORIGINS = os.getenv(
        "CORS_ALLOWED_ORIGINS", "http://localhost:3000"
    ).split(",")

# Additional CORS settings you might want
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "apps.core.throttling.BurstRateThrottle",
        "apps.core.throttling.SustainedRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "burst": "10/minute",
        "sustained": "100/hour",
        "user_burst": "20/minute",
        "user_sustained": "200/hour",
        "write_operations": "30/hour",
    },
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_PAGINATION_CLASS": "djangify_backend.apps.core.pagination.CustomPagination",
    "PAGE_SIZE": 12,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}


# djangify_backend/config/settings/base.py

SPECTACULAR_SETTINGS = {
    "TITLE": "Djangify API",
    "DESCRIPTION": "API for Djangify portfolio and blog",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    # Other settings...
    "SWAGGER_UI_SETTINGS": {
        "persistAuthorization": True,
    },
    "PREPROCESSING_HOOKS": [],
    "SERVE_PERMISSIONS": ["rest_framework.permissions.AllowAny"],
    "SCHEMA_PATH_PREFIX": "/api/v1",
}


# Debug toolbar settings
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG,
}

SUMMERNOTE_CONFIG = {
    # Use this to customize the editor
    "iframe": True,
    "summernote": {
        # Customize editor size
        "width": "100%",
        "height": "480",
        # Toolbar customization
        "toolbar": [
            ["style", ["style"]],
            ["font", ["bold", "underline", "clear"]],
            ["fontname", ["fontname"]],
            ["color", ["color"]],
            ["para", ["ul", "ol", "paragraph"]],
            ["table", ["table"]],
            ["insert", ["link", "picture", "video"]],
            ["view", ["fullscreen", "codeview", "help"]],
        ],
        # Customize which tags are allowed
        "styleTags": ["p", "h1", "h2", "h3", "h4", "h5", "h6"],
        # Set default font family
        "fontNames": [
            "Arial",
            "Arial Black",
            "Comic Sans MS",
            "Courier New",
            "Helvetica Neue",
            "Merriweather",
        ],
        # Configure image upload settings
        "attachments": True,
        "width": "100%",
    },
    # Set maximum file size (in bytes)
    "attachment_filesize_limit": 5 * 1024 * 1024,  # 5MB
    # Restrict upload file types
    "attachment_upload_to": "summernote",
    "attachment_allowed_types": ["image/jpeg", "image/svg", "image/png", "image/gif"],
}

X_FRAME_OPTIONS = "SAMEORIGIN"

# Add SVG to Django's allowed upload formats
FILE_UPLOAD_HANDLERS = [
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
]

# Configurations for better file upload handling
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5 MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5 MB

# Add SVG MIME type
MIME_TYPES = {
    "svg": "image/svg+xml",
}

# djangify_backend/config/settings/development.py
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

# Logging Configuration
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/djangify.log"),
            "formatter": "verbose",
        },
    },
    "loggers": {
        "": {  # Root logger
            "handlers": ["console", "file"],
            "level": "INFO",
        },
        "djangify_backend": {  # Your project's logger
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "django": {  # Django's internal logger
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# Create logs directory if it doesn't exist
LOGS_DIR = os.path.join(BASE_DIR, "logs")
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)


# Email settings for notifications
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("EMAIL_HOST_USER")
ADMIN_EMAIL = os.getenv("EMAIL_HOST_USER")


# URL of your Next.js frontend
FRONTEND_URL = "http://localhost:3000"  # Development
# FRONTEND_URL = 'https://your-production-domain.com'  # Production
SITE_NAME = "Djangify"

APPEND_SLASH = True
