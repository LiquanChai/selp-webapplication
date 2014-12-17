"""
Django settings for quiz project.

For more information on this file, see

For the full list of settings and their values, see
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '868g+*73=-4=0nwh$!3(43q)4m%#%hy3gxw=m%s=%+$#(_eq4i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
USERMGT_TEMPLATE_DIR = os.path.join(BASE_DIR, 'usermgt/templates')
TEMPLATE_DEBUG = True
TEMPLATE_PATH = os.path.join(BASE_DIR, 'template')
TEMPLATE_DIRS = (
        USERMGT_TEMPLATE_DIR,
        TEMPLATE_PATH,
    )

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap_toolkit',
    'quiz',
    'usermgt',
    'south',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'quiz.urls'

WSGI_APPLICATION = 'quiz.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'



MEDIA_ROOT = BASE_DIR + '/media/'
MEDIA_URL = '/media/'
