import os
from pathlib import Path
from urllib import parse
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from corsheaders.defaults import default_headers
import cloudinary

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Loading Env
env_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path = env_path)

cloudinary.config(
    cloud_name = os.getenv(key='CLOUD_NAME'),
    api_key = os.getenv(key='API_KEY'),
    api_secret = os.getenv(key='API_SECRET'),
    secure = True
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(key='SECRET_KEY')
REFRESH_SECRET_KEY = os.getenv(key='REFRESH_SECRET_KEY')
ACCESS_TOKEN_EXPIRY = 30
REFRESH_TOKEN_EXPIRY = 24*60

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',

    'accounts'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True



# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
# Restart: sudo /etc/init.d/mysql start

DB_HOST = os.getenv(key = 'DB_HOST')
DB_NAME = os.getenv(key = 'DB_NAME')
DB_USER = os.getenv(key = 'DB_USER')
DB_PASSWORD = os.getenv(key = 'DB_PASSWORD')
DB_PORT = os.getenv(key = 'DB_PORT')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
        'TIME_ZONE': TIME_ZONE
    }
}

DATABASE_URL = 'mysql://' + \
    DB_USER + ':' + \
    parse.quote_plus(DB_PASSWORD) + '@' + \
    DB_HOST + '/' + DB_NAME

ENGINE = create_engine(DATABASE_URL, pool_pre_ping=True, echo = False)
METADATA = MetaData(bind=ENGINE)
SAL_SESSION = sessionmaker(bind=ENGINE)
DB_SESSION = SAL_SESSION()

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '{name} {levelname} {message}',
            'style': '{',
        },
        'file': {
            'format': 'Time: {asctime} | App: {name} | {levelname}: {message}',
            'style': '{',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'accounts.file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': './logs/accounts.log',
        },
    },
    'loggers': {
        'accounts': {
            'handlers': ['console', 'accounts.file'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ],
}