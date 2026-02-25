"""
Django settings for Voter Analysis Backend
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-dev-key-change-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ["202.79.51.253", "localhost", "127.0.0.1", "api.voter.election.dahalpradeep.com.np", "django"]

# Application definition
INSTALLED_APPS = [
    # Django built-in apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'drf_spectacular',
    'corsheaders',          # ✅ CORS
    'django_extensions',

    # Our apps
    'voters',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',   # ✅ MUST be first
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',   # ✅ CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

# Database
import dj_database_url

# DATABASES = {
#         "default": dj_database_url.config(default=os.getenv("DATABASE_URL")),
#         'ENGINE': 'django.db.backends.postgresql',
# }


#
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'area' / 'area.sqlite3',
#        "OPTIONS": {
#            "timeout": 60,  # seconds
#        },
#    }
#}
#
DATABASES = {
  'default': {
      'ENGINE': 'django.db.backends.postgresql',
      'NAME': 'mydb',
      'USER': 'username',
      'PASSWORD': 'password',
       'HOST': 'postgres',  # matches docker-compose service name
       'PORT': '5432',
  }
}
# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kathmandu'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'data' / 'uploads'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

# =======================
# CORS + CSRF SETTINGS
# =======================

# Dev only – allow all origins
CORS_ALLOW_ALL_ORIGINS = True

# If frontend uses cookies / sessions
CORS_ALLOW_CREDENTIALS = True

# Trust your frontend for CSRF
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://202.79.51.253",
    "https://api.voter.election.dahalpradeep.com.np",
    "https://voter.election.dahalpradeep.com.np"
]



# API Documentation Settings (Swagger)
SPECTACULAR_SETTINGS = {
    'TITLE': 'Voter Analysis API',
    'DESCRIPTION': 'API for analyzing ward-level voter demographic data',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    
    # Swagger UI settings
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': True,
    },
    
    # Schema settings
    'COMPONENT_SPLIT_REQUEST': True,
}




# Max size of request body (in bytes)


# # Max size of request body (in bytes)
# DATA_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024  # 50 MB

# # Max size of uploaded file kept in memory (before writing to disk)
# FILE_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024  # 50 MB

# CORS Settings (for frontend integration)
# CORS_ALLOW_ALL_ORIGINS = True  # Relaxed for development
# CORS_ALLOWED_ORIGINS = os.environ.get(
#     'CORS_ALLOWED_ORIGINS',
#     "http://localhost:3000"
# # ).split(',')

# CORS_ALLOW_CREDENTIALS = True

# Allow all HTTP methods
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# Allow all headers including those needed for file uploads
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]


# File Upload Settings
# Limit to 55MB to prevent timeouts
DATA_UPLOAD_MAX_MEMORY_SIZE = 55 * 1024 * 1024   # 50MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 55 * 1024 * 1024   # 50MB



# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'data' / 'django.log',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'voters': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"
