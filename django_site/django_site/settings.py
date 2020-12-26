import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'bNpvCDKINH8go7qsL7V3Y3VQ5fy0GEnJVvXtoKUI9OIuqmt1L0'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    # 第三方插件
    'simpleui',
    
    # 官方模块
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # 第三方插件
    'debug_toolbar',
    'import_export',

    # 自定义的应用
    'django_site',
    'app1.apps.App1Config',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # 导入 debug_toolbar
]

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

DATABASES = {
    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'mysql': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db1',
        'USER': 'root',
        'PASSWORD': '******',
        'HOST': '10.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES', innodb_strict_mode=1",
            'charset': 'utf8mb4'
        }
    }
}

DATABASES = {'default': DATABASES['sqlite']}

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

STATIC_URL       = '/static/'
STATIC_ROOT      = os.path.join(BASE_DIR, 'static')

ROOT_URLCONF     = 'django_site.urls'
WSGI_APPLICATION = 'django_site.wsgi.application'

LANGUAGE_CODE    = 'zh-hans'
TIME_ZONE        = 'Asia/Shanghai'
USE_I18N         = True
USE_L10N         = True
USE_TZ           = True

# 以上是 Django 自带的配置项

# 以下是导入某些模块的内容作为配置
from .configs.logging       import *
from .configs.simple_ui     import *
from .configs.import_export import *
from .configs.cache         import *


INTERNAL_IPS  = [       # 对哪些 IP 显示调试工具栏 debug_toolbar
    '127.0.0.1',
]
