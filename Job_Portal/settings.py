from pathlib import Path
import os

BASE_DIR = Path(r"C:\Users\ACER\Desktop\LOG\Job_Portal")
LOGIN_REDIRECT_URL = '/accounts/index/'
TIME_ZONE  = 'Asia/Kathmandu'
USE_TZ = True
LOGOUT_REDIRECT_URL = '/'  
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'user_login.log',  # Log to a file
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}


ALLOWED_HOSTS = ['localhost', '127.0.0.1']
DEBUG = True

ROOT_URLCONF = 'Job_Portal.urls'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',  
     'login_history', 
     
]

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # Add this line
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Ensure this is in the right order
    'django.contrib.messages.middleware.MessageMiddleware',  # Add this line
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'default-secret-key-if-not-set')
