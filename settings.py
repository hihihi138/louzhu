# Django settings for bestyouku project.
import os
import socket

ROOT_PATH = os.path.dirname(__file__)

if socket.gethostname() in ('harness-test.bej.corp.google.com', 'Muer Workstation', 'liujun-glaptop'):
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG
    
    DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    DATABASE_NAME = ROOT_PATH+'/louzhu.db'             # Or path to database file if using sqlite3.
    DATABASE_USER = ''             # Not used with sqlite3.
    DATABASE_PASSWORD = ''         # Not used with sqlite3.
    DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.
    
    # Email Host
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = 'bestyouku520@gmail.com'
    EMAIL_HOST_PASSWORD = 'youkujingxuan'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
else:
    DEBUG =  False
    TEMPLATE_DEBUG = DEBUG
    
    DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    DATABASE_NAME = 'louzhu_mydata'             # Or path to database file if using sqlite3.
    DATABASE_USER = 'louzhu'             # Not used with sqlite3.
    DATABASE_PASSWORD = '3351808'         # Not used with sqlite3.
    DATABASE_HOST = 'mysql.alwaysdata.com'             # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.
    
    EMAIL_HOST = 'smtp.alwaysdata.com'
    EMAIL_HOST_USER = 'louzhu@alwaysdata.net'
    EMAIL_HOST_PASSWORD = '3351808'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL = 'no-reply@louzhu.com'

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
    ('Muer', 'hihihi138@gmail.com'),
)
SEND_BROKEN_LINK_EMAILS = False
MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-CN'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(ROOT_PATH, 'public/site_media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/site_media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 't)3hk3pg+vgn*3+l_zq@ouau($o1xji4tn6d0-ge81+0m9^i80'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'louzhu.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(ROOT_PATH, 'templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    'louzhu.douban',
)
