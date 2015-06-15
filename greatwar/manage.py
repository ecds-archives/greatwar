#!/usr/bin/env python
from django.core.management import execute_manager
try:
    import settings # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

if __name__ == "__main__":
    #setup logger
    import sys
    import localsettings
    import logging
    logging.basicConfig(level=localsettings.LOGGING_LEVEL, format=localsettings.LOGGING_FORMAT, filename=localsettings.LOGGING_FILENAME)

    # load test settings when running tests
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        import testsettings as settings

    execute_manager(settings)
