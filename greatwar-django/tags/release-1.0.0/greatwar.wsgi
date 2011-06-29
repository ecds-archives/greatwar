import os
import sys
#sys.path.append('/home/httpd/greatwar/greatwar')
#sys.path = ['/home/httpd/greatwar/greatwar','/home/httpd/greatwar' ] + sys.path
os.environ['DJANGO_SETTINGS_MODULE'] = 'greatwar.settings'
os.environ['PYTHON_EGG_CACHE'] = '/tmp'
os.environ['HTTP_PROXY'] = 'http://skoda.library.emory.edu:3128/'
os.environ['VIRTUAL_ENV'] = '/home/httpd/greatwar/env/'

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
