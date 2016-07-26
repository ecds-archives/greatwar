# Django settings for findingaids project. Or great war project.
from os import path

# Get the directory of this file for relative dir paths.
# Django sets too many absolute paths.
BASE_DIR = path.dirname(path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = path.join(BASE_DIR, 'static')

# Additional locations of static files
STATICFILES_DIRS = [
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    path.join(BASE_DIR, 'sitemedia'),
]

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
#MEDIA_ROOT = path.join(BASE_DIR, 'media')
#'Users/sepalme/Desktop/greatwar/sitemedia'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
#ADMIN_MEDIA_PREFIX = '/media/'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'eultheme.middleware.DownpageMiddleware'
)

ROOT_URLCONF = 'greatwar.urls'

TEMPLATE_DIRS = (
    path.join(BASE_DIR, 'templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'eulxml',
    'eulexistdb',
    'eulfedora',
    'eultheme',
    'widget_tweaks',
    'downtime',
    'django_auth_ldap',
    'greatwar.postcards',
    'greatwar.poetry',
]

AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.contrib.messages.context_processors.messages",
    # additional context processors
    "django.core.context_processors.request", # always include request in render context
    "eultheme.context_processors.template_settings",
    "eultheme.context_processors.downtime_context"
)


EXISTDB_INDEX_CONFIGFILE = path.join(BASE_DIR, "greatwar", "exist_index.xconf")

# temporary pid - should eventually use ARK. must match PID in fixture
POSTCARD_COLLECTION_PID = 'emory-control:Beck-GreatWar-Postcards-collection'

# This is used to identify Great War records.  The relation is stored on each postcard object
RELATION = 'The Great War 1914-1918'

# the default owner of all fedora objects created by this app
FEDORA_OBJECT_OWNERID = 'beck-greatwar'

# used to identidy the description for the postcard in the description elements
POSTCARD_DESCRIPTION_LABEL = 'Description:\n'

# used to identidy the floating text in the description elements
POSTCARD_FLOATINGTEXT_LABEL = 'Text on postcard:\n'

# exempted paths for downtime; exempts any urls starting with these strings
DOWNTIME_EXEMPT_PATHS = (
    '/about',
    '/admin',
    '/poetry',
    '/links',
    '/credits'
)
DOWNTIME_EXEMPT_EXACT_URLS = (
    '/',
)

# list of IPs that can access the site despite downtime
# DOWNTIME_ALLOWED_IPS = ['127.0.0.1']

import sys
try:
    sys.path.extend(EXTENSION_DIRS)
except NameError:
    pass # EXTENSION_DIRS not defined. This is OK; we just won't use it.
del sys

try:
    from localsettings import *
except ImportError:
    import sys
    print >>sys.stderr, 'No local settings. Trying to start, but if ' + \
        'stuff blows up, try copying localsettings-sample.py to ' + \
        'localsettings.py and setting appropriately for your environment.'
    pass

try:
    # NOTE: errors if DATABASES is not configured (in some cases),
    # so this must be done after importing localsettings
    import django_nose
    INSTALLED_APPS.append('django_nose')
    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
    NOSE_PLUGINS = [
        'eulfedora.testutil.EulfedoraSetUp',
        'eulexistdb.testutil.ExistDBSetUp',
        # ...
    ]
    NOSE_ARGS = ['--with-eulfedorasetup', '--with-existdbsetup']
except ImportError:
    pass


