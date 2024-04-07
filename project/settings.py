
from pathlib import Path
from decouple import config # TODO : not working with .env file

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-tsc#00gth%-k2e)+jc!6te&rtpw3^y2&$g)ny5vx(18%r+2x0t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

SHARED_APPS = (
    'django_tenants',  # mandatory
    'backend', # myapp where my tenant model resides in

    # everything below here is optional
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tenant_users.permissions',   
    'tenant_users.tenants', 
)

TENANT_APPS = (
    'tenants', # myapp tenants models resides in
    'django.contrib.auth', # Defined in both shared apps and tenant apps
    'django.contrib.contenttypes', # Defined in both shared apps and tenant apps
    'tenant_users.permissions', # Defined in both shared apps and tenant apps
)

INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]

# Modèle qui représente un tenant = 'Client' qui est défini dans app backend.
TENANT_MODEL = "backend.Client"

# Modèle qui représente le domain d'un tenant = 'Domain' qui est défini dans app backend.
TENANT_DOMAIN_MODEL = "backend.Domain"

# Les backends d'authentification à utiliser pour vérifier les informations d'identification des utilisateurs lors de la connexion.
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend", "tenant_users.permissions.backend.UserBackend"
]

TENANT_USERS_DOMAIN = "localhost"

'''
Le modèle spécifique au tenant (TenantUser) dans backend est utilisé à la fois: 
comme modèle pour représenter les utilisateurs associés à chaque tenant; 
et comme modèle global pour représenter tous les utilisateurs de l'application.
TENANT_USER_MODEL est spécifique à l'environnement multi-tenant de votre 
application, indiquant à Django quel modèle utiliser pour représenter 
les utilisateurs associés à chaque locataire, tandis que AUTH_USER_MODEL 
est utilisé de manière plus générale pour définir le modèle d'utilisateur pour toute l'application.
'''

TENANT_USER_MODEL = "backend.TenantUser"
AUTH_USER_MODEL = "backend.TenantUser"

MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

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

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

''' TODO : not working with .env file
DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

'''

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': 'numedia_db',
        'USER': 'numedia_user',
        'PASSWORD': 'numedia_user',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SHOW_PUBLIC_IF_NO_TENANT_FOUND = True #Temporary for creating 1st public tenant using browser django admin
