from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True  # Only for development!

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Debug toolbar settings
INSTALLED_APPS += ['debug_toolbar'],
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware'],
INTERNAL_IPS = ['127.0.0.1']