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
    POET_STRING = '''<choice xmlns="http://www.tei-c.org/ns/1.0">
        <reg>Peterson, Margaret</reg>
    </choice>'''

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

        
class FullTextPoetryViewsTest(TestCase):
    # tests for views that require eXist full-text index
    exist_fixtures = { 'index' : settings.EXISTDB_INDEX_CONFIGFILE,
                       'directory' : exist_fixture_path }

    def test_view_search_keyword(self):
        search_url = reverse('poetry:search')

        # TODO: test/cleanup form display - shouldn't complain about no search terms,
        # 0 results when user hasn't entered a query

        response = self.client.get(search_url, {'keyword': 'spectre'})
        expected = 200
        self.assertEqual(response.status_code, expected,
                        'Expected %s but returned %s for %s' % \
                        (expected, response.status_code, search_url))
        
        self.assertContains(response, reverse('poetry:poem', kwargs={'doc_id':'fiery',
            'div_id': 'fiery012'}),
            msg_prefix='search results include link to poem with match (fiery012)')
        self.assertContains(response, 'From Germany',
            msg_prefix='search results include title of poem with match')
        self.assertContains(response, reverse('poetry:book-toc', kwargs={'doc_id':'fiery'}),
            msg_prefix='search results include link to book that contains poem with match')
        self.assertContains(response, 'Pale <span class="exist-match">spectre</span>',
            msg_prefix='search results include poem line with search term highlighted')

        # TODO: also matches fiery004 with title of 'None' - fix title display, test

        # exact phrase search - should work in poem line matches
        response = self.client.get(search_url, {'keyword': '"pale spectre"'})
        expected = 200
        self.assertEqual(response.status_code, expected,
                        'Expected %s but returned %s for %s' % \
                        (expected, response.status_code, search_url))
        self.assertContains(response, '<span class="exist-match">Pale spectre</span> of the slain',
            msg_prefix='search results include poem line with exact phrase search term highlighted')
