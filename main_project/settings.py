from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-default-key-for-dev-only')

# 在 .env 文件中设置 DJANGO_DEBUG=1 表示 True, 其他任何值（包括未设置）都表示 False
DEBUG = os.environ.get('DJANGO_DEBUG', '1') == '1' # 开发时默认为 True

# 从环境变量读取允许的主机，并用空格分隔
ALLOWED_HOSTS_STRING = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost 127.0.0.1')
ALLOWED_HOSTS = ALLOWED_HOSTS_STRING.split(' ') if ALLOWED_HOSTS_STRING else []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'rest_framework',
    'rest_framework_gis',
    'ruins_api.apps.RuinsApiConfig',
    'django_bootstrap5',
    'leaflet',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main_project.urls'

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

WSGI_APPLICATION = 'main_project.wsgi.application'


# Database Configuration for Local Development
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'ruins_db',
        'USER': 'postgres',
        'PASSWORD': 'postgres123!',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# GDAL/GEOS Library Path Configuration for Windows
if os.name == 'nt':
    OSGEO4W_DIR = r"C:\OSGeo4W"
    try:
        # 请再次确认您 C:\OSGeo4W\bin 目录下的 gdal dll 文件名是否真的是 gdal310.dll
        gdal_dll_path_str = os.path.join(OSGEO4W_DIR, 'bin', 'gdal310.dll')
        if os.path.exists(gdal_dll_path_str):
            GDAL_LIBRARY_PATH = gdal_dll_path_str
        else:
            print(f"警告: 在 {gdal_dll_path_str} 未找到 GDAL DLL。GeoDjango 可能无法正常工作。")

        geos_dll_path_str = os.path.join(OSGEO4W_DIR, 'bin', 'geos_c.dll')
        if os.path.exists(geos_dll_path_str):
            GEOS_LIBRARY_PATH = geos_dll_path_str
        else:
            print(f"警告: 在 {geos_dll_path_str} 未找到 GEOS DLL。GeoDjango 可能无法正常工作。")

    except Exception as e:
        print(f"设置 GDAL/GEOS 路径时出错: {e}")


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Internationalization
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True

# Static and Media files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'mediafiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Leaflet settings
LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (36.0, 103.8),
    'DEFAULT_ZOOM': 4,
    'MIN_ZOOM': 3,
    'MAX_ZOOM': 18,
    'RESET_VIEW': True,
}