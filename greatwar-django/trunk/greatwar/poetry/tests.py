"""
Great War Poetry Test Cases
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
  
    FIXTURES = ['flower.xml', 'fiery.xml','lest.xml']
    POET_STRING = '<docAuthor n="Peterson, Margaret">Margaret Peterson</docAuthor>' 

    def setUp(self):
      
        # load the three xml poetry objects    
        self.poetry = dict()
        for file in self.FIXTURES:    
          filebase = file.split('.')[0]       
          self.poetry[filebase] = load_xmlobject_from_file(path.join(exist_fixture_path,
                                file), PoetryBook)                                                  
        # load the poet fixture docAuther
        self.poet = load_xmlobject_from_string(self.POET_STRING, Poet)
                                  
    def test_init(self):
        for file, p in self.poetry.iteritems():   
            self.assert_(isinstance(p, PoetryBook))
          
    def test_xml_fixture_load(self):
        self.assertEqual(3, len(self.poetry))    
      
    def test_poet_attributes(self):    
        self.assertEqual(self.poet.first_letter, 'P')
        self.assertEqual(self.poet.name, 'Peterson, Margaret')
