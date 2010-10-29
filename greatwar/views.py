#import logging
#from lxml import etree
#from urllib import urlencode

from django.shortcuts import render_to_response
from django.http import HttpResponse
#from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template import RequestContext

#from eulcore.django.existdb.db import ExistDB
#from eulcore.existdb.exceptions import DoesNotExist # ReturnedMultiple needed also ?
#from eulcore.xmlmap.teimap import TEI_NAMESPACE

def index(request):
    "Front page"
    return render_to_response('index.html')
