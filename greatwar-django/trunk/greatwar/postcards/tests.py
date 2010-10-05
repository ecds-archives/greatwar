"""
Great War Postcards Test Cases
"""

from datetime import datetime
from os import path
import re
from time import sleep
from types import ListType
from lxml import etree
from urllib import quote as urlquote

from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.http import Http404, HttpRequest
from django.template import RequestContext, Template
from django.test import Client, TestCase as DjangoTestCase

from eulcore.xmlmap  import load_xmlobject_from_file, load_xmlobject_from_string, XmlObject
from eulcore.xmlmap.teimap import Tei, TeiDiv, TeiLineGroup, TEI_NAMESPACE
from eulcore.django.existdb.db import ExistDB
from eulcore.django.test import TestCase

from greatwar.poetry.models import PoetryBook, Poem, Poet
from greatwar.poetry.views import books, book_toc, div, poets, poets_by_firstletter, _show_poets, poet_list

import logging

exist_fixture_path = path.join(path.dirname(path.abspath(__file__)), 'fixtures')
exist_index_path = path.join(path.dirname(path.abspath(__file__)), '..', 'exist_index.xconf')

class PoetryTestCase(DjangoTestCase):
                                  
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)
