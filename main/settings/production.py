"""
Django settings for main project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qz0#1f9=m6e^hc%=9y%v!ol=7g%!m=@ej6!dqkw(y4jywd_e*n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',


    # project apps
    'apps.pages.apps.PagesConfig',
    'apps.accounts.apps.AccountsConfig',


]


SITE_ID = 1

AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = '/login/'
LOGIN_URL_REDIRECT = '/'
LOGOUT_URL = '/logout/'
LOGOUT_REDIRECT_URL = '/login/'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'apps/pages/templates'),
            os.path.join(BASE_DIR, 'apps/accounts/templates'),
            # os.path.join(BASE_DIR, 'apps/search/templates'),
            # os.path.join(BASE_DIR, 'apps/carts/templates'),
            # os.path.join(BASE_DIR, 'apps/accounts/templates'),
            # os.path.join(BASE_DIR, 'apps/addresses/templates'),
            # os.path.join(BASE_DIR, 'apps/billing/templates'),
            # os.path.join(BASE_DIR, 'apps/marketing/templates'),
        ],
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

WSGI_APPLICATION = 'main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)


# *************************** OWN settings ***************************


# ############### Twilio SendGrid ###############

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# DEFAULT_FROM_EMAIL = 'ps96068@gmail.com' #sendgrig sender email
#
# EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'apikey'
# EMAIL_HOST_PASSWORD = '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'


# EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'
# SENDGRID_SANDBOX_MODE_IN_DEBUG = False
# FROM_EMAIL = 'ps96068@yahoo.com' # replace with your address
# SENDGRID_API_KEY = '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'



# need  django-sendgrid-v5

EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'
DEFAULT_FROM_EMAIL = 'ps96068@gmail.com' #sendgrig sender email
SENDGRID_SANDBOX_MODE_IN_DEBUG = False
SENDGRID_ECHO_TO_STDOUT=True
SENDGRID_API_KEY = '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'
BASE_URL = 'http://127.0.0.1:8000'
# ############### END Twilio SendGrid ###############


# ######## MAILCHIMP settings ################

MAILCHIMP_API_KEY           = "f278d3c1cd861d90f0fd6119d24f35f5-us10"
MAILCHIMP_DATA_CENTER       = "us10"
MAILCHIMP_EMAIL_LIST_ID     = "f3d2fd2988"

# ######## END MAILCHIMP settings ################



FORCE_SESSION_TO_ONE = False
FORCE_INACTIVE_USER_ENDSESSION= False




CORS_REPLACE_HTTPS_REFERER      = True
HOST_SCHEME                     = "https://"
SECURE_PROXY_SSL_HEADER         = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT             = True
SESSION_COOKIE_SECURE           = True
CSRF_COOKIE_SECURE              = True
SECURE_HSTS_INCLUDE_SUBDOMAINS  = True
SECURE_HSTS_SECONDS             = 1000000
SECURE_FRAME_DENY               = True