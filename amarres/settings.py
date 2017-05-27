"""
Django settings for amarres project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c%43#m_js5k4%8@s5f4l1o@^q6fbs^fzs!_c%y!4f9ol0ijjlr'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]', '172.19.2.133', '192.168.1.90', 'www.amarreapp.net', '90.162.116.26', 'www.econavbalear.net']


# Application definition

INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # Third party apps
    'registration',
    'crispy_forms',
    # My apps
    'amarreapp.apps.AmarreappConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'amarres.urls'

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

WSGI_APPLICATION = 'amarres.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'NAME': 'amarres_db',
#        'USER': 'amarres_db',
#        'PASSWORD': 'amarres_db',
#    }
#}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'es'
LANGUAGES = (                                                                   
      ('es', 'Spanish'),                                                          
      ('en', 'English'),                                                          
)
    
TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Settings django-registration-redux
#
# Begin by adding registration to the INSTALLED_APPS setting of your project,
# and specifying one additional setting:
#
# ACCOUNT_ACTIVATION_DAYS
#    This is the number of days users will have to activate their accounts 
# after registering. If a user does not activate within that period, the
# account will remain permanently inactive and may be deleted by maintenance
# scripts provided in django-registration-redux.
# REGISTRATION_DEFAULT_FROM_EMAIL
#    Optional. If set, emails sent through the registration app will use 
# this string. Falls back to using Django’s built-in DEFAULT_FROM_EMAIL setting.
# REGISTRATION_EMAIL_HTML
#    Optional. If this is False, registration emails will be send in plain text.
#  If this is True, emails will be sent as HTML. Defaults to True.
# REGISTRATION_AUTO_LOGIN
#    Optional. If this is True, your users will automatically log in when they
# click on the activation link in their email. Defaults to False. 
# REGISTRATION_OPEN
#    A boolean (either True or False) indicating whether registration of new
# accounts is currently permitted. A default of True will be assumed if this
# setting is not supplied. 
REGISTRATION_OPEN = True                # If True, users can register
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_AUTO_LOGIN = False
SITE_ID = 1
 # The page you want users to arrive at after they successful log in
LOGIN_REDIRECT_URL = '/econavbalear/'
# The page users are directed to if they are not logged in,
# and are trying to access pages requiring authenticatio
LOGIN_URL = '/accounts/login/'  
