from pathlib import Path
import os
import socket
import sys
from decouple import config


BASE_DIR = Path(__file__).resolve().parent.parent

if os.environ.get("GITHUB_ACTIONS") == "true":
    SECRET_KEY = '459a2211e3e1cb2219fde2460560070c7081872b629211708'
else:
    SECRET_KEY = config('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['137.63.148.211', 'ip.it.renu.ac.ug', '127.0.0.1', 'f36c-197-239-9-19.ngrok-free.app']

if 'test' in sys.argv or 'test_coverage' in sys.argv:
    COVERAGE_MODULE_EXCLUDES = ['tests', 'mainapp/migrations', 'migrations', 'settings']
    COVERAGE_REPORT_HTML_OUTPUT_DIR = 'coverage_html'

if 'test' in sys.argv or 'test_coverage' in sys.argv:
    COVERAGE_MODULE_EXCLUDES = ['tests', 'mainapp/migrations', 'migrations', 'settings']
    COVERAGE_REPORT_HTML_OUTPUT_DIR = 'coverage_html'

# Application definition

INSTALLED_APPS = [
    'mainapp',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ip-monitoring-tool.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'ip-monitoring-tool.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/ip-monitoring-logs.log',
            'formatter': 'verbose',
        },
        'file2': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/deployment-logs.log',
            'formatter': 'verbose',
        },
        'file3': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/auth-logs.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'ip-monitoring-tool': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'deployment': {
            'handlers': ['file2'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'auth': {
            'handlers': ['file3'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}



# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = 'static/'


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'dashboard'
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'

# Session
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 900 # 15minutes

# Secure flag for the session cookie (set it to True for HTTPS-only)
SESSION_COOKIE_SECURE = True

CSRF_TRUSTED_ORIGINS = ['https://ip.it.renu.ac.ug', 'https://f36c-197-239-9-19.ngrok-free.app']

EMAIL_HOST = socket.gethostbyname('smtp.gmail.com')
EMAIL_PORT = 587  # Replace with your SMTP server port (587 for TLS, 465 for SSL)
EMAIL_USE_TLS = False  # Use TLS (True) or SSL (False) depending on your server configuration
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'renutest100@gmail.com'  # Replace with your email address
EMAIL_HOST_PASSWORD = config('EMAIL_PASSWORD')
DEFAULT_FROM_EMAIL = 'admin@renu.ac.ug'  # Replace with the email address to appear as the sender
