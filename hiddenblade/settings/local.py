DEBUG = True
TEMPLATE_DEBUG = DEBUG
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hiddenblade',
        'USER': 'vagrant',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)
THIRD_PARTY_APPS = (
    'debug_toolbar',
)

LOCAL_APPS = (
    'players',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

ALLOWED_HOSTS=['*']

INTERNAL_IPS = (
    '10.0.2.2',
)
