# Django local settings for edc project.

# all settings in debug section should be false in production environment
[debug]
DEBUG = True
TEMPLATE_DEBUG = DEBUG
DEV_ENV = True

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

#This setting is used instead of the referencing :class:`~django.contrib.sites.models.Site`
#When creating arks, this will be the base of the target uri.
#Usually, this value will be tied to the site through the Django framework.
#Since we are not using the admin portion for anything else it would be a lot
#of overhead to activate it for this one variable.
#If admin section is ever activated, this logic should be moved there.
BASE_URL='http://myurl.com'  #no trailing slash

#We will not be using a RDB but this will allow tests to run
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'no_db'

#Specify Session Engine
CACHE_BACKEND = 'file:///tmp/django_cache'
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# configure an HTTP PROXY to enable lxml to cache XML Schemas (e.g., EAD XSD)
import os
os.environ['HTTP_PROXY'] = 'http://spiderman.library.emory.edu:3128'

#Exist DB Settings
EXISTDB_SERVER_PROTOCOL = "http://"
# hostname, port, & path to exist xmlrpc - e.g., "localhost:8080/exist/xmlrpc"
EXISTDB_SERVER_HOST     = ""
EXISTDB_SERVER_USER     = ""
EXISTDB_SERVER_PWD      = ""
#EXISTDB_SERVER_URL      = EXISTDB_SERVER_PROTOCOL + EXISTDB_SERVER_HOST
EXISTDB_SERVER_URL  = EXISTDB_SERVER_PROTOCOL + EXISTDB_SERVER_HOST
# collection should begin with / -  e.g., /edc
EXISTDB_ROOT_COLLECTION = ""
EXISTDB_TEST_COLLECTION = ""
# NOTE: EXISTDB_INDEX_CONFIGFILE is configured in settings.py (for fa; is it for gw?)

# Fedora Repository settings
FEDORA_ROOT = 'https://host:port/fedora/'
FEDORA_PIDSPACE = 'greatwar'
#configure these for unit tests only
#FEDORA_USER = 'user'
#FEDORA_PASS = 'pass'



# from fa:
# a bug in python xmlrpclib loses the timezone; override it here
# most likely, you want either tz.tzlocal() or tz.tzutc()
from dateutil import tz
EXISTDB_SERVER_TIMEZONE = tz.tzlocal()

# from fa:
# EULCORE LDAP SETTINGS
# LDAP login settings. These are configured for emory, but you'll need
# to get a base user DN and password elsewhere.
AUTH_LDAP_SERVER = '' # i.e. 'ldaps://vlad.service.emory.edu'
AUTH_LDAP_BASE_USER = '' # i.e. 'uid=USERNAME,ou=services,o=emory.edu'
AUTH_LDAP_BASE_PASS = '' # password for USERNAME above
AUTH_LDAP_SEARCH_SUFFIX = '' # i.e. 'o=emory.edu'
AUTH_LDAP_SEARCH_FILTER = '' # i.e. '(uid=%s)'
AUTH_LDAP_CHECK_SERVER_CERT = False # ALWAYS SET True in production.
AUTH_LDAP_CA_CERT_PATH = '' # absolute path of cert

# pidman PID generation
PIDMAN_HOST = 'http://pid.emory.edu/' # the web root where we'll ask for pids
PIDMAN_USER = 'user'
PIDMAN_PASSWORD = 'pass'
PIDMAN_DOMAIN = 'http://pid.emory.edu/domains/123/' # the full url of the domain or subdomain we'll create pids in


ADDITIONAL_DATA_INDEX   = ""
DOI_PURL_HOST = "http://dx.doi.org/"

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

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''


#Logger Settings
import logging
#logging levels: NOLOG, CRITICAL, ERROR, WARNING, INFO, DEBUG
LOGGING_LEVEL=logging.NOLOG
LOGGING_FORMAT="%(asctime)s : %(name)s:  %(levelname)s : %(message)s"
LOGGING_FILENAME="" # "" will print to stdout
