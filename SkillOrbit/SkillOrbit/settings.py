"""
Django settings for SkillOrbit project.
"""

import os
from pathlib import Path
from urllib.parse import urlparse

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-9lo-01_mw*2vp)8c1l2q6w3^te^z^1*50(a_t!=y8e-4sb)h^d'

DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'daphne',
    'session',
    'chat',
    'skill',
    'core',
    'course',
    'channels',
    'jazzmin',
    'accounts',
    'channels_redis',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

SITE_ID = 1

ASGI_APPLICATION = 'SkillOrbit.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}

LOGIN_URL = 'signin'
LOGIN_REDIRECT_URL = 'profile'
ACCOUNT_LOGOUT_REDIRECT_URL = 'signout'
AUTH_USER_MODEL = 'accounts.CustomUser'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backend.AuthenticationBackend',
)

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'OAUTH_PKCE_ENABLED': True,
        'APPS': [{
            'client_id': '',
            'secret': '',
            'key': ''
        }]
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

JAZZMIN_SETTINGS = {
    "site_brand": "SkillOrbit Admin",
    "theme": "cyborg",
    "dark_mode_theme": "cyborg",
    "ui_dark_mode": True,
    "custom_css": "admin/css/admin.css",
}

JAZZMIN_UI_TWEAKS = {
    "theme": "cyborg",
    "dark_mode_theme": "cyborg",
    "ui_dark_mode": True,
    "navbar": "navbar-dark bg-dark",
    "sidebar": "sidebar-dark-warning",
    "accent": "accent-warning",
    "button_classes": {
        "primary": "btn-warning",
        "secondary": "btn-secondary"
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'SkillOrbit.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'skill.context_processors.pending_request',
                'chat.context_processors.unread_messages_count',
                'skill.context_processors.connection_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'SkillOrbit.wsgi.application'

# Database Configuration (Supports Render.com DATABASE_URL environment variable)
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    db_info = urlparse(DATABASE_URL)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': db_info.path[1:],
            'USER': db_info.username,
            'PASSWORD': db_info.password,
            'HOST': db_info.hostname,
            'PORT': db_info.port or 5432,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'skillorbit_db',        
            'USER': 'skillorbit_user',     
            'PASSWORD': 'skillorbit_password',      
            'HOST': 'localhost',              
            'PORT': '5432',                   
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'