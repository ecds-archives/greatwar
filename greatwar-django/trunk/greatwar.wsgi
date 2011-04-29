import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'greatwar.settings'
os.environ['PYTHON_EGG_CACHE'] = '/tmp'
os.environ['HTTP_PROXY'] = 'http://spiderman.library.emory.edu:3128/'

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()