from pathlib import Path
import os
import dj_database_url # 导入 dj-database-url 包

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-default-key-for-dev-only')

# 在 .env 文件中设置 DJANGO_DEBUG=1 表示 True, 其他任何值（包括未设置）都表示 False
DEBUG = os.environ.get('DJANGO_DEBUG', '0') == '1'

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
    'ruins_api.apps.RuinsApiConfig', # 您的核心应用
    'django_bootstrap5',
    'leaflet', # django-leaflet 包对应的应用名
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

# --- 核心修改 ---
# 将这里的项目名从 'RuinsProject' 修改为 'main_project'
ROOT_URLCONF = 'main_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # This line tells Django to look in the global `templates` folder
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True, # This tells Django to also look inside each app's `templates` folder
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

# --- 核心修改 ---
# 将这里的项目名从 'RuinsProject' 修改为 'main_project'
WSGI_APPLICATION = 'main_project.wsgi.application'


# 使用 dj-database-url 从 DATABASE_URL 环境变量读取数据库配置
DATABASES = {
    'default': dj_database_url.config(
        # 从环境变量 'DATABASE_URL' 读取连接信息
        default=os.environ.get('DATABASE_URL'),
        # 告诉 dj_database_url 我们使用的是 PostGIS 引擎
        engine='django.contrib.gis.db.backends.postgis',
        # 设置连接最大存活时间
        conn_max_age=600
    )
}


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

# 新增：配置 WhiteNoise 用于静态文件存储
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