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
exist_index_path = path.join(path.dirname(path.abspath(__file__)), '..', 'collection.xconf')

class PoetryTestCase(DjangoTestCase):
  
    FIXTURES = ['flower.xml', 'fiery.xml', 'lest.xml']
    POET_STRING = '<docAuthor><name><choice><reg>Peterson, Margaret</reg><sic>Margaret Peterson</sic></choice></name></docAuthor>' 

    def setUp(self):
      
        # load the three xml poetry objects    
        self.poetry = dict()
        for file in self.FIXTURES:    
          filebase = file.split('.')[0]       
          self.poetry[filebase] = load_xmlobject_from_file(path.join(exist_fixture_path,
                                file), PoetryBook)                                                  
        # load the poet fixture docAuthor
        self.poet = load_xmlobject_from_string(self.POET_STRING, Poet)
                                  
    def test_init(self):
        for file, p in self.poetry.iteritems():   
            self.assert_(isinstance(p, PoetryBook))
          
    def test_xml_fixture_load(self):
        self.assertEqual(3, len(self.poetry))    
      
    def test_poet_attributes(self):    
        self.assertEqual(self.poet.first_letter, 'P')
        self.assertEqual(self.poet.name, 'Peterson, Margaret')
        
    def test_view_simple(self):
        gw_url = reverse('poetry:books')
        response = self.client.get(gw_url)
        expected = 200
        self.assertEqual(response.status_code, expected,
                        'Expected %s but returned %s for %s' % \
                        (expected, response.status_code, gw_url)) 
             
    def test_view_search_title(self):
        gw_url = "http://localhost:8001/poetry/search/?title=Flower"
        response = self.client.get(gw_url)
        expected = 200
        self.assertEqual(response.status_code, expected,
                        'Expected %s but returned %s for %s' % \
                        (expected, response.status_code, gw_url))                         
        # should include 'Flower'
        self.assertContains(response, 'Flower')
        
    def test_view_search_author(self):
        gw_url = "http://localhost:8001/poetry/search/?author=Smith"
        response = self.client.get(gw_url)
        expected = 200
        self.assertEqual(response.status_code, expected,
                        'Expected %s but returned %s for %s' % \
                        (expected, response.status_code, gw_url))                         
        # should include 'Smith'
        self.assertContains(response, 'Smith')
        
    def test_view_search_keyword(self):
        gw_url = "http://localhost:8001/poetry/search/?keyword=rainbow"
        response = self.client.get(gw_url)
        expected = 200
        self.assertEqual(response.status_code, expected,
                        'Expected %s but returned %s for %s' % \
                        (expected, response.status_code, gw_url))                         
        # should include 'rainbow'
        self.assertContains(response, 'rainbow')                
